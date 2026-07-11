# -*- coding: utf-8 -*-
"""Generuje drukowalny raport HTML (Ctrl+P -> Zapisz jako PDF) na podstawie report_data.json."""
import json
import html
from variants_db import PLAIN_ADVICE

RISK_ORDER = {
    "wysokie": 0, "podwyzszone": 1, "lekko podwyzszone": 2,
    "lekko podwyzszone ryzyko niedoboru": 2, "umiarkowane": 2,
    "nosiciel": 3, "info": 4, "info_pomiar_nizszy": 4, "info_pomiar_wyzszy": 4,
    "standardowe": 5,
    "nieznany": 6, "brak_odczytu": 7, "brak_danych": 8,
}
RISK_LABEL = {
    "wysokie": "Wysokie ryzyko", "podwyzszone": "Podwyzszone ryzyko",
    "lekko podwyzszone": "Lekko podwyzszone", "lekko podwyzszone ryzyko niedoboru": "Lekko podwyzszone",
    "umiarkowane": "Umiarkowane", "nosiciel": "Nosiciel", "info": "Informacyjne",
    "info_pomiar_nizszy": "Mozliwy nizszy pomiar", "info_pomiar_wyzszy": "Mozliwy wyzszy pomiar",
    "standardowe": "Standardowe / typowe", "nieznany": "Nieopisany genotyp",
    "brak_odczytu": "Brak odczytu", "brak_danych": "Brak danych na chipie",
}
RISK_CLASS = {
    "wysokie": "risk-high", "podwyzszone": "risk-high",
    "lekko podwyzszone": "risk-mid", "lekko podwyzszone ryzyko niedoboru": "risk-mid",
    "umiarkowane": "risk-mid", "nosiciel": "risk-mid", "info": "risk-info",
    "info_pomiar_nizszy": "risk-info", "info_pomiar_wyzszy": "risk-info",
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
.standard-label{
  font-size: 11px; text-transform: uppercase; letter-spacing: .05em; color: var(--ink-soft);
  margin-top: 14px; margin-bottom: 6px;
}
.variant-list-compact{ display:flex; flex-direction:column; gap: 4px; }
.variant-standard{
  padding: 6px 12px; grid-template-columns: 1fr auto; align-items: center; gap: 8px;
}
.variant-standard .v-heading{ margin-bottom: 0; }
.variant-standard .v-name{ font-size: 12.5px; font-weight: 500; color: var(--ink-soft); }
.variant-standard .v-gene{ display: none; }
.variant-standard .v-side{ flex-direction: row; align-items: center; gap: 8px; }
.variant-standard .rsid{ display: none; }
.variant-standard .badge{ font-size: 10px; padding: 2px 7px; }
.variant-standard .genotype{ font-size: 11.5px; }
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

SEVERE_RISK = {"wysokie", "podwyzszone"}
STANDARD_RISK = {"standardowe", "nieznany"}
# wszystko inne (info, lekko podwyzszone, umiarkowane, nosiciel, info_pomiar_*, brak_odczytu) = "srednie"

def risk_tier(risk):
    if risk in SEVERE_RISK:
        return "severe"
    if risk in STANDARD_RISK:
        return "standard"
    return "medium"

def render_variant_row(r):
    risk = r["risk"]
    tier = risk_tier(risk)
    cls = RISK_CLASS.get(risk, "risk-muted")
    label = RISK_LABEL.get(risk, risk)
    genotype = r["genotype"] if r["genotype"] else "—"
    # powazne: pelny opis + notatka. srednie: sam opis (polowicznie). standardowe: bez opisu (krotko).
    desc = f'<div class="v-desc">{esc(r["desc"])}</div>' if tier != "standard" else ""
    note = f'<div class="v-note">{esc(r["note"])}</div>' if r.get("note") and tier == "severe" else ""
    return f'''
        <div class="variant variant-{tier}">
          <div class="v-main">
            <div class="v-heading">
              <span class="v-name">{esc(r["name"])}</span>
              <span class="v-gene">{esc(r["gene"])}</span>
            </div>
            {desc}
            {note}
          </div>
          <div class="v-side">
            <span class="badge {cls}">{esc(label)}</span>
            <span class="genotype">{esc(genotype)}</span>
            <span class="rsid">{esc(r["rsid"])}</span>
          </div>
        </div>'''

def render_category(cat, rows):
    severe = [r for r in rows if risk_tier(r["risk"]) == "severe"]
    medium = [r for r in rows if risk_tier(r["risk"]) == "medium"]
    standard = [r for r in rows if risk_tier(r["risk"]) == "standard"]
    for group in (severe, medium, standard):
        group.sort(key=lambda r: RISK_ORDER.get(r["risk"], 9))

    body = "\n".join(render_variant_row(r) for r in severe + medium)
    standard_body = "\n".join(render_variant_row(r) for r in standard)
    standard_block = (
        f'<div class="standard-label">Wyniki standardowe / typowe</div>'
        f'<div class="variant-list variant-list-compact">{standard_body}</div>'
    ) if standard else ""

    return f'''
      <section class="category">
        <h2>{esc(cat)}</h2>
        <div class="variant-list">
          {body}
        </div>
        {standard_block}
      </section>'''

def build_person_html(person, generated_date):
    name = person["name"]
    all_results = person["results"]
    apoe = person.get("apoe")

    untested_count = sum(1 for r in all_results if r["risk"] in ("brak_danych", "brak_odczytu"))
    results = [r for r in all_results if r["risk"] not in ("brak_danych", "brak_odczytu")]

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
        "Choroby metaboliczne", "Watroba / alkohol", "Dna moczanowa / stawy", "Kosci / stawy",
        "Tarczyca / autoimmunologia", "Nowotwory", "Wzrok", "Alergie / odpornosc", "Alergie / autoimmunologia",
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
      <span>Wariantow z wynikiem: {len(results)}</span>
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
    Raport wygenerowany lokalnie na podstawie surowych danych AncestryDNA — wylacznie do uzytku prywatnego/edukacyjnego.<br>
    {untested_count} wariantow z bazy pominieto w tym raporcie, bo nie sa mierzone na tym chipie (brak danych/no-call) — nie pokazujemy pustych wynikow.
  </footer>
</div>
</body>
</html>'''

SIMPLE_CSS = """
:root{
  --paper: #ffffff; --ink: #000000; --ink-soft: #333333; --line: #000000; --line-soft: #999999;
}
@media (prefers-color-scheme: dark){
  :root{ --paper:#000000; --ink:#ffffff; --ink-soft:#dddddd; --line:#ffffff; --line-soft:#888888; }
}
*{ box-sizing: border-box; }
body{
  margin:0; background: var(--paper); color: var(--ink);
  font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6; font-size: 17px;
}
.page{ max-width: 760px; margin: 0 auto; padding: 40px 30px 60px; }
.cover{ border-bottom: 3px solid var(--line); padding-bottom: 16px; margin-bottom: 8px; }
.cover h1{
  font-family: Georgia, "Iowan Old Style", serif; font-size: 34px; margin: 6px 0 4px;
}
.cover-sub{ color: var(--ink-soft); font-size: 15px; margin-bottom: 4px; letter-spacing: .03em; text-transform: uppercase; }
.intro{
  border: 2px solid var(--line); border-radius: 8px; padding: 18px 20px;
  font-size: 15.5px; margin: 24px 0 28px; line-height: 1.55;
}
.intro strong{ font-size: 16px; }
h2.sec-title{
  font-size: 22px; margin: 34px 0 14px; padding-bottom: 6px;
  border-bottom: 2px solid var(--line); display: flex; align-items: baseline; gap: 10px;
}
h2.sec-title .sec-icon{ font-size: 22px; }
.item{
  border: 1.5px solid var(--line); border-radius: 8px; padding: 16px 18px; margin-bottom: 14px;
  break-inside: avoid; position: relative;
}
/* rozroznienie sekcji BEZ koloru - poprzez styl/grubosc lewej krawedzi */
.item.sec-uwaga{ border-left: 8px double var(--line); }
.item.sec-lekarz{ border-left: 8px solid var(--line); }
.item.sec-styl{ border-left: 8px dashed var(--line); }
.item.sec-dobra{ border-left: 8px solid var(--line); border-style: solid; }
.item.sec-dobra:before{
  content: "✓"; position: absolute; top: 14px; right: 16px; font-size: 18px; font-weight: 700;
}
.item.sec-ciekaw{ border-left: 8px dotted var(--line); }
.item .item-head{ display:flex; align-items:center; gap:10px; margin-bottom: 6px; }
.item .icon{ font-size: 22px; }
.item .title{ font-weight: 700; font-size: 16.5px; color: var(--ink); }
.item .text{ font-size: 15.5px; color: var(--ink-soft); }
.item .extra{ font-size: 14px; color: var(--ink-soft); margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--line-soft); }
.item .extra-label{ font-weight: 700; color: var(--ink); }
.empty-note{ color: var(--ink-soft); font-style: italic; font-size: 14.5px; }
.footer-note{
  margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--line-soft);
  font-size: 13.5px; color: var(--ink-soft); line-height: 1.6;
}
@page{ size: A4; margin: 16mm 14mm; }
@media print{
  :root{ --paper:#fff; --ink:#000; --ink-soft:#222; --line:#000; --line-soft:#666; }
  body{ font-size: 14.5px; }
  .page{ max-width: none; padding: 0; }
}
"""

SECTION_META = {
    "uwaga": ("Na co warto zwrócić uwagę", "⚠️", "sec-uwaga"),
    "lekarz": ("Co warto powiedzieć lekarzowi lub farmaceucie", "💊", "sec-lekarz"),
    "styl_zycia": ("Styl życia i codzienne nawyki", "🍽️", "sec-styl"),
    "dobra_wiadomosc": ("Dobre wiadomości", "✅", "sec-dobra"),
    "ciekawostka": ("Ciekawostki", "✨", "sec-ciekaw"),
}

EXTRA_LABELS = {
    "origin": ("🌍", "Pochodzenie"),
    "diet": ("🍽️", "Dieta"),
    "body_mind": ("🧭", "Ciało / umysł / hobby"),
}

def render_extras(item):
    lines = []
    for key in ("origin", "diet", "body_mind"):
        if item.get(key):
            icon, label = EXTRA_LABELS[key]
            lines.append(f'<div class="extra"><span class="extra-label">{icon} {esc(label)}:</span> {esc(item[key])}</div>')
    return "\n".join(lines)

def build_simple_person_html(person, generated_date):
    name = person["name"]
    results_by_rsid = {r["rsid"]: r for r in person["results"]}
    apoe = person.get("apoe")

    buckets = {k: [] for k in SECTION_META}

    if apoe:
        interp = apoe["interpretation"]
        if "PODWYZSZONE" in interp:
            buckets["uwaga"].append({"icon": "🧠", "title": "Pamięć i mózg",
                "text": "Wyniki sugerują nieco wyższą genetyczną skłonność do problemów z pamięcią w starszym "
                "wieku. To NIE oznacza, że choroba na pewno wystąpi — to sygnał, żeby dodatkowo o mózg zadbać.",
                "diet": "Więcej warzyw, ryb, oliwy; mniej cukru i przetworzonego jedzenia (dieta śródziemnomorska ma tu najlepsze dowody naukowe).",
                "body_mind": "Regularne ćwiczenie umysłu (czytanie, krzyżówki, nauka nowych rzeczy) i codzienny ruch fizyczny razem dają najlepszy efekt ochronny."})
        elif "OBNIZONE" in interp:
            buckets["dobra_wiadomosc"].append({"icon": "🧠", "title": "Pamięć i mózg",
                "text": "Wyniki genetyczne związane z ryzykiem Alzheimera są korzystne — nie ma podwyższonego ryzyka związanego z tym konkretnym genem."})

    for adv in PLAIN_ADVICE:
        r = results_by_rsid.get(adv["rsid"])
        if not r:
            continue
        if r["risk"] not in adv.get("trigger_risks", []):
            continue
        item = {"icon": adv["icon"], "title": adv["title"], "text": adv["text"]}
        for key in ("origin", "diet", "body_mind"):
            if adv.get(key):
                item[key] = adv[key]
        buckets[adv["section"]].append(item)

    body_parts = []
    for key, (heading, sec_icon, css_class) in SECTION_META.items():
        items = buckets[key]
        if not items:
            continue
        rows = "\n".join(f'''
          <div class="item {css_class}">
            <div class="item-head">
              <span class="icon">{item["icon"]}</span>
              <span class="title">{esc(item["title"])}</span>
            </div>
            <div class="text">{esc(item["text"])}</div>
            {render_extras(item)}
          </div>''' for item in items)
        body_parts.append(f'<h2 class="sec-title"><span class="sec-icon">{sec_icon}</span>{esc(heading)}</h2>\n{rows}')

    if not body_parts:
        body_parts.append('<p class="empty-note">Dla dostępnych danych nie znaleziono punktów wymagających uwagi w tej uproszczonej wersji — sprawdź pełny raport szczegółowy.</p>')

    content = "\n".join(body_parts)
    synthesis = render_synthesis(buckets)

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
    To Twoje wyniki DNA po ludzku — bez trudnych słów. Zebraliśmy z Twojego testu to, co
    naprawdę warto wiedzieć: na co uważać, co powiedzieć lekarzowi i co możesz zacząć robić
    już dziś, żeby czuć się lepiej i żyć dłużej w dobrym zdrowiu. Geny to nie wyrok — to
    najczęściej niewielkie przechylenie szali, na które masz realny wpływ przez to, co jesz,
    ile się ruszasz i jak dbasz o siebie. Ten dokument to nie straszenie, tylko konkretna,
    dobra wiadomość: wiesz już, na czym się skupić.
  </div>

  {content}

  {synthesis}

  <div class="footer-note">
    Pełny, szczegółowy raport techniczny (z nazwami genów i wynikami badań naukowych)
    znajduje się w osobnym pliku — dla tych, którzy chcą zobaczyć wszystkie szczegóły.
    Ten dokument to jego uproszczona wersja, przygotowana z myślą o łatwym wydruku na
    kartce A4 i czytelności dla każdego, niezależnie od wiedzy o genetyce.
  </div>
</div>
</body>
</html>'''

def render_synthesis(buckets):
    all_items = buckets["uwaga"] + buckets["lekarz"] + buckets["styl_zycia"] + buckets["dobra_wiadomosc"] + buckets["ciekawostka"]

    diet_bits = [(it["title"], it["diet"]) for it in all_items if it.get("diet")]
    body_bits = [(it["title"], it["body_mind"]) for it in all_items if it.get("body_mind")]
    uwaga_titles = [it["title"] for it in buckets["uwaga"]]

    def render_bits(bits):
        return "\n".join(
            f'<div class="text"><strong>{esc(title)}:</strong> {esc(text)}</div>'
            for title, text in bits
        )

    if diet_bits:
        food_body = render_bits(diet_bits)
        food_intro = "Konkretnie z Twoich wyników wynika:"
    else:
        food_body = ('<div class="text">Więcej warzyw, ryb, oliwy i pełnoziarnistych produktów; '
                     'mniej cukru, słodkich napojów i wysoko przetworzonego jedzenia.</div>')
        food_intro = "Żaden z Twoich wyników nie wskazuje tu na nic szczególnego, więc uniwersalna zasada:"

    if body_bits:
        body_body = render_bits(body_bits)
        body_intro = "Konkretnie z Twoich wyników wynika:"
    else:
        body_body = ('<div class="text">Codzienny spacer (nawet 20-30 minut) daje więcej korzyści '
                     'zdrowotnych niż większość suplementów razem wziętych.</div>')
        body_intro = "Żaden z Twoich wyników nie wskazuje tu na nic szczególnego, więc uniwersalna zasada:"

    uwaga_line = ""
    if uwaga_titles:
        uwaga_line = (
            '<div class="item sec-lekarz"><div class="text"><strong>Priorytet numer jeden z Twoich wyników:</strong> '
            + esc(", ".join(uwaga_titles)) + ' — to punkty z sekcji "Na co warto zwrócić uwagę" wyżej, '
            'które najbardziej opłaca się przełożyć na konkretne działanie.</div></div>'
        )

    return f'''
  <h2 class="sec-title"><span class="sec-icon">🌿</span>Jak żyć długo, spokojnie i w zdrowiu — na podstawie Twoich wyników</h2>
  {uwaga_line}
  <div class="item sec-styl">
    <div class="item-head"><span class="icon">🥗</span><span class="title">Jedzenie</span></div>
    <div class="text" style="margin-bottom:6px;"><em>{food_intro}</em></div>
    {food_body}
  </div>
  <div class="item sec-styl">
    <div class="item-head"><span class="icon">🚶</span><span class="title">Ruch, ciało i temperament</span></div>
    <div class="text" style="margin-bottom:6px;"><em>{body_intro}</em></div>
    {body_body}
  </div>
  <div class="item sec-styl">
    <div class="item-head"><span class="icon">😴</span><span class="title">Sen i spokój</span></div>
    <div class="text">Regularne godziny snu (7-8h) i mniej stresu to jedne z najlepiej
    potwierdzonych czynników długowieczności — niezależnie od wyniku DNA, to jedna z najlepszych
    inwestycji w zdrowie jaką można zrobić.</div>
  </div>
  <div class="item sec-dobra">
    <div class="item-head"><span class="icon">👨‍👩‍👧‍👦</span><span class="title">Rozmowa z bliskimi</span></div>
    <div class="text">Bliskie relacje i rozmowa to jeden z najsilniej potwierdzonych czynników długiego
    życia. Czasem warto wprost porozmawiać o tym, co komu pomaga się dobrze czuć (np. czy ktoś lepiej
    funkcjonuje w spokoju, a ktoś w ruchu i zmianie, patrz sekcja "Ruch, ciało i temperament" powyżej)
    — to ułatwia wzajemne zrozumienie, a nie jest niczyją "winą".</div>
  </div>
  <p style="font-size:14px; font-style:italic; margin-top:16px;">
    Nawet niewielka, ale trwała zmiana jednego nawyku — więcej ruchu, mniej cukru, regularny
    sen — realnie się liczy. Nie trzeba zmieniać wszystkiego naraz.
  </p>'''

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
