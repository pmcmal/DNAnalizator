# DNAnalizator

<details>
<summary><strong>🇬🇧 English</strong> (click to expand)</summary>

<br>

A local tool for analyzing raw DNA data from consumer tests (AncestryDNA/23andMe)
against a curated set of well-documented, research-backed variants related to
health, pharmacogenomics, physical traits, and lifestyle.

Generates a clean HTML report (ready to print/save as PDF from the browser)
for each analyzed person.

## ⚠️ Disclaimer

**This tool is NOT medical diagnostics.** Most of the described variants are
statistical risk factors with small to moderate effect sizes, based on
published population studies (GWAS, PharmGKB, ClinVar, peer-reviewed literature
including Nature/Nature Genetics/Science/PNAS). A genotype is not a sentence —
most traits described here are highly polygenic and modified by lifestyle.
Results do not replace medical consultation or genetic testing performed in a
clinical setting by a certified laboratory.

## 🔒 Privacy

Raw DNA data and generated reports are personal data (in this case also health
data) — **never commit them to the repository**, especially a public one.
This repo's `.gitignore` excludes by default:

- `*.zip` (downloaded AncestryDNA/23andMe archives)
- `mama/`, `tata/` (folders with unpacked raw data)
- `report_data.json`, `raport_*.html` (generated results)

Keep your DNA data and generated reports strictly local.

## How it works

1. **Input**: a raw `AncestryDNA.txt` file (rsid / chromosome / position / allele1 / allele2).
2. **`variants_db.py`**: a hand-curated database of known SNPs with
   descriptions, grouped into categories (neurodegenerative diseases,
   cardiovascular, metabolic, cancer, addictions, pharmacogenomics, physical
   traits, sleep, longevity, and more).
3. **`analyze.py`**: parses the raw data, matches genotypes against the
   database (handling opposite-strand reads), and writes the result to
   `report_data.json`.
4. **`build_report.py`**: generates a readable, printable HTML report per
   person from the data (`raport_<person>.html`).

## Usage

```bash
# 1. Unzip the downloaded AncestryDNA archive into a folder, e.g. mama/ and tata/
unzip dna-data-*.zip -d mama

# 2. Run the analysis (edit the list of people/paths in analyze.py if needed)
python analyze.py

# 3. Generate the HTML reports
python build_report.py

# 4. Open raport_<person>.html in a browser and use Ctrl+P -> Save as PDF
```

## Confidence levels

Every variant in the database has context attached via the `note` field —
some are very well and repeatedly replicated effects (e.g. APOE/Alzheimer's,
Factor V Leiden, eye color, MC1R), while others are curiosities with
weaker/inconsistent replication (explicitly flagged in the description).
Treat `note` as information about the strength of evidence, not just extra
context.

## Extending the variant database

To add a new variant, append an entry to the `VARIANTS` list in `variants_db.py`:

```python
{
    "rsid": "rsXXXXXXX", "gene": "GENE_NAME", "category": "Category",
    "name": "Short variant description",
    "genotypes": {
        "AA": ("risk_level", "description for this genotype"),
        ...
    },
    "note": "Context / strength of evidence / source"
}
```

</details>

<details open>
<summary><strong>🇵🇱 Polski</strong> (kliknij, aby zwinąć)</summary>

<br>

Lokalne narzędzie do analizy surowych danych DNA z testów typu AncestryDNA/23andMe
pod kątem dobrze udokumentowanych w literaturze naukowej wariantów związanych ze
zdrowiem, farmakogenomiką, cechami fizycznymi i stylem życia.

Generuje czytelny raport HTML (gotowy do wydruku/zapisu jako PDF z przeglądarki)
dla każdej analizowanej osoby.

## ⚠️ Zastrzeżenie

**To narzędzie NIE jest diagnostyką medyczną.** Większość opisanych wariantów to
statystyczne czynniki ryzyka o niewielkim lub umiarkowanym wpływie, oparte na
publikowanych badaniach populacyjnych (GWAS, PharmGKB, ClinVar, recenzowana
literatura naukowa, m.in. Nature/Nature Genetics/Science/PNAS). Genotyp to nie
wyrok — większość opisanych tu cech jest silnie poligenowa i modyfikowana przez
styl życia. Wyniki nie zastępują konsultacji lekarskiej ani badania genetycznego
wykonanego w warunkach klinicznych z certyfikowanego laboratorium.

## 🔒 Prywatność

Surowe dane DNA i wygenerowane raporty to dane osobowe (a w tym wypadku również
dane o stanie zdrowia) — **nigdy nie commituj ich do repozytorium**, zwłaszcza
publicznego. `.gitignore` w tym repo domyślnie wyklucza:

- `*.zip` (pobrane archiwa z AncestryDNA/23andMe)
- `mama/`, `tata/` (foldery z rozpakowanymi danymi surowymi)
- `report_data.json`, `raport_*.html` (wygenerowane wyniki)

Trzymaj swoje dane DNA i wygenerowane raporty wyłącznie lokalnie.

## Jak to działa

1. **Wejście**: surowy plik `AncestryDNA.txt` (rsid / chromosom / pozycja / allele1 / allele2).
2. **`variants_db.py`**: ręcznie dobrana baza znanych wariantów (SNP) z opisem,
   pogrupowana w kategorie (choroby neurodegeneracyjne, sercowo-naczyniowe,
   metaboliczne, nowotwory, uzależnienia, farmakogenomika, cechy fizyczne, sen,
   długowieczność i inne).
3. **`analyze.py`**: parsuje dane, dopasowuje genotypy do bazy (z obsługą
   odczytu na przeciwnej nici DNA), zapisuje wynik do `report_data.json`.
4. **`build_report.py`**: generuje z danych czytelny, drukowalny raport HTML
   per osoba (`raport_<osoba>.html`).

## Użycie

```bash
# 1. Rozpakuj pobrane archiwum AncestryDNA do folderu np. mama/ i tata/
unzip dna-data-*.zip -d mama

# 2. Uruchom analizę (edytuj listę osób/ścieżek w analyze.py jeśli trzeba)
python analyze.py

# 3. Wygeneruj raporty HTML
python build_report.py

# 4. Otwórz raport_<osoba>.html w przeglądarce i użyj Ctrl+P -> Zapisz jako PDF
```

## Poziomy pewności

Każdy wariant w bazie ma przypisany kontekst w polu `note` — część to bardzo
dobrze i wielokrotnie replikowane efekty (np. APOE/Alzheimer, Factor V Leiden,
kolor oczu, MC1R), a część to ciekawostki o słabszej/niespójnej replikacji
(zaznaczone wprost w opisie). Traktuj `note` jako informację o sile dowodów,
nie tylko dodatkowy kontekst.

## Rozszerzanie bazy wariantów

Aby dodać nowy wariant, dopisz wpis do listy `VARIANTS` w `variants_db.py`:

```python
{
    "rsid": "rsXXXXXXX", "gene": "NAZWA_GENU", "category": "Kategoria",
    "name": "Krotki opis wariantu",
    "genotypes": {
        "AA": ("poziom_ryzyka", "opis dla tego genotypu"),
        ...
    },
    "note": "Kontekst / sila dowodow / zrodlo"
}
```

</details>
