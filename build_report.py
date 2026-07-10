# -*- coding: utf-8 -*-
"""Generuje drukowalny raport HTML (Ctrl+P -> Zapisz jako PDF) na podstawie report_data.json."""
import json
import html

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

@media print{
  body{ background: #fff; }
  .page{ max-width: none; padding: 0; }
  .variant, .apoe-card{ box-shadow: none; }
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

if __name__ == "__main__":
    with open("report_data.json", encoding="utf-8") as f:
        data = json.load(f)
    date_str = "2026-07-10"
    for key in ("mama", "tata"):
        html_out = build_person_html(data[key], date_str)
        fname = f"raport_{key}.html"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(html_out)
        print("Zapisano", fname)
