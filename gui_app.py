# -*- coding: utf-8 -*-
"""
GUI (Tkinter) do analizy surowych danych DNA i generowania raportow PDF.
Mozna spakowac do samodzielnego .exe (patrz build_exe.py) - nie wymaga
zainstalowanego Pythona u uzytkownika koncowego.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import zipfile
from datetime import date

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import analyze
import build_report

APP_TITLE = "DNAnalizator"


def desktop_dir():
    home = os.path.expanduser("~")
    for candidate in ("Desktop", "Pulpit"):
        path = os.path.join(home, candidate)
        if os.path.isdir(path):
            return path
    return home


def find_chromium_browser():
    """Szuka Edge/Chrome do konwersji HTML -> PDF (headless print-to-pdf)."""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    for exe in ("msedge.exe", "msedge", "chrome.exe", "google-chrome"):
        found = shutil.which(exe)
        if found:
            return found
    return None


def html_to_pdf(browser_path, html_path, pdf_path):
    uri = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    cmd = [
        browser_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={os.path.abspath(pdf_path)}",
        "--print-to-pdf-no-header",
        uri,
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=60, check=False)
    except Exception:
        return False
    return os.path.isfile(pdf_path) and os.path.getsize(pdf_path) > 0


def extract_dna_txt(input_path, work_dir):
    """Zwraca sciezke do pliku tekstowego z surowymi danymi DNA (rozpakowuje zip w razie potrzeby)."""
    if input_path.lower().endswith(".zip"):
        with zipfile.ZipFile(input_path) as zf:
            names = zf.namelist()
            txt_names = [n for n in names if n.lower().endswith(".txt")]
            if not txt_names:
                raise ValueError("W archiwum ZIP nie znaleziono pliku .txt z danymi DNA.")
            preferred = [n for n in txt_names if "ancestrydna" in n.lower()]
            pick = preferred[0] if preferred else txt_names[0]
            zf.extract(pick, work_dir)
            return os.path.join(work_dir, pick)
    return input_path


def safe_filename(name):
    slug = re.sub(r"[^\w\- ]", "", name, flags=re.UNICODE).strip().replace(" ", "_")
    return slug or "osoba"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("560x360")
        self.resizable(False, False)

        pad = {"padx": 12, "pady": 6}

        tk.Label(self, text="DNAnalizator", font=("Segoe UI", 16, "bold")).pack(pady=(14, 2))
        tk.Label(
            self,
            text="Analiza surowych danych DNA (AncestryDNA/23andMe) pod katem\n"
                 "zdrowia, farmakogenomiki i cech fizycznych - wylacznie lokalnie.",
            font=("Segoe UI", 9), fg="#555555", justify="center",
        ).pack(pady=(0, 10))

        form = tk.Frame(self)
        form.pack(fill="x", **pad)

        tk.Label(form, text="Imie / etykieta osoby:", anchor="w").grid(row=0, column=0, sticky="w", pady=4)
        self.name_var = tk.StringVar(value="Osoba")
        tk.Entry(form, textvariable=self.name_var, width=40).grid(row=0, column=1, sticky="we", pady=4)

        tk.Label(form, text="Plik z danymi DNA (.txt lub .zip):", anchor="w").grid(row=1, column=0, sticky="w", pady=4)
        self.input_var = tk.StringVar()
        tk.Entry(form, textvariable=self.input_var, width=40).grid(row=1, column=1, sticky="we", pady=4)
        tk.Button(form, text="Przegladaj...", command=self.pick_input).grid(row=1, column=2, padx=(6, 0))

        tk.Label(form, text="Folder na raport (domyslnie Pulpit):", anchor="w").grid(row=2, column=0, sticky="w", pady=4)
        self.output_var = tk.StringVar(value=desktop_dir())
        tk.Entry(form, textvariable=self.output_var, width=40).grid(row=2, column=1, sticky="we", pady=4)
        tk.Button(form, text="Przegladaj...", command=self.pick_output).grid(row=2, column=2, padx=(6, 0))

        form.columnconfigure(1, weight=1)

        self.generate_btn = tk.Button(
            self, text="Generuj raport", command=self.start_generate,
            bg="#2f5d54", fg="white", font=("Segoe UI", 11, "bold"), height=2,
        )
        self.generate_btn.pack(fill="x", padx=12, pady=(16, 6))

        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", padx=12, pady=(0, 6))

        self.status_var = tk.StringVar(value="Gotowy.")
        tk.Label(self, textvariable=self.status_var, fg="#555555", wraplength=520, justify="left").pack(
            fill="x", padx=12, pady=(0, 10)
        )

        self.open_folder_btn = tk.Button(self, text="Otworz folder z raportem", command=self.open_output_folder)
        self.open_folder_btn.pack(fill="x", padx=12)
        self.open_folder_btn.pack_forget()

    def pick_input(self):
        path = filedialog.askopenfilename(
            title="Wybierz plik z danymi DNA",
            filetypes=[("Dane DNA / ZIP", "*.txt *.zip"), ("Wszystkie pliki", "*.*")],
        )
        if path:
            self.input_var.set(path)

    def pick_output(self):
        path = filedialog.askdirectory(title="Wybierz folder na raport", initialdir=self.output_var.get())
        if path:
            self.output_var.set(path)

    def open_output_folder(self):
        path = self.output_var.get()
        if os.path.isdir(path):
            os.startfile(path)

    def start_generate(self):
        input_path = self.input_var.get().strip()
        output_dir = self.output_var.get().strip()
        name = self.name_var.get().strip() or "Osoba"

        if not input_path or not os.path.isfile(input_path):
            messagebox.showerror(APP_TITLE, "Wybierz prawidlowy plik z danymi DNA.")
            return
        if not output_dir or not os.path.isdir(output_dir):
            messagebox.showerror(APP_TITLE, "Wybierz prawidlowy folder docelowy.")
            return

        self.generate_btn.config(state="disabled")
        self.open_folder_btn.pack_forget()
        self.progress.start(12)
        self.status_var.set("Analizuje dane DNA, to moze potrwac kilkanascie sekund...")

        thread = threading.Thread(target=self._generate_worker, args=(input_path, output_dir, name), daemon=True)
        thread.start()

    def _generate_worker(self, input_path, output_dir, name):
        try:
            result = self._generate(input_path, output_dir, name)
            self.after(0, self._on_success, result)
        except Exception as exc:
            self.after(0, self._on_error, str(exc))

    def _generate(self, input_path, output_dir, name):
        work_dir = tempfile.mkdtemp(prefix="dnanalizator_")
        try:
            txt_path = extract_dna_txt(input_path, work_dir)
            person = analyze.run(name, txt_path)
        finally:
            shutil.rmtree(work_dir, ignore_errors=True)

        date_str = date.today().isoformat()
        slug = safe_filename(name)

        full_html = build_report.build_person_html(person, date_str)
        simple_html = build_report.build_simple_person_html(person, date_str)

        full_html_path = os.path.join(output_dir, f"raport_{slug}.html")
        simple_html_path = os.path.join(output_dir, f"raport_{slug}_prosty.html")
        with open(full_html_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        with open(simple_html_path, "w", encoding="utf-8") as f:
            f.write(simple_html)

        pdf_paths = []
        browser = find_chromium_browser()
        if browser:
            for html_path in (full_html_path, simple_html_path):
                pdf_path = html_path[:-5] + ".pdf"
                if html_to_pdf(browser, html_path, pdf_path):
                    pdf_paths.append(pdf_path)

        return {
            "total_snps": person["total_snps"],
            "html_paths": [full_html_path, simple_html_path],
            "pdf_paths": pdf_paths,
            "pdf_ok": len(pdf_paths) == 2,
        }

    def _on_success(self, result):
        self.progress.stop()
        self.generate_btn.config(state="normal")
        self.open_folder_btn.pack(fill="x", padx=12, pady=(0, 12))

        if result["pdf_ok"]:
            msg = (
                f"Gotowe! Przeanalizowano {result['total_snps']:,} markerow.\n"
                f"Zapisano {len(result['pdf_paths'])} pliki PDF (pelny + uproszczony) "
                f"w wybranym folderze."
            )
        else:
            msg = (
                f"Gotowe! Przeanalizowano {result['total_snps']:,} markerow.\n"
                f"Nie znaleziono przegladarki Edge/Chrome do automatycznego zapisu PDF - "
                f"zapisano pliki HTML. Otworz je w przegladarce i uzyj Ctrl+P -> Zapisz jako PDF."
            )
        self.status_var.set(msg)

    def _on_error(self, error_message):
        self.progress.stop()
        self.generate_btn.config(state="normal")
        self.status_var.set("Blad: " + error_message)
        messagebox.showerror(APP_TITLE, f"Nie udalo sie wygenerowac raportu:\n{error_message}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
