# DNAnalizator

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
