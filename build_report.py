# -*- coding: utf-8 -*-
"""Generuje drukowalny raport HTML (Ctrl+P -> Zapisz jako PDF) na podstawie report_data.json."""
import json
import html
from variants_db import PLAIN_ADVICE

RISK_ORDER = {
    "wysokie": 0, "podwyzszone": 1, "lekko podwyzszone": 2,
    "lekko podwyzszone ryzyko niedoboru": 2, "umiarkowane": 2,
    "nosiciel": 3, "info": 4, "standardowe": 5,
    "nieznany": 6, "brak_odczytu": 7, "brak_danych": 8,
}
RISK_LABEL = {
    "wysokie": "Wysokie ryzyko", "podwyzszone": "Podwyzszone ryzyko",
    "lekko podwyzszone": "Lekko podwyzszone", "lekko podwyzszone ryzyko niedoboru": "Lekko podwyzszone",
    "umiarkowane": "Umiarkowane", "nosiciel": "Nosiciel", "info": "Informacyjne",
    "standardowe": "Standardowe / typowe", "nieznany": "Nieopisany genotyp",
    "brak_odczytu": "Brak odczytu", "brak_danych": "Brak danych na chipie",
}
RISK_CLASS = {
    "wysokie": "risk-high", "podwyzszone": "risk-high",
    "lekko podwyzszone": "risk-mid", "lekko podwyzszone ryzyko niedoboru": "risk-mid",
    "umiarkowane": "risk-mid", "nosiciel": "risk-mid", "info": "risk-info",
    "standardowe": "risk-ok", "nieznany": "risk-muted",
    "brak_odczytu": "risk-muted", "brak_danych": "risk-muted",
}

CSS = """
:root{
  --paper: #f6f5f1;
  --paper-raised: #ffffff;
  --ink: #1f2623;
  --ink-soft: #4b544f;
  --line: #dcd8cd;
  --accent: #2f5d54;
  --accent-soft: #e4ede9;
  --ok-fg: #2c6e49; --ok-bg: #e5f1e8;
  --mid-fg: #9a6a12; --mid-bg: #faf1dd;
  --high-fg: #a5312a; --high-bg: #fbe8e6;
  --info-fg: #395b8f; --info-bg: #e8eef8;
  --muted-fg: #8b8f8a; --muted-bg: #eeece5;
}
@media (prefers-color-scheme: dark){
  :root{
    --paper: #14181a; --paper-raised: #1b2023; --ink: #e9ede9; --ink-soft: #a9b2ac;
    --line: #2c3436; --accent: #7fb8a8; --accent-soft: #1e2f2b;
    --ok-fg: #7fd19a; --ok-bg: #1c2c22;
    --mid-fg: #e0b256; --mid-bg: #2e2712;
    --high-fg: #e58a83; --high-bg: #351f1d;
    --info-fg: #8fb1e0; --info-bg: #1c2634;
    --muted-fg: #7d8580; --muted-bg: #22282a;
  }
}
:root[data-theme="dark"]{
  --paper: #14181a; --paper-raised: #1b2023; --ink: #e9ede9; --ink-soft: #a9b2ac;
  --line: #2c3436; --accent: #7fb8a8; --accent-soft: #1e2f2b;
  --ok-fg: #7fd19a; --ok-bg: #1c2c22;
  --mid-fg: #e0b256; --mid-bg: #2e2712;
  --high-fg: #e58a83; --high-bg: #351f1d;
  --info-fg: #8fb1e0; --info-bg: #1c2634;
  --muted-fg: #7d8580; --muted-bg: #22282a;
}
:root[data-theme="light"]{
  --paper: #f6f5f1; --paper-raised: #ffffff; --ink: #1f2623; --ink-soft: #4b544f;
  --line: #dcd8cd; --accent: #2f5d54; --accent-soft: #e4ede9;
  --ok-fg: #2c6e49; --ok-bg: #e5f1e8;
  --mid-fg: #9a6a12; --mid-bg: #faf1dd;
  --high-fg: #a5312a; --high-bg: #fbe8e6;
  --info-fg: #395b8f; --info-bg: #e8eef8;
  --muted-fg: #8b8f8a; --muted-bg: #eeece5;
}
*{ box-sizing: border-box; }
body{
  margin:0; background: var(--paper); color: var(--ink);
  font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.5;
}
.page{ max-width: 860px; margin: 0 auto; padding: 48px 32px 80px; }
.cover{
  border-bottom: 2px solid var(--accent);
  padding-bottom: 28px; margin-bottom: 36px;
}
.cover-kicker{
  font-size: 12px; letter-spacing: .12em; text-transform: uppercase;
  color: var(--accent); font-weight: 600; margin-bottom: 10px;
}
.cover h1{
  font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
  font-size: 42px; margin: 0 0 14px; text-wrap: balance; letter-spacing: -0.01em;
}
.cover-meta{
  display:flex; flex-wrap: wrap; gap: 8px 22px;
  font-size: 13px; color: var(--ink-soft); margin-bottom: 18px;
  font-variant-numeric: tabular-nums;
}
.disclaimer{
  background: var(--accent-soft); border: 1px solid var(--line); border-radius: 10px;
  padding: 14px 16px; font-size: 13px; color: var(--ink-soft); line-height: 1.55;
}
.apoe-card{
  background: var(--paper-raised); border: 1px solid var(--line); border-left: 4px solid var(--accent);
  border-radius: 10px; padding: 18px 20px; margin: 0 0 36px;
}
.apoe-head{ display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.apoe-tag{
  font-family: ui-monospace, "SF Mono", Consolas, monospace; font-size: 11px;
  background: var(--accent); color: var(--paper); padding: 2px 8px; border-radius: 5px;
  letter-spacing: .04em;
}
.apoe-title{ font-weight: 600; font-size: 14.5px; }
.apoe-body{ margin: 0; font-size: 14px; color: var(--ink-soft); }

.category{ margin-bottom: 32px; break-inside: avoid-page; }
.category h2{
  font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
  font-size: 20px; font-weight: 600; margin: 0 0 14px;
  padding-bottom: 8px; border-bottom: 1px solid var(--line);
}
.variant-list{ display:flex; flex-direction:column; gap: 10px; }
.variant{
  background: var(--paper-raised); border: 1px solid var(--line); border-radius: 10px;
  padding: 14px 16px; display: grid; grid-template-columns: 1fr 150px; gap: 14px;
  break-inside: avoid-page;
}
.v-heading{ display:flex; align-items: baseline; gap: 8px; flex-wrap: wrap; margin-bottom: 4px; }
.v-name{ font-weight: 600; font-size: 14.5px; }
.v-gene{ font-size: 12px; color: var(--ink-soft); font-family: ui-monospace, "SF Mono", Consolas, monospace; }
.v-desc{ font-size: 13.5px; color: var(--ink-soft); }
.v-note{ font-size: 12px; color: var(--ink-soft); margin-top: 6px; font-style: italic; opacity: .85; }
.v-side{ display:flex; flex-direction: column; align-items: flex-end; gap: 6px; text-align:right; }
.badge{
  font-size: 11px; font-weight: 600; padding: 3px 9px; border-radius: 999px;
  white-space: nowrap;
}
.risk-high{ color: var(--high-fg); background: var(--high-bg); }
.risk-mid{ color: var(--mid-fg); background: var(--mid-bg); }
.risk-ok{ color: var(--ok-fg); background: var(--ok-bg); }
.risk-info{ color: var(--info-fg); background: var(--info-bg); }
.risk-muted{ color: var(--muted-fg); background: var(--muted-bg); }
.genotype{
  font-family: ui-monospace, "SF Mono", Consolas, monospace; font-size: 13px; font-weight: 600;
}
.rsid{ font-family: ui-monospace, "SF Mono", Consolas, monospace; font-size: 11px; color: var(--ink-soft); }

.page-footer{
  margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--line);
  font-size: 11.5px; color: var(--muted-fg); text-align: center;
}

@page{ size: A4; margin: 14mm 12mm; }
@media print{
  :root{
    --paper: #ffffff; --paper-raised: #ffffff; --ink: #111; --ink-soft: #444; --line: #ccc;
  }
  body{ background: #fff; font-size: 12.5px; }
  .page{ max-width: none; padding: 0; }
  .variant, .apoe-card{ box-shadow: none; }
  .category{ break-inside: auto; }
  .variant, .apoe-card{ break-inside: avoid; }
  .badge, .risk-high, .risk-mid, .risk-ok, .risk-info, .risk-muted{
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }
  a[href]:after{ content: none; }
}
@media (max-width: 560px){
  .variant{ grid-template-columns: 1fr; }
  .v-side{ flex-direction: row; align-items: center; justify-content: flex-start; }
}
"""

def esc(s):
    return html.escape(str(s)) if s is not None else ""

def render_apoe(apoe):
    if not apoe:
        return ""
    return f'''
    <div class="apoe-card">
      <div class="apoe-head">
        <span class="apoe-tag">APOE</span>
        <span class="apoe-title">Ryzyko choroby Alzheimera (interpretacja laczna rs429358 + rs7412)</span>
      </div>
      <p class="apoe-body">{esc(apoe["interpretation"])}</p>
    </div>'''

def render_variant_row(r):
    risk = r["risk"]
    cls = RISK_CLASS.get(risk, "risk-muted")
    label = RISK_LABEL.get(risk, risk)
    genotype = r["genotype"] if r["genotype"] else "—"
    note = f'<div class="v-note">{esc(r["note"])}</div>' if r.get("note") else ""
    return f'''
        <div class="variant">
          <div class="v-main">
            <div class="v-heading">
              <span class="v-name">{esc(r["name"])}</span>
              <span class="v-gene">{esc(r["gene"])}</span>
            </div>
            <div class="v-desc">{esc(r["desc"])}</div>
            {note}
          </div>
          <div class="v-side">
            <span class="badge {cls}">{esc(label)}</span>
            <span class="genotype">{esc(genotype)}</span>
            <span class="rsid">{esc(r["rsid"])}</span>
          </div>
        </div>'''

def render_category(cat, rows):
    rows_sorted = sorted(rows, key=lambda r: RISK_ORDER.get(r["risk"], 9))
    body = "\n".join(render_variant_row(r) for r in rows_sorted)
    return f'''
      <section class="category">
        <h2>{esc(cat)}</h2>
        <div class="variant-list">
          {body}
        </div>
      </section>'''

def build_person_html(person, generated_date):
    name = person["name"]
    results = person["results"]
    apoe = person.get("apoe")

    categories = {}
    for r in results:
        categories.setdefault(r["category"], []).append(r)

    counts = {"wysokie": 0, "podwyzszone": 0, "info_or_more": 0}
    for r in results:
        if r["risk"] in ("wysokie",):
            counts["wysokie"] += 1
        elif r["risk"] in ("podwyzszone",):
            counts["podwyzszone"] += 1

    cat_order = [
        "Choroby neurodegeneracyjne", "Zakrzepica / uklad krazenia", "Cukrzyca / metabolizm",
        "Choroby metaboliczne", "Nowotwory", "Alergie / odpornosc", "Alergie / autoimmunologia",
        "Farmakogenomika", "Metabolizm alkoholu / reakcje", "Metabolizm alkoholu / uzaleznienia",
        "Uzaleznienia", "Uzaleznienia / neurologia", "Neurologia / metabolizm",
        "Metabolizm / serce", "Wydolnosc fizyczna", "Sen", "Odczuwanie bolu",
        "Dlugowiecznosc", "Skora / opalanie", "Cechy fizyczne", "Cechy / nietolerancje",
        "Witaminy / metabolizm",
    ]
    ordered_cats = [c for c in cat_order if c in categories]
    ordered_cats += [c for c in categories if c not in ordered_cats]

    sections = "\n".join(render_category(c, categories[c]) for c in ordered_cats)

    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<title>Raport genetyczny — {esc(name)}</title>
<style>
{CSS}
</style>
</head>
<body>
<div class="page">
  <header class="cover">
    <div class="cover-kicker">RAPORT DANYCH SUROWYCH DNA &middot; AncestryDNA</div>
    <h1>{esc(name)}</h1>
    <div class="cover-meta">
      <span>Wygenerowano: {esc(generated_date)}</span>
      <span>Zanalizowanych markerow: {person["total_snps"]:,}</span>
      <span>Wariantow w bazie: {len(results)}</span>
    </div>
    <div class="disclaimer">
      To narzedzie NIE jest diagnostyka medyczna. Wiekszosc opisanych tu wariantow to
      statystyczne czynniki ryzyka o niewielkim lub umiarkowanym wplywie, ustalone na podstawie
      publikowanych badan populacyjnych (GWAS, PharmGKB, literatura recenzowana). Nie zastepuja
      konsultacji lekarskiej ani badania genetycznego wykonanego w celach klinicznych. Interpretacje
      moga sie zmieniac wraz z postepem nauki.
    </div>
  </header>

  {render_apoe(apoe)}

  {sections}

  <footer class="page-footer">
    Raport wygenerowany lokalnie na podstawie surowych danych AncestryDNA — wylacznie do uzytku prywatnego/edukacyjnego.
  </footer>
</div>
</body>
</html>'''

SIMPLE_CSS = """
:root{
  --paper: #fdfcfa; --ink: #1a1a1a; --ink-soft: #444;
  --line: #e4e1d8; --accent: #2f5d54;
  --uwaga-fg:#8a3b1f; --uwaga-bg:#fbeee6; --uwaga-bd:#d98a5f;
  --lekarz-fg:#1f4e8a; --lekarz-bg:#e9f1fb; --lekarz-bd:#5f93d9;
  --styl-fg:#2c6e2c; --styl-bg:#eef7ec; --styl-bd:#6fb85f;
  --dobra-fg:#8a6d1f; --dobra-bg:#fdf6e3; --dobra-bd:#d9b95f;
  --ciekaw-fg:#5c3d8a; --ciekaw-bg:#f2ecfb; --ciekaw-bd:#a583d9;
}
@media (prefers-color-scheme: dark){
  :root{
    --paper:#181614; --ink:#f0ede6; --ink-soft:#c7c2b7; --line:#3a3630; --accent:#7fb8a8;
    --uwaga-fg:#f0b499; --uwaga-bg:#3a2419; --uwaga-bd:#d98a5f;
    --lekarz-fg:#a9c8f0; --lekarz-bg:#182338; --lekarz-bd:#5f93d9;
    --styl-fg:#b3e0a6; --styl-bg:#1c2c19; --styl-bd:#6fb85f;
    --dobra-fg:#f0dca6; --dobra-bg:#332a15; --dobra-bd:#d9b95f;
    --ciekaw-fg:#d3b9f0; --ciekaw-bg:#271c38; --ciekaw-bd:#a583d9;
  }
}
*{ box-sizing: border-box; }
body{
  margin:0; background: var(--paper); color: var(--ink);
  font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6; font-size: 17px;
}
.page{ max-width: 760px; margin: 0 auto; padding: 40px 30px 60px; }
.cover h1{
  font-family: Georgia, "Iowan Old Style", serif; font-size: 34px; margin: 6px 0 4px;
}
.cover-sub{ color: var(--ink-soft); font-size: 15px; margin-bottom: 18px; }
.intro{
  background: var(--accent); color: #fff; border-radius: 12px; padding: 18px 20px;
  font-size: 15.5px; margin-bottom: 28px; line-height: 1.55;
}
.intro strong{ font-size: 16px; }
h2.sec-title{
  font-size: 22px; margin: 34px 0 14px; padding-bottom: 6px;
  border-bottom: 2px solid var(--line);
}
.item{
  border-left: 6px solid var(--bd); background: var(--bg); color: var(--fg);
  border-radius: 10px; padding: 16px 18px; margin-bottom: 14px;
  break-inside: avoid;
}
.item .item-head{ display:flex; align-items:center; gap:10px; margin-bottom: 6px; }
.item .icon{ font-size: 22px; }
.item .title{ font-weight: 700; font-size: 16.5px; color: var(--ink); }
.item .text{ font-size: 15.5px; color: var(--ink-soft); }
.empty-note{ color: var(--ink-soft); font-style: italic; font-size: 14.5px; }
.footer-note{
  margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--line);
  font-size: 13.5px; color: var(--ink-soft); line-height: 1.6;
}
@page{ size: A4; margin: 16mm 14mm; }
@media print{
  :root{ --paper:#fff; --ink:#111; --ink-soft:#333; --line:#ccc; }
  body{ font-size: 14.5px; }
  .page{ max-width: none; padding: 0; }
  .item{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .intro{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
"""

SECTION_META = {
    "uwaga": ("⚠️ Na co warto zwrócić uwagę", "uwaga"),
    "lekarz": ("💊 Co warto powiedzieć lekarzowi lub farmaceucie", "lekarz"),
    "styl_zycia": ("🍽️ Styl życia i codzienne nawyki", "styl"),
    "dobra_wiadomosc": ("✅ Dobre wiadomości", "dobra"),
    "ciekawostka": ("✨ Ciekawostki", "ciekaw"),
}

def build_simple_person_html(person, generated_date):
    name = person["name"]
    results_by_rsid = {r["rsid"]: r for r in person["results"]}
    apoe = person.get("apoe")

    buckets = {k: [] for k in SECTION_META}

    if apoe:
        interp = apoe["interpretation"]
        if "PODWYZSZONE" in interp:
            buckets["uwaga"].append(("🧠", "Pamięć i mózg",
                "Wyniki sugerują nieco wyższą genetyczną skłonność do problemów z pamięcią w starszym "
                "wieku. To NIE oznacza, że choroba na pewno wystąpi. Warto: regularnie ćwiczyć umysł "
                "(czytanie, krzyżówki, nauka nowych rzeczy), dbać o aktywność fizyczną, dobry sen i "
                "zdrową dietę (dużo warzyw, ryby, mniej cukru) — to realnie zmniejsza ryzyko."))
        elif "OBNIZONE" in interp:
            buckets["dobra_wiadomosc"].append(("🧠", "Pamięć i mózg",
                "Wyniki genetyczne związane z ryzykiem Alzheimera są korzystne — nie ma podwyższonego "
                "ryzyka związanego z tym konkretnym genem."))

    for adv in PLAIN_ADVICE:
        r = results_by_rsid.get(adv["rsid"])
        if not r:
            continue
        if r["risk"] not in adv.get("trigger_risks", []):
            continue
        buckets[adv["section"]].append((adv["icon"], adv["title"], adv["text"]))

    body_parts = []
    for key, (heading, css_key) in SECTION_META.items():
        items = buckets[key]
        if not items:
            continue
        rows = "\n".join(f'''
          <div class="item" style="--bg:var(--{css_key}-bg); --fg:var(--{css_key}-fg); --bd:var(--{css_key}-bd);">
            <div class="item-head">
              <span class="icon">{icon}</span>
              <span class="title">{esc(title)}</span>
            </div>
            <div class="text">{esc(text)}</div>
          </div>''' for icon, title, text in items)
        body_parts.append(f'<h2 class="sec-title">{heading}</h2>\n{rows}')

    if not body_parts:
        body_parts.append('<p class="empty-note">Dla dostępnych danych nie znaleziono punktów wymagających uwagi w tej uproszczonej wersji — sprawdź pełny raport szczegółowy.</p>')

    content = "\n".join(body_parts)

    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<title>Wyniki DNA w prostych słowach — {esc(name)}</title>
<style>
{SIMPLE_CSS}
</style>
</head>
<body>
<div class="page">
  <header class="cover">
    <div class="cover-sub">WYNIKI TESTU DNA — WERSJA UPROSZCZONA</div>
    <h1>{esc(name)}</h1>
    <div class="cover-sub">Wygenerowano: {esc(generated_date)}</div>
  </header>

  <div class="intro">
    <strong>Co to jest ten dokument?</strong><br>
    To uproszczone podsumowanie wyników testu DNA — bez trudnych słów, tylko konkretne
    wskazówki: na co warto zwrócić uwagę, co powiedzieć lekarzowi i co można zrobić
    już dziś. To NIE jest diagnoza choroby — to tylko wskazówki oparte na badaniach
    naukowych dotyczących dużych grup ludzi. Ostateczne decyzje zawsze warto
    skonsultować z lekarzem rodzinnym.
  </div>

  {content}

  <div class="footer-note">
    Pełny, szczegółowy raport techniczny (z nazwami genów i wynikami badań) znajduje się
    w osobnym pliku. Ten dokument to jego uproszczona wersja, przygotowana z myślą o
    łatwym wydruku na kartce A4 i czytelności dla każdego, niezależnie od wiedzy
    o genetyce.
  </div>
</div>
</body>
</html>'''

if __name__ == "__main__":
    with open("report_data.json", encoding="utf-8") as f:
        data = json.load(f)
    date_str = "2026-07-11"
    for key in ("mama", "tata"):
        person = data[key]
        with open(f"raport_{key}.html", "w", encoding="utf-8") as f:
            f.write(build_person_html(person, date_str))
        print("Zapisano", f"raport_{key}.html")
        with open(f"raport_{key}_prosty.html", "w", encoding="utf-8") as f:
            f.write(build_simple_person_html(person, date_str))
        print("Zapisano", f"raport_{key}_prosty.html")
