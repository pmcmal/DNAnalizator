# -*- coding: utf-8 -*-
"""
Baza dobrze udokumentowanych wariantow SNP o znaczeniu zdrowotnym/farmakogenomicznym/cechowym.
Zrodla: literatura naukowa (GWAS Catalog, PharmGKB, ClinVar, SNPedia - konsensus publiczny).
UWAGA: To NIE jest narzedzie diagnostyczne. Wiekszosc wariantow to czynniki ryzyka
o niewielkim/umiarkowanym efekcie, nie determinuja choroby.

Struktura kazdego wpisu:
  rsid: identyfikator SNP
  gene: gen / region
  category: kategoria
  name: krotki opis
  genotypes: dict genotyp(posortowany) -> (poziom_ryzyka, opis)
  note: dodatkowy kontekst
"""

VARIANTS = [
    # ---------------- CHOROBY NEURODEGENERACYJNE ----------------
    {
        "rsid": "rs429358", "gene": "APOE", "category": "Choroby neurodegeneracyjne",
        "name": "APOE - allel e4 (czesc 1/2, patrz tez rs7412) - ryzyko Alzheimera",
        "genotypes": {
            "CC": ("podwyzszone", "Prawdopodobny nosiciel APOE e4/e4 lub e4/e3 - wymaga polaczenia z rs7412 dla pelnej interpretacji"),
            "CT": ("umiarkowane", "Jedna kopia allelu zwiazanego z e4 - wymaga rs7412 do pelnej interpretacji"),
            "TT": ("standardowe", "Brak allelu C - nie jest to e4 (przy zalozeniu typowego ukladu z rs7412)"),
        },
        "note": "Interpretacja APOE wymaga LACZNEGO odczytu rs429358 + rs7412 (patrz apoe_combo w raporcie). Samo rs429358=T i rs7412=T zwykle oznacza e3/e3 (najczestszy, neutralny genotyp)."
    },
    {
        "rsid": "rs7412", "gene": "APOE", "category": "Choroby neurodegeneracyjne",
        "name": "APOE - allel e2 (czesc 2/2, patrz rs429358) - ryzyko Alzheimera",
        "genotypes": {
            "CC": ("info", "Brak allelu e2 (T) - patrz interpretacja laczna APOE"),
            "CT": ("info", "Jedna kopia allelu zwiazanego z e2 (dzialanie ochronne na ryzyko Alzheimera) - patrz interpretacja laczna"),
            "TT": ("info", "Homozygota e2/e2 (rzadkie) - patrz interpretacja laczna, moze wiazac sie z hiperlipoproteinemia typu III"),
        },
        "note": "Patrz rs429358."
    },

    {
        "rsid": "rs4420638", "gene": "APOC1 (ok. 11kb od APOE)", "category": "Choroby neurodegeneracyjne",
        "name": "Poszlakowy marker w regionie APOE (NIE bezposredni test e4!) - Alzheimer / cholesterol",
        "genotypes": {
            "AA": ("info", "Allel A (obie kopie) czesciej wspolwystepuje z BRAKIEM APOE e4 (czyli e2/e2, e2/e3 lub e3/e3) - uspokajajacy sygnal, ale to tylko poszlaka, nie bezposredni wynik APOE"),
            "AG": ("info", "Uklad mieszany - bardzo niepewny sygnal co do APOE e4, nie da sie na tej podstawie sensownie nic wywnioskowac"),
            "GG": ("umiarkowane", "Allel G (obie kopie) czesciej wspolwystepuje z OBECNOSCIA APOE e4 - ALE nawet przy tym wyniku szansa na faktyczne posiadanie e4 to w badaniach ok. 50%, czyli w przyblizeniu rzut moneta - to ZDECYDOWANIE nie jest wynik diagnostyczny"),
        },
        "note": "WAZNE OGRANICZENIE: ten SNP lezy w genie APOC1, ok. 11 tys. par zasad od APOE. Bywa uzywany w literaturze (i przez stare chipy 23andMe) jako przyblizony marker sprzezenia (LD) z APOE e4, poniewaz AncestryDNA od 2017 roku NIE testuje bezposrednio rs429358/rs7412 potrzebnych do ustalenia e2/e3/e4 (patrz wyzej - brak danych). Zwiazek tego SNP z Alzheimerem wynika WYLACZNIE z powiazania z APOE, a wedlug SNPedia nawet przy 'obciazonym' genotypie GG szansa na faktyczne posiadanie e4 to ok. 50% - zbyt niepewne, by na tym budowac jakiekolwiek decyzje zdrowotne. Jesli zalezy Ci na prawdziwym wyniku APOE: (1) test 23andMe (nowsze chipy testuja obie pozycje bezposrednio), (2) darmowa imputacja danych AncestryDNA przez serwisy jak NutraHacker lub ADNTRO (uzywaja statystycznych paneli referencyjnych, nie zgadywania z sasiedztwa) - pamietaj, ze wyslanie danych DNA bliskiej osoby do zewnetrznego serwisu to swiadoma decyzja o prywatnosci."
    },

    # ---------------- ZAKRZEPICA / SERCE ----------------
    {
        "rsid": "rs6025", "gene": "F5 (Czynnik V Leiden)", "category": "Zakrzepica / uklad krazenia",
        "name": "Czynnik V Leiden - ryzyko zakrzepicy zylnej",
        "genotypes": {
            "GG": ("standardowe", "Brak mutacji Leiden - typowe ryzyko zakrzepicy"),
            "GA": ("podwyzszone", "Nosiciel jednej kopii Factor V Leiden - ok. 3-8x wyzsze ryzyko zylnej choroby zakrzepowo-zatorowej"),
            "AA": ("wysokie", "Homozygota Factor V Leiden - istotnie podwyzszone ryzyko zakrzepicy zylnej, warto skonsultowac z hematologiem zwlaszcza przed operacjami/dluga podroza/HTZ"),
        },
        "note": "Jeden z najsilniejszych i najlepiej potwierdzonych czynnikow genetycznych zakrzepicy zylnej."
    },
    {
        "rsid": "rs1799963", "gene": "F2 (Protrombina G20210A)", "category": "Zakrzepica / uklad krazenia",
        "name": "Mutacja protrombiny - ryzyko zakrzepicy",
        "genotypes": {
            "GG": ("standardowe", "Brak mutacji - typowe ryzyko"),
            "GA": ("podwyzszone", "Nosiciel wariantu protrombiny - podwyzszone ryzyko zakrzepicy zylnej"),
            "AA": ("wysokie", "Homozygota - znaczaco podwyzszone ryzyko zakrzepicy"),
        },
        "note": "Czesto sprawdzany razem z Factor V Leiden."
    },
    {
        "rsid": "rs9923231", "gene": "VKORC1", "category": "Farmakogenomika",
        "name": "Wrazliwosc na warfaryne (lek przeciwzakrzepowy)",
        "genotypes": {
            "CC": ("info", "Typowa wrazliwosc na warfaryne, standardowe dawkowanie"),
            "CT": ("info", "Zwiekszona wrazliwosc - moze wymagac nizszej dawki warfaryny"),
            "TT": ("info", "Wysoka wrazliwosc na warfaryne - istotnie nizsza dawka poczatkowa zalecana, koniecznie poinformowac lekarza przy wdrazaniu leczenia"),
        },
        "note": "Wazne przy ewentualnym leczeniu warfaryna - warto pokazac lekarzowi."
    },
    {
        "rsid": "rs1801133", "gene": "MTHFR C677T", "category": "Metabolizm / serce",
        "name": "MTHFR C677T - metabolizm kwasu foliowego, homocysteina",
        "genotypes": {
            "GG": ("standardowe", "Prawidlowa aktywnosc enzymu MTHFR"),
            "GA": ("lekko podwyzszone", "Ok. 65% normalnej aktywnosci enzymu - zwykle bez klinicznego znaczenia"),
            "AA": ("podwyzszone", "Ok. 30% normalnej aktywnosci enzymu - podwyzszony poziom homocysteiny mozliwy, rozwazyc suplementacje aktywnym folianem (metylofolian) zamiast kwasu foliowego, warto omowic z lekarzem zwlaszcza przy planowaniu ciazy"),
        },
        "note": "Bardzo popularny wariant, szeroko badany ale efekt kliniczny czesto przeceniany w internecie - nie jest to choroba, tylko wariant metabolizmu. DODATKOWO (zweryfikowane, lipiec 2026): kontrolowane badanie kliniczne (McNulty i wsp., Circulation 2006) wykazalo, ze TYLKO homozygoty AA (dwie kopie wariantu, ~30% aktywnosci enzymu) odpowiadaja na suplementacje ryboflawiny (witamina B2, ok. 1.6mg/dz.) spadkiem homocysteiny (nawet do -22-40%) - u osob GG i GA (jedna kopia) suplementacja B2 nie dala efektu w tym badaniu. Ryboflawina jest kofaktorem samego enzymu MTHFR, wiec ma to sens biochemicznie, ale dotyczy WYLACZNIE genotypu AA - u nosicieli jednej kopii (GA) nie ma podstaw, by spodziewac sie tego samego efektu."
    },
    {
        "rsid": "rs1801131", "gene": "MTHFR A1298C", "category": "Metabolizm / serce",
        "name": "MTHFR A1298C - metabolizm kwasu foliowego",
        "genotypes": {
            "TT": ("standardowe", "Prawidlowa aktywnosc"),
            "TG": ("info", "Nosiciel jednej kopii - zwykle bez znaczenia klinicznego samodzielnie"),
            "GG": ("info", "Dwie kopie - w polaczeniu z rs1801133 moze dodatkowo obnizac aktywnosc enzymu"),
        },
        "note": "Ocenia sie zwykle razem z rs1801133 (C677T)."
    },

    # ---------------- HEMOCHROMATOZA / METABOLIZM ZELAZA ----------------
    {
        "rsid": "rs1800562", "gene": "HFE C282Y", "category": "Choroby metaboliczne",
        "name": "Hemochromatoza dziedziczna (nadmiar zelaza)",
        "genotypes": {
            "GG": ("standardowe", "Brak mutacji C282Y"),
            "GA": ("nosiciel", "Nosiciel jednej kopii - zwykle bez objawow, niewielkie podwyzszenie ryzyka przeciazenia zelazem"),
            "AA": ("wysokie", "Homozygota C282Y/C282Y - najczestsza przyczyna genetyczna hemochromatozy w populacjach europejskich, warto sprawdzic poziom ferrytyny/zelaza we krwi, badanie penetracji jest niepelne (nie kazdy homozygota rozwija objawy)"),
        },
        "note": "Jeden z niewielu wariantow o realnym znaczeniu klinicznym mozliwym do sprawdzenia badaniem krwi (ferrytyna, TIBC)."
    },
    {
        "rsid": "rs1799945", "gene": "HFE H63D", "category": "Choroby metaboliczne",
        "name": "Hemochromatoza dziedziczna - drugi wariant HFE",
        "genotypes": {
            "CC": ("standardowe", "Brak mutacji H63D"),
            "CG": ("nosiciel", "Nosiciel - samo w sobie niskie ryzyko, ale w polaczeniu z C282Y (rs1800562) moze zwiekszac ryzyko"),
            "GG": ("podwyzszone", "Homozygota H63D/H63D - lagodniejsza forma, zwykle niski dodatkowy wzrost ryzyka"),
        },
        "note": "Ocenia sie razem z rs1800562."
    },

    # ---------------- NOWOTWORY ----------------
    {
        "rsid": "rs80357906", "gene": "BRCA1 (proxy, rzadko na chipach)", "category": "Nowotwory",
        "name": "BRCA1 - wariant zwiazany z rakiem piersi/jajnika",
        "genotypes": {},
        "note": "Testy typu AncestryDNA/23andMe zwykle NIE pokrywaja klinicznie istotnych mutacji BRCA1/2 (w tym trzech zalozycielskich wariantow aszkenazyjskich) - ten wpis jest informacyjny; jesli w rodzinie wystepowal rak piersi/jajnika/prostaty w mlodym wieku, rozwazcie panel genetyczny w poradni onkologicznej, nie surowe dane z testu rekreacyjnego."
    },

    # ---------------- ALKOHOL / UZALEZNIENIA ----------------
    {
        "rsid": "rs671", "gene": "ALDH2", "category": "Metabolizm alkoholu / reakcje",
        "name": "Reakcja \"Asian flush\" na alkohol / metabolizm aldehydu octowego",
        "genotypes": {
            "GG": ("standardowe", "Prawidlowy metabolizm aldehydu octowego"),
            "GA": ("info", "Czesciowy deficyt ALDH2 - typowe zaczerwienienie twarzy, kolatanie serca po alkoholu, wiaze sie tez z mniejszym ryzykiem naduzywania alkoholu ale WYZSZYM ryzykiem raka przelyku przy regularnym piciu"),
            "AA": ("info", "Calkowity deficyt ALDH2 - silna reakcja na alkohol (nudnosci, zaczerwienienie), zdecydowanie odradzane regularne picie ze wzgledu na ryzyko nowotworu przelyku"),
        },
        "note": "Wariant bardzo rzadki w populacji polskiej/europejskiej (typowy dla Azji Wschodniej), ale warto sprawdzic."
    },
    {
        "rsid": "rs1229984", "gene": "ADH1B", "category": "Metabolizm alkoholu / uzaleznienia",
        "name": "Szybkosc metabolizmu alkoholu do aldehydu octowego",
        "genotypes": {
            "GG": ("standardowe", "Typowe tempo metabolizmu etanolu"),
            "GA": ("info", "Szybszy metabolizm etanolu do (nieprzyjemnego) aldehydu octowego - wiaze sie ze statystycznie nizszym ryzykiem uzaleznienia od alkoholu"),
            "AA": ("info", "Bardzo szybki metabolizm - silny efekt ochronny przed alkoholizmem opisywany w literaturze"),
        },
        "note": "Jeden z najlepiej potwierdzonych wariantow zwiazanych (odwrotnie) z ryzykiem uzaleznienia od alkoholu."
    },
    {
        "rsid": "rs16969968", "gene": "CHRNA5", "category": "Uzaleznienia",
        "name": "Podatnosc na uzaleznienie od nikotyny / intensywnosc palenia",
        "genotypes": {
            "GG": ("standardowe", "Typowe ryzyko"),
            "GA": ("lekko podwyzszone", "Nosiciel - opisywany zwiazek z wieksza liczba wypalanych papierosow u osob palacych"),
            "AA": ("podwyzszone", "Homozygota - najsilniej opisywany w literaturze wariant zwiazany z intensywnoscia nikotynizmu i ryzykiem raka pluc u palaczy (dziala TYLKO w kontekscie palenia)"),
        },
        "note": "Efekt widoczny tylko u osob palacych - nie zwieksza ryzyka samego w sobie bez ekspozycji na nikotyne."
    },
    {
        "rsid": "rs1799971", "gene": "OPRM1", "category": "Uzaleznienia",
        "name": "Receptor opioidowy mu - wrazliwosc na opioidy/ich efekt nagrody",
        "genotypes": {
            "AA": ("standardowe", "Typowa wrazliwosc na opioidy"),
            "AG": ("info", "Allel G (Asp40) - w badaniach zwiazany z odmiennym odczuwaniem nagrody/bolu przy opioidach, moze wplywac na dawkowanie lekow przeciwbolowych"),
            "GG": ("info", "Homozygota G - podobnie jak wyzej, silniejszy efekt"),
        },
        "note": "Efekty niespojne miedzy badaniami, traktowac jako ciekawostke, nie regule kliniczna."
    },

    # ---------------- CUKRZYCA / METABOLIZM ----------------
    {
        "rsid": "rs7903146", "gene": "TCF7L2", "category": "Cukrzyca / metabolizm",
        "name": "Najsilniejszy powszechny wariant ryzyka cukrzycy typu 2",
        "genotypes": {
            "CC": ("standardowe", "Typowe ryzyko cukrzycy typu 2"),
            "CT": ("podwyzszone", "Ok. 1.4x wyzsze ryzyko cukrzycy typu 2 w porownaniu do CC"),
            "TT": ("wysokie", "Ok. 2x wyzsze ryzyko cukrzycy typu 2 - warto dbac o dieta/aktywnosc fizyczna i regularne badania glukozy, ale to nadal tylko jeden z wielu czynnikow (poligenowa choroba)"),
        },
        "note": "Najsilniejszy pojedynczy powszechny SNP zwiazany z cukrzyca typu 2, ale sama choroba jest silnie poligenowa i zalezna od stylu zycia."
    },
    {
        "rsid": "rs9939609", "gene": "FTO", "category": "Cukrzyca / metabolizm",
        "name": "Wariant FTO - predyspozycja do otylosci",
        "genotypes": {
            "TT": ("standardowe", "Typowe ryzyko masy ciala"),
            "AT": ("lekko podwyzszone", "Nosiciel - ok. 1.3x wyzsze ryzyko otylosci, sredni wzrost masy ciala ok. 1.5 kg"),
            "AA": ("podwyzszone", "Homozygota - ok. 1.7x wyzsze ryzyko otylosci, sredni wzrost masy ciala ok. 3 kg w badaniach populacyjnych; efekt niwelowany przez regularna aktywnosc fizyczna"),
        },
        "note": "Efekt niewielki i mocno modyfikowany przez styl zycia."
    },

    # ---------------- CELIAKIA / ALERGIE ----------------
    {
        "rsid": "rs2187668", "gene": "HLA-DQ2.5 (proxy)", "category": "Alergie / autoimmunologia",
        "name": "Predyspozycja HLA do celiakii",
        "genotypes": {
            "TT": ("info", "Brak charakterystycznego allelu ryzyka w tym proxy"),
            "CT": ("info", "Nosiciel jednej kopii - obecnosc allelu HLA-DQ2.5 zwiazanego z celiakia (ale wiekszosc nosicieli NIGDY nie rozwija celiakii)"),
            "CC": ("podwyzszone", "Homozygota - wyzsza predyspozycja HLA do celiakii, ale to warunek konieczny nie wystarczajacy - rozwoj choroby wymaga dodatkowych czynnikow"),
        },
        "note": "HLA-DQ2/DQ8 to marker podatnosci, nie diagnoza - >99% nosicieli nigdy nie zachoruje na celiakie."
    },

    # ---------------- CECHY / NIETOLERANCJE ----------------
    {
        "rsid": "rs4988235", "gene": "MCM6/LCT", "category": "Cechy / nietolerancje",
        "name": "Tolerancja laktozy w wieku doroslym",
        "genotypes": {
            "TT": ("info", "Prawdopodobna tolerancja laktozy w wieku doroslym (persystencja laktazy)"),
            "CT": ("info", "Prawdopodobna tolerancja laktozy (allel dominujacy)"),
            "CC": ("info", "Prawdopodobna nietolerancja laktozy w wieku doroslym (typowy wzorzec dla wiekszosci ludzi na swiecie, mniej powszechny w Europie Polnocnej)"),
        },
        "note": "Jeden z najlepiej potwierdzonych wariantow cech w genetyce populacyjnej."
    },
    {
        "rsid": "rs713598", "gene": "TAS2R38", "category": "Cechy / nietolerancje",
        "name": "Odczuwanie goryczy (PTC/PROP - np. w brukselce, kapuscie)",
        "genotypes": {
            "CC": ("info", "Prawdopodobnie 'super-taster' - silne wyczuwanie goryczy"),
            "CG": ("info", "Posrednia wrazliwosc na gorzki smak"),
            "GG": ("info", "Prawdopodobnie slabe wyczuwanie goryczy PTC"),
        },
        "note": "Cecha neutralna zdrowotnie, ciekawostka."
    },
    {
        "rsid": "rs762551", "gene": "CYP1A2", "category": "Farmakogenomika",
        "name": "Szybkosc metabolizmu kofeiny",
        "genotypes": {
            "AA": ("info", "Szybki metabolizer kofeiny - kawa metabolizowana szybciej, mniejsze ryzyko dzialan niepozadanych przy wiekszym spozyciu"),
            "AC": ("info", "Posredni/wolniejszy metabolizm kofeiny - warto ograniczac ilosc kawy, zwlaszcza wieczorem"),
            "CC": ("info", "Wolny metabolizer kofeiny - kofeina dluzej we krwi, wyzsze opisywane ryzyko nadcisnienia/zawalu przy duzym spozyciu kawy, warto ograniczyc kawe"),
        },
        "note": "Popularny i dobrze powtarzalny wariant farmakogenomiczny."
    },
    {
        "rsid": "rs1800497", "gene": "ANKK1/DRD2 (TaqIA)", "category": "Uzaleznienia / neurologia",
        "name": "Gestosc receptorow dopaminowych D2 - powiazania z uzaleznieniami/ADHD w badaniach",
        "genotypes": {
            "GG": ("standardowe", "Typowa gestosc receptorow D2 (allel A2/A2)"),
            "AG": ("info", "Nosiciel allelu A1 - w niektorych badaniach zwiazany z nizsza gestoscia receptorow D2 i wyzszym opisywanym ryzykiem uzaleznien/ADHD, wyniki niespojne miedzy badaniami"),
            "AA": ("info", "Homozygota A1/A1 - jw., efekt silniejszy w niektorych badaniach, ale wyniki replikacji sa mieszane"),
        },
        "note": "WAZNE ZASTRZEZENIE: zwiazek z ADHD/uzaleznieniami jest slabo i niespojnie replikowany w nowszych, wiekszych badaniach GWAS. Traktowac wylacznie jako ciekawostke, nie wskaznik diagnostyczny."
    },
    {
        "rsid": "rs4680", "gene": "COMT (Val158Met)", "category": "Neurologia / metabolizm",
        "name": "COMT - metabolizm dopaminy w korze przedczolowej ('wojownik vs. martwiacy sie')",
        "genotypes": {
            "GG": ("info", "Val/Val - szybszy rozklad dopaminy w korze przedczolowej, opisywane jako typ 'wojownik' (lepsza odpornosc na stres, czasem gorsza wydajnosc poznawcza w spokoju)"),
            "AG": ("info", "Genotyp posredni Val/Met"),
            "AA": ("info", "Met/Met - wolniejszy rozklad dopaminy, opisywane jako typ 'martwiacy sie' (lepsza wydajnosc poznawcza w spokoju, wieksza wrazliwosc na stres/bol)"),
        },
        "note": "Popularny w popularnonaukowych opisach, efekty realne ale niewielkie i silnie zalezne od kontekstu."
    },

    # ---------------- STATYNY / LEKI ----------------
    {
        "rsid": "rs4149056", "gene": "SLCO1B1", "category": "Farmakogenomika",
        "name": "Ryzyko dzialan niepozadanych (bole miesni) przy statynach (np. simwastatyna)",
        "genotypes": {
            "TT": ("standardowe", "Typowe ryzyko miopatii przy statynach"),
            "CT": ("podwyzszone", "Umiarkowanie podwyzszone ryzyko miopatii zwiazanej ze statynami (zwlaszcza simwastatyna w wyzszych dawkach) - warto wspomniec lekarzowi przy przepisywaniu statyn"),
            "CC": ("wysokie", "Znaczaco podwyzszone ryzyko miopatii/rabdomiolizy przy statynach, szczegolnie simwastatynie - istotna informacja dla lekarza prowadzacego przy doborze leku/dawki"),
        },
        "note": "Uznawany przez CPIC/PharmGKB wariant o realnym znaczeniu klinicznym przy leczeniu statynami."
    },
    {
        "rsid": "rs1057910", "gene": "CYP2C9*3", "category": "Farmakogenomika",
        "name": "Metabolizm lekow przez CYP2C9 (warfaryna, NLPZ, niektore leki przeciwpadaczkowe)",
        "genotypes": {
            "AA": ("standardowe", "Prawidlowy metabolizm CYP2C9"),
            "AC": ("info", "Posredni metabolizer - mozliwa zwiekszona wrazliwosc na niektore leki (np. warfaryna, fenytoina, NLPZ)"),
            "CC": ("info", "Wolny metabolizer CYP2C9 - istotnie zmieniony metabolizm wielu lekow, warto poinformowac lekarza/farmaceute"),
        },
        "note": "Czesto oceniany razem z VKORC1 (rs9923231) przy dawkowaniu warfaryny."
    },

    # ---------------- WYDOLNOSC FIZYCZNA / SPORT ----------------
    {
        "rsid": "rs1815739", "gene": "ACTN3 (R577X)", "category": "Wydolnosc fizyczna",
        "name": "'Gen sprintera' - wlokna miesniowe szybkokurczliwe vs. wytrzymalosciowe",
        "genotypes": {
            "CC": ("info", "Genotyp RR - pelna alfa-aktynina-3, predyspozycja do dyscyplin siłowo-szybkosciowych (sprint, skoki, podnoszenie ciezarow)"),
            "CT": ("info", "Genotyp RX - mieszany profil, korzysci zarowno w dyscyplinach szybkosciowych jak i wytrzymalosciowych"),
            "TT": ("info", "Genotyp XX - brak funkcjonalnej alfa-aktyniny-3, statystyczna predyspozycja do dyscyplin wytrzymalosciowych (biegi dlugodystansowe)"),
        },
        "note": "Jeden z najlepiej potwierdzonych wariantow zwiazanych z typem wydolnosci sportowej (liczne badania w Nature Genetics/Am J Hum Genet), ale to tylko jeden z wielu czynnikow - trening i motywacja licza sie znacznie bardziej."
    },
    {
        "rsid": "rs4253778", "gene": "PPARA", "category": "Wydolnosc fizyczna",
        "name": "Metabolizm energetyczny miesni - predyspozycja wytrzymalosciowa",
        "genotypes": {
            "GG": ("info", "Wariant zwiazany z lepsza adaptacja wytrzymalosciowa (metabolizm tluszczowy w miesniach)"),
            "GC": ("info", "Genotyp posredni"),
            "CC": ("info", "Wariant czesciej zwiazany z predyspozycja silowo-szybkosciowa"),
        },
        "note": "Efekt niewielki, badany glownie u sportowcow wyczynowych - traktowac jako ciekawostke."
    },

    # ---------------- SEN ----------------
    {
        "rsid": "rs73598374", "gene": "ADA", "category": "Sen",
        "name": "Glebokosc snu wolnofalowego",
        "genotypes": {},
        "note": "Wariant czesto opisywany w popularnych serwisach, ale rzadko obecny na chipach konsumenckich - pomijamy bez odczytu."
    },
    {
        "rsid": "rs12413112", "gene": "RASD1 / okolica zwiazana z chronotypem", "category": "Sen",
        "name": "Chronotyp - skowronek vs. sowa",
        "genotypes": {
            "AA": ("info", "Statystyczna predyspozycja do wczesnego wstawania ('skowronek')"),
            "AG": ("info", "Chronotyp posredni"),
            "GG": ("info", "Statystyczna predyspozycja do pozniejszego chodzenia spac ('sowa')"),
        },
        "note": "Jeden z wielu (setki) loci GWAS zwiazanych z chronotypem (23andMe/UK Biobank, Nature Communications 2016+) - efekt pojedynczego SNP jest bardzo maly, chronotyp jest silnie poligenowy."
    },
    {
        "rsid": "rs121912617", "gene": "DEC2/BHLHE41", "category": "Sen",
        "name": "Krotki sen naturalny ('short sleeper')",
        "genotypes": {},
        "note": "Niezwykle rzadki wariant (rodzinny), praktycznie nieobecny na typowych chipach konsumenckich - informacyjnie."
    },

    # ---------------- BOL / ODCZUWANIE ----------------
    {
        "rsid": "rs6269", "gene": "COMT", "category": "Odczuwanie bolu",
        "name": "Wrazliwosc na bol i skutecznosc lekow przeciwbolowych (powiazany z rs4680)",
        "genotypes": {
            "GG": ("info", "Wariant zwiazany z nizsza wrazliwoscia na bol w niektorych badaniach"),
            "AG": ("info", "Genotyp posredni"),
            "AA": ("info", "Wariant zwiazany z wyzsza wrazliwoscia na bol w niektorych badaniach"),
        },
        "note": "Wyniki badan sa niespojne - traktowac jako ciekawostke, nie regule."
    },

    # ---------------- DLUGOWIECZNOSC ----------------
    {
        "rsid": "rs2802292", "gene": "FOXO3", "category": "Dlugowiecznosc",
        "name": "Wariant FOXO3 zwiazany z dlugowiecznoscia",
        "genotypes": {
            "GG": ("info", "Nosiciel wariantu ochronnego FOXO3 - w wielu niezaleznych badaniach populacyjnych (w tym japonskich stulatkow, publikacje w PNAS) zwiazany ze zwiekszona szansa dozycia sedziwego wieku"),
            "GT": ("info", "Jedna kopia wariantu ochronnego"),
            "TT": ("info", "Brak wariantu ochronnego FOXO3 - typowe (przecietne) szanse dlugowiecznosci zwiazane z tym genem"),
        },
        "note": "Jeden z niewielu wariantow dlugowiecznosci powtarzalnych w wielu populacjach (Japonia, Niemcy, USA, Wlochy) - efekt umiarkowany, styl zycia ma znacznie wieksze znaczenie."
    },

    # ---------------- SKORA / SLONCE ----------------
    {
        "rsid": "rs1805007", "gene": "MC1R", "category": "Skora / opalanie",
        "name": "Wrazliwosc skory na slonce, ryzyko oparzen (MC1R - 'gen rudych')",
        "genotypes": {
            "CC": ("standardowe", "Typowa reakcja skory na slonce"),
            "CT": ("info", "Nosiciel wariantu MC1R - zwiekszona sklonnosc do piegow/jasnej karnacji, wyzsza wrazliwosc na oparzenia sloneczne, zalecana wzmozona ochrona SPF"),
            "TT": ("podwyzszone", "Silny wariant MC1R (czesto wystepuje z rudymi wlosami) - wysoka wrazliwosc na sloce, istotnie podwyzszone ryzyko czerniaka i raka skory przy nadmiernej ekspozycji - zdecydowanie zalecana ochrona SPF i regularne kontrole dermatologiczne znamion"),
        },
        "note": "MC1R to najlepiej poznany gen zwiazany z ryzykiem czerniaka poprzez fototyp skory - potwierdzone w wielu badaniach (Nature Genetics)."
    },

    # ---------------- OCZY / WLOSY ----------------
    {
        "rsid": "rs12913832", "gene": "HERC2/OCA2", "category": "Cechy fizyczne",
        "name": "Kolor oczu (niebieski vs. brazowy)",
        "genotypes": {
            "AA": ("info", "Bardzo prawdopodobny niebieski kolor oczu"),
            "AG": ("info", "Posredni - czesto zielony/orzechowy lub jasnobrazowy kolor oczu"),
            "GG": ("info", "Bardzo prawdopodobny brazowy kolor oczu"),
        },
        "note": "Najsilniejszy pojedynczy determinant koloru oczu u ludzi (>70% wariancji), dobrze potwierdzone od 2008 r. (Eiberg et al.)."
    },
    {
        "rsid": "rs4778241", "gene": "OCA2", "category": "Cechy fizyczne",
        "name": "Kolor oczu - wariant dodatkowy",
        "genotypes": {
            "GG": ("info", "Sprzyja jasniejszemu kolorowi oczu"),
            "GT": ("info", "Genotyp posredni"),
            "TT": ("info", "Sprzyja ciemniejszemu kolorowi oczu"),
        },
        "note": "Dziala wspolnie z rs12913832 w ustalaniu ostatecznego koloru oczu."
    },
    {
        "rsid": "rs17822931", "gene": "ABCC11", "category": "Cechy fizyczne",
        "name": "Typ woszczyny usznej i zapach potu (suchy/mokry earwax)",
        "genotypes": {
            "CC": ("info", "Woszczyna mokra (typowa dla Europy/Afryki), zwiazana takze z bardziej wyczuwalnym zapachem potu spod pach"),
            "CT": ("info", "Genotyp posredni - zwykle mokra woszczyna"),
            "TT": ("info", "Woszczyna sucha, typowo mniej intensywny zapach potu spod pach (czesty w Azji Wschodniej)"),
        },
        "note": "Klasyczny, bardzo dobrze potwierdzony wariant (Nature Genetics 2006, Yoshiura et al.) - czysta ciekawostka bez znaczenia zdrowotnego."
    },
    {
        "rsid": "rs3827760", "gene": "EDAR", "category": "Cechy fizyczne",
        "name": "Grubosc wlosow, ksztalt siekaczy (wariant azjatycki EDAR)",
        "genotypes": {
            "AA": ("info", "Wariant azjatycki EDAR - grubsze wlosy, charakterystyczny ksztalt siekaczy"),
            "AG": ("info", "Genotyp posredni"),
            "GG": ("info", "Wariant typowy dla Europy/Afryki - cieńsze wlosy"),
        },
        "note": "Rzadki w populacjach europejskich, jeden z najsilniej pod wzgledem selekcji naturalnej zbadanych SNP u czlowieka."
    },
    {
        "rsid": "rs1426654", "gene": "SLC24A5", "category": "Cechy fizyczne",
        "name": "Jasna karnacja skory (europejski wariant depigmentacji)",
        "genotypes": {
            "AA": ("info", "Wariant zwiazany z jasna karnacja skory (typowy dla Europy/Bliskiego Wschodu/Azji Poludniowej)"),
            "AG": ("info", "Genotyp posredni"),
            "GG": ("info", "Wariant przodkowy zwiazany z ciemniejsza karnacja (typowy dla Afryki/rdzennej ludnosci wielu regionow)"),
        },
        "note": "Jeden z najsilniej dzialajacych pojedynczych genow depigmentacji skory u czlowieka, szeroko cytowany (Science 2005, Lamason et al.)."
    },

    # ---------------- ALERGIE / ODPORNOSC ----------------
    {
        "rsid": "rs20541", "gene": "IL13", "category": "Alergie / odpornosc",
        "name": "Predyspozycja do astmy i chorob atopowych (alergie, egzema)",
        "genotypes": {
            "AA": ("standardowe", "Typowe ryzyko chorob atopowych"),
            "AG": ("lekko podwyzszone", "Nosiciel - nieznacznie podwyzszone ryzyko astmy/atopii w niektorych populacjach"),
            "GG": ("podwyzszone", "Homozygota - opisywane umiarkowanie podwyzszone ryzyko astmy i chorob atopowych (egzema, katar sienny)"),
        },
        "note": "Jeden z wielu (dziesiatki) loci zwiazanych z astma w GWAS - efekt pojedynczego wariantu jest niewielki."
    },

    # ---------------- METABOLIZM WITAMIN ----------------
    {
        "rsid": "rs2282679", "gene": "GC (VDBP)", "category": "Witaminy / metabolizm",
        "name": "Poziom witaminy D w surowicy",
        "genotypes": {
            "TT": ("standardowe", "Typowy poziom bialka wiazacego witamine D"),
            "GT": ("info", "Nosiciel wariantu zwiazanego z nieco nizszym typowym poziomem witaminy D we krwi"),
            "GG": ("lekko podwyzszone ryzyko niedoboru", "Homozygota - w badaniach populacyjnych (w tym duzych GWAS w Nature Genetics) zwiazana z nizszym typowym poziomem witaminy D, warto rozwazyc regularne badanie 25(OH)D zwlaszcza w miesiacach zimowych"),
        },
        "note": "Jeden z najsilniej potwierdzonych wariantow zwiazanych z poziomem witaminy D we krwi."
    },
    {
        "rsid": "rs602662", "gene": "FUT2", "category": "Witaminy / metabolizm",
        "name": "Status 'sekretora' - wplywa na ZMIERZONY poziom witaminy B12 we krwi",
        "genotypes": {
            "GG": ("info", "'Sekretor' - w badaniach populacyjnych zwiazany z NIZSZYM zmierzonym poziomem calkowitej witaminy B12 we krwi"),
            "AG": ("info", "Posredni status sekretora - posredni zmierzony poziom B12"),
            "AA": ("info", "'Nie-sekretor' - w badaniach populacyjnych zwiazany z WYZSZYM zmierzonym poziomem calkowitej witaminy B12 we krwi (srednio ok. 16-25% wyzszy)"),
        },
        "note": "WAZNE (zweryfikowane w niezaleznym procesie badawczym, lipiec 2026): efekt dziala przez frakcje B12 zwiazana z haptokoryna (tzw. holo-haptokoryna) - czyli wplywa na WYNIK BADANIA KRWI, a NIE na biologicznie aktywna, dostepna dla komorek frakcje (holo-transkobalamina), ktora u sekretorow i nie-sekretorow jest podobna (Fedosov i wsp., Human Molecular Genetics 2017/2018). Innymi slowy: 'sekretor' (GG) moze miec NIZSZY wynik badania B12 we krwi bez faktycznego niedoboru na poziomie komorek. Popularna w internecie porada, ze 'sekretorzy' (lub nosiciele okreslonego genotypu) potrzebuja wiekszej dawki, formy podjezykowej/w zastrzykach lub metylokobalaminy - NIE ma potwierdzenia w literaturze naukowej dla tego konkretnego genu. Jesli wystepuja objawy sugerujace niedobor B12 (problemy z pamiecia, drętwienie, zmeczenie) - decyduje faktyczny wynik badania krwi (B12, kwas metylomalonowy, homocysteina), nie ten gen."
    },
    {
        "rsid": "rs1801222", "gene": "CUBN", "category": "Witaminy / metabolizm",
        "name": "Wchlanianie witaminy B12 w jelicie (receptor kubilina)",
        "genotypes": {
            "GG": ("standardowe", "Zwiazany z wyzszym typowym poziomem witaminy B12 we krwi"),
            "AG": ("info", "Posredni - jedna kopia wariantu zwiazanego z nizszym typowym poziomem B12"),
            "AA": ("lekko podwyzszone", "Zwiazany z nizszym typowym poziomem witaminy B12 we krwi"),
        },
        "note": "WAZNE (zweryfikowane, lipiec 2026): CUBN koduje kubilinę - realny receptor odpowiedzialny za wchlanianie witaminy B12 (polaczonej z czynnikiem wewnetrznym) w koncowym odcinku jelita cienkiego. To mechanistycznie NAJBARDZIEJ wiarygodny z genow B12 w tym raporcie pod katem faktycznego wchlaniania (w odroznieniu od FUT2, ktory wplywa tylko na pomiar we krwi). Rzadkie, powazne mutacje w tym genie powoduja zespol Imerslund-Grasbeck wymagajacy wstrzykiwan B12 do konca zycia - ale to POSPOLITY wariant o wiele slabszym efekcie, nie ta choroba. Brak badan klinicznych potwierdzajacych, ze nosiciele tego wariantu potrzebuja innej formy/dawki B12 - to wciaz tylko wskazowka, nie regula. Hazra i wsp., Human Molecular Genetics 2009; potwierdzone w kohorcie islandzko-dunskiej (P=3.3x10^-75)."
    },

    # ---------------- WATROBA / ALKOHOL ----------------
    {
        "rsid": "rs58542926", "gene": "TM6SF2 (E167K)", "category": "Watroba / alkohol",
        "name": "Ryzyko uszkodzenia watroby zwiazanego z alkoholem",
        "genotypes": {
            "CC": ("standardowe", "Typowe ryzyko stluszczenia/uszkodzenia watroby, w tym zwiazanego z alkoholem"),
            "CT": ("podwyzszone", "Nosiciel jednej kopii wariantu - realnie podwyzszone ryzyko stluszczenia watroby, wloknienia i marskosci watroby zwiazanej z alkoholem w porownaniu do osob bez tego wariantu przy tym samym poziomie picia"),
            "TT": ("wysokie", "Rzadkie (homozygota) - najwyzsze ryzyko w tej grupie, ale bardzo rzadkie w populacji europejskiej (czestosc allelu ok. 7-8%)"),
        },
        "note": "WAZNE (zweryfikowane w niezaleznym procesie badawczym z aktywnym poszukiwaniem sprzecznych dowodow, lipiec 2026): drugi najsilniej potwierdzony (po PNPLA3) gen ryzyka choroby watroby zwiazanej z alkoholem (Buch/Stickel/Trepo i wsp., Nature Genetics 2015, P=7.9x10^-10). WAZNA UWAGA: ten sam wariant T obniza jednoczesnie LDL/trojglicerydy i ryzyko sercowo-naczyniowe - to NIE jest jednoznacznie 'zly' wariant, tylko niekorzystny konkretnie dla watroby. NAJWAZNIEJSZY pojedynczy gen ryzyka watroby alkoholowej to PNPLA3 (rs738409) - ale ten SNP NIE jest mierzony na chipie AncestryDNA, wiec nie da sie go tu sprawdzic. Jesli w rodzinie regularnie spozywany jest alkohol, warto to potraktowac jako dodatkowy, realny argument za ograniczeniem picia i regularnym sprawdzaniem prob watrobowych (ALT, AST, GGTP), niezaleznie od wyniku tego pojedynczego genu."
    },

    # ---------------- DNA MOCZANOWA / STAWY ----------------
    {
        "rsid": "rs2231142", "gene": "ABCG2 (Q141K)", "category": "Dna moczanowa / stawy",
        "name": "Poziom kwasu moczowego i ryzyko dny moczanowej",
        "genotypes": {
            "GG": ("standardowe", "Typowy poziom kwasu moczowego, standardowe ryzyko dny moczanowej"),
            "GT": ("podwyzszone", "Nosiciel jednej kopii - transporter usuwajacy kwas moczowy dziala slabiej, podwyzszony poziom kwasu moczowego i ryzyko dny moczanowej"),
            "TT": ("wysokie", "Dwie kopie wariantu - znaczaco slabszy transport kwasu moczowego, wyraznie podwyzszone ryzyko dny moczanowej (bolesne napady zapalenia stawow, czesto w duzym palcu u nogi)"),
        },
        "note": "Jeden z dwoch najsilniej i najszerzej potwierdzonych genow kwasu moczowego/dny na swiecie (obok SLC2A9, ktory nie jest mierzony na tym chipie), replikowany w dziesiatkach populacji (m.in. Dehghan i wsp., Lancet 2008; Kolz i wsp., PLoS Genetics 2009). WAZNE ZASTRZEZENIE: bolesne narosla/zmiany na stawach palcow (zwlaszcza stop) moga miec wiele przyczyn poza dna - choroba zwyrodnieniowa stawow (artroza, tzw. guzki Heberdena/Boucharda) jest znacznie CZESTSZA u starszych osob i ma zupelnie inne, w wiekszosci niegenetyczne przyczyny (zuzycie stawow). Ten gen NIE odroznia dny od artrozy - jedynie badanie krwi (poziom kwasu moczowego) i ocena lekarza/reumatologa moga to rozstrzygnac."
    },

    # ---------------- TARCZYCA / AUTOIMMUNOLOGIA ----------------
    {
        "rsid": "rs2476601", "gene": "PTPN22 (R620W)", "category": "Tarczyca / autoimmunologia",
        "name": "Predyspozycja do chorob autoimmunologicznych (w tym tarczycy)",
        "genotypes": {
            "GG": ("standardowe", "Brak wariantu ryzyka - standardowe ryzyko chorob autoimmunologicznych zwiazane z tym genem"),
            "AG": ("lekko podwyzszone", "Nosiciel jednej kopii - podwyzszone ryzyko chorob autoimmunologicznych (w tym Hashimoto, Graves-Basedow, cukrzyca typu 1, reumatoidalne zapalenie stawow, toczen)"),
            "AA": ("podwyzszone", "Dwie kopie - najwyzsze ryzyko w tej grupie, choc nadal rzadkie (homozygota wystepuje rzadko)"),
        },
        "note": "Jeden z najslawniejszych i najlepiej potwierdzonych genow autoimmunologicznych u czlowieka (Bottini i wsp., Nature Genetics 2004, replikowany setki razy). Podwyzsza ryzyko calej grupy chorob autoimmunologicznych naraz (nie tylko tarczycy) - jesli w rodzinie juz wystepuje jedna choroba autoimmunologiczna, ten gen czesciowo tlumaczy dlaczego, ale NIE jest jedynym czynnikiem (dziesiatki innych genow + srodowisko). Uwaga: kierunek i sila efektu dla tego wpisu oparte na ugruntowanej wiedzy z literatury (nie byly ponownie weryfikowane w tej sesji przez zywe wyszukiwanie ze wzgledu na limit sesji) - zalecana niezalezna weryfikacja przy okazji kolejnej aktualizacji bazy."
    },
    {
        "rsid": "rs965513", "gene": "FOXE1 (9q22.33)", "category": "Tarczyca / autoimmunologia",
        "name": "Ryzyko guzkow tarczycy i raka brodawkowatego tarczycy",
        "genotypes": {
            "GG": ("standardowe", "Standardowe (nizsze w tej grupie) ryzyko guzkow tarczycy i raka brodawkowatego tarczycy"),
            "AG": ("lekko podwyzszone", "Nosiciel jednej kopii - umiarkowanie podwyzszone ryzyko guzkow tarczycy/raka brodawkowatego tarczycy"),
            "AA": ("podwyzszone", "Dwie kopie - najwyzsze ryzyko w tej grupie (ok. 1.75x na kopie allelu wg oryginalnego badania)"),
        },
        "note": "Wariant z Gudmundsson i wsp., Nature Genetics 2009 (region 9q22.33 blisko genu FOXE1) - jeden z pierwszych i najsilniej potwierdzonych powszechnych wariantow ryzyka raka tarczycy. WAZNE: to marker OGOLNEGO, POPULACYJNEGO ryzyka - w ZADEN sposob nie moze ocenic, czy KONKRETNY, juz istniejacy i monitorowany guzek jest lagodny czy zlosliwy. O tym decyduje wylacznie USG, biopsja i ocena endokrynologa/onkologa - ten gen tego nie zastapi i nie powinien wplywac na decyzje o dalszej diagnostyce ani jej odwlekac. Uwaga: kierunek efektu oparty na ugruntowanej wiedzy z literatury (nie byl ponownie weryfikowany w tej sesji przez zywe wyszukiwanie ze wzgledu na limit sesji) - zalecana niezalezna weryfikacja przy okazji kolejnej aktualizacji bazy."
    },
]

# Warianty do specjalnej, laczonej interpretacji (np. APOE)
COMBO_APOE = {
    ("rs429358", "rs7412"): {
        ("TT", "CC"): "e3/e3 - najczestszy genotyp w populacji, neutralne ryzyko Alzheimera zwiazane z APOE",
        ("TT", "CT"): "e2/e3 - jedna kopia allelu e2, lekko OBNIZONE ryzyko Alzheimera",
        ("TT", "TT"): "e2/e2 - rzadkie, potencjalnie obnizone ryzyko Alzheimera, ale zwiazane z ryzykiem hiperlipoproteinemii typu III",
        ("CT", "CC"): "e3/e4 - jedna kopia allelu e4, umiarkowanie PODWYZSZONE ryzyko Alzheimera (ok. 2-3x)",
        ("CC", "CC"): "e4/e4 - dwie kopie allelu e4, ISTOTNIE PODWYZSZONE ryzyko Alzheimera (nawet 8-12x) - jeden z najsilniejszych znanych czynnikow genetycznych, ale NIE jest to pewnosc zachorowania",
        ("CT", "CT"): "e2/e4 (rzadkie, niejednoznaczne) - mieszany profil, zwykle traktowany jako w przyblizeniu neutralny/lekko podwyzszony",
    }
}

# ---------------------------------------------------------------------------
# WARSTWA "PROSTY JEZYK" - dla uproszczonego raportu dla os. starszych/
# niewtajemniczonych. Zaden zargon (bez "genotyp", "homozygota", "rsID").
# Kazdy wpis pokazuje sie w uproszczonym raporcie TYLKO gdy poziom ryzyka danej
# osoby (pole "risk" z analizy) znajduje sie w "trigger_risks".
# section: "uwaga" (na co uwazac) / "lekarz" (co powiedziec lekarzowi) /
#          "styl_zycia" (dieta/nawyki) / "dobra_wiadomosc" / "ciekawostka"
# ---------------------------------------------------------------------------
PLAIN_ADVICE = [
    {
        "rsid": "rs6025", "section": "uwaga", "icon": "🩸",
        "title": "Skrzepy krwi (zakrzepica)",
        "trigger_risks": ["podwyzszone", "wysokie"],
        "text": "Organizm ma nieco większą skłonność do tworzenia zakrzepów krwi. Ważne żeby powiedzieć o tym lekarzowi przed: dłuższym unieruchomieniem (np. po operacji, długi lot samolotem), przy przepisywaniu hormonów (np. tabletki antykoncepcyjne, hormonalna terapia zastępcza).",
        "diet": "Jedz: dużo wody, ryby (kwasy omega-3 lekko rozrzedzają krew), warzywa. Unikaj: długiego siedzenia bez ruchu, odwodnienia, nadmiaru soli.",
        "origin": "Wariant najczęstszy u osób pochodzenia europejskiego (nosicielstwo ok. 3-8%), rzadki w Azji i Afryce.",
        "body_mind": "Dotyczy ciała, nie umysłu. Dobre hobby: spacery, pływanie, jazda na rowerze — cokolwiek co przerywa długie siedzenie.",
    },
    {
        "rsid": "rs1799963", "section": "uwaga", "icon": "🩸",
        "title": "Skrzepy krwi (zakrzepica)",
        "trigger_risks": ["podwyzszone", "wysokie"],
        "text": "Podobnie jak wyżej — nieco większa skłonność do zakrzepów krwi. Warto poinformować lekarza, zwłaszcza przed operacjami lub długimi podróżami.",
        "origin": "Podobnie jak wariant Leiden — częstszy u osób pochodzenia europejskiego.",
    },
    {
        "rsid": "rs9923231", "section": "lekarz", "icon": "💊",
        "title": "Leki rozrzedzające krew (np. Warfaryna, Acenokumarol)",
        "trigger_risks": ["info"],
        "text": "Jeśli kiedykolwiek lekarz przepisze leki rozrzedzające krew (Warfaryna/Acenokumarol), warto wspomnieć, że wrażliwość na ten lek może być inna niż przeciętna — dawka powinna być dobierana ostrożnie, ze wzmożoną kontrolą na początku leczenia.",
        "diet": "Przy takim leczeniu liczy się STAŁA (nie zerowa) ilość witaminy K w diecie — nie zmieniaj nagle ilości zielonych warzyw liściastych (jarmuż, szpinak, brokuły), bo to wpływa na działanie leku.",
    },
    {
        "rsid": "rs1801133", "section": "styl_zycia", "icon": "🥗",
        "title": "Kwas foliowy (witamina B9)",
        "trigger_risks": ["lekko podwyzszone", "podwyzszone"],
        "text": "Organizm gorzej przetwarza zwykły kwas foliowy z suplementów/wzbogaconej żywności.",
        "diet": "Jedz: dużo zielonych warzyw liściastych (szpinak, brokuły, sałata, jarmuż), jajka, rośliny strączkowe. Przy suplementacji pytaj aptekarza o formę 'metylofolian' zamiast zwykłego kwasu foliowego — lepiej przyswajalna przy tym wariancie.",
        "origin": "Wariant bardzo częsty na całym świecie, ale wyjątkowo częsty w populacjach śródziemnomorskich i latynoskich (nawet 25-30% osób z dwiema kopiami).",
    },
    {
        "rsid": "rs1800562", "section": "uwaga", "icon": "⚙️",
        "title": "Nadmiar żelaza w organizmie (hemochromatoza)",
        "trigger_risks": ["wysokie"],
        "text": "Organizm może gromadzić za dużo żelaza, co z czasem obciąża wątrobę, serce i stawy. Warto poprosić lekarza o zwykłe badanie krwi (żelazo, ferrytyna, TIBC) — jeśli poziom jest za wysoki, leczenie jest proste (regularne oddawanie krwi/upusty krwi) i bardzo skuteczne, jeśli wykryte wcześnie. Wykryte i leczone na czas — długość życia jest normalna.",
        "diet": "Unikaj: suplementów żelaza i witaminy C w dużych dawkach przy posiłkach (witamina C zwiększa wchłanianie żelaza), ograniczaj czerwone mięso i alkohol (obciążają wątrobę dodatkowo przy nadmiarze żelaza), nie gotuj w żeliwnych naczyniach. Herbata i kawa do posiłków lekko ZMNIEJSZAJĄ wchłanianie żelaza — tu akurat pomaga.",
        "origin": "To tzw. 'celtycka choroba' — zdecydowanie najczęstsza u osób pochodzenia północnoeuropejskiego (Irlandia, Szkocja, Skandynawia), bardzo rzadka w Azji i Afryce.",
    },
    {
        "rsid": "rs1799945", "section": "uwaga", "icon": "⚙️",
        "title": "Nadmiar żelaza w organizmie",
        "trigger_risks": ["podwyzszone"],
        "text": "Niewielka skłonność do gromadzenia żelaza. Warto przy okazji badań krwi poprosić o sprawdzenie poziomu żelaza/ferrytyny raz na jakiś czas.",
        "origin": "Podobnie jak wyżej — najczęstszy w populacjach północnoeuropejskich.",
    },
    {
        "rsid": "rs671", "section": "styl_zycia", "icon": "🍷",
        "title": "Reakcja na alkohol",
        "trigger_risks": ["info"],
        "text": "Organizm gorzej rozkłada alkohol — po piciu może pojawiać się silne czerwienienie twarzy, przyspieszone bicie serca, złe samopoczucie. Regularne picie mimo takiej reakcji wiąże się z podwyższonym ryzykiem raka przełyku, więc najlepiej mocno ograniczyć alkohol.",
        "origin": "Wariant niemal wyłącznie u osób pochodzenia wschodnioazjatyckiego (Chiny, Japonia, Korea) — u osób pochodzenia europejskiego praktycznie nie występuje.",
    },
    {
        "rsid": "rs16969968", "section": "styl_zycia", "icon": "🚬",
        "title": "Palenie papierosów",
        "trigger_risks": ["lekko podwyzszone", "podwyzszone"],
        "text": "Osoby z tym wariantem, jeśli palą, mają zwykle większy 'głód' nikotyny i palą więcej papierosów — co dodatkowo zwiększa ryzyko raka płuc. Jeśli ktoś pali — to jeden z najlepszych możliwych argumentów, żeby rzucić. Jeśli nie pali — ten wariant nie ma żadnego znaczenia.",
    },
    {
        "rsid": "rs7903146", "section": "uwaga", "icon": "🍬",
        "title": "Cukrzyca typu 2",
        "trigger_risks": ["podwyzszone", "wysokie"],
        "text": "Nieco wyższa skłonność do cukrzycy typu 2 — to ryzyko, na które mamy realny wpływ przez dietę i ruch. Raz w roku warto zrobić badanie poziomu cukru we krwi (glukoza na czczo), szczególnie po 40-50 roku życia. Nieleczona/niekontrolowana cukrzyca skraca średnią długość życia o kilka lat wg badań epidemiologicznych — ale dobra kontrola (dieta, ruch, ew. leki) niweluje większość tego ryzyka.",
        "diet": "Jedz: więcej błonnika (warzywa, pełne ziarna, rośliny strączkowe) i białka przy posiłkach — spowalniają wzrost cukru we krwi. Unikaj: cukru prostego, słodzonych napojów, białego pieczywa i produktów wysoko przetworzonych — ten wariant sprawia, że organizm gorzej sobie z nimi radzi niż przeciętnie.",
        "body_mind": "Regularny ruch (nawet codzienny spacer 30 minut) działa tu podobnie skutecznie jak niejeden lek.",
    },
    {
        "rsid": "rs9939609", "section": "styl_zycia", "icon": "⚖️",
        "title": "Skłonność do nadwagi",
        "trigger_risks": ["lekko podwyzszone", "podwyzszone"],
        "text": "Nieco większa genetyczna skłonność do przybierania na wadze — ten gen wpływa na uczucie sytości (łatwiej przejeść, wolniej czuć, że już wystarczy). Dobra wiadomość: regularna aktywność fizyczna niemal całkowicie znosi ten efekt w badaniach naukowych.",
        "diet": "Jedz: więcej białka i błonnika przy każdym posiłku — obydwa mocno wydłużają uczucie sytości, co kompensuje słabszy sygnał tego genu. Unikaj: podjadania między posiłkami i dużych porcji jedzenia w pośpiechu (mniejsza szansa zauważyć sytość na czas).",
        "origin": "Wariant częsty w populacjach europejskich (ok. 45%), rzadszy w Azji Wschodniej.",
    },
    {
        "rsid": "rs2187668", "section": "uwaga", "icon": "🌾",
        "title": "Celiakia (nietolerancja glutenu)",
        "trigger_risks": ["podwyzszone"],
        "text": "Organizm ma podwyższoną gotowość układu odpornościowego do reagowania na gluten. To NIE znaczy, że celiakia na pewno wystąpi (u większości osób z tym wynikiem nigdy nie występuje) — ale jeśli pojawią się objawy jak bóle brzucha, wzdęcia, biegunki, niewyjaśnione zmęczenie lub 'mgła mózgowa' — warto wspomnieć o tym lekarzowi i zrobić badanie krwi w kierunku celiakii, ZANIM samodzielnie wyeliminuje się gluten z diety (odstawienie glutenu przed badaniem może zafałszować wynik).",
        "origin": "HLA-DQ2.5 najczęstszy w populacjach europejskich, celiakia rzadsza w Azji Wschodniej.",
    },
    {
        "rsid": "rs602662", "section": "lekarz", "icon": "🩺",
        "title": "Witamina B12 — wynik badania krwi może być mylący",
        "trigger_risks": ["info"],
        "text": "Ten gen wpływa na to, ile wynosi standardowe badanie krwi 'witamina B12' — niezależnie od tego, ile B12 faktycznie dociera do komórek. Innymi słowy: wynik krwi może wyglądać nisko lub wysoko z powodu tego genu, a nie prawdziwego niedoboru. WAŻNE: popularna w internecie porada, że przez ten gen potrzeba większej dawki B12 albo specjalnej formy (podjęzykowa, zastrzyki, metylokobalamina) — NIE ma potwierdzenia naukowego. Jeśli występują objawy niedoboru B12 (problemy z pamięcią, dezorientacja, mrowienie/drętwienie rąk i nóg, silne zmęczenie) — najlepiej poprosić lekarza nie tylko o zwykłe B12, ale też o kwas metylomalonowy (MMA) lub homocysteinę — to dokładniej pokazuje rzeczywisty status, niezależnie od tego genu.",
    },
    {
        "rsid": "rs1801222", "section": "lekarz", "icon": "🩺",
        "title": "Wchłanianie witaminy B12 w jelicie",
        "trigger_risks": ["info", "lekko podwyzszone"],
        "text": "Ten gen odpowiada za realny mechanizm wchłaniania witaminy B12 w jelicie (nie tylko za wynik badania krwi, jak poprzedni). Wynik sugerujący słabsze wchłanianie to nadal tylko niewielka statystyczna skłonność, nie diagnoza. Jeśli występują objawy niedoboru B12 (problemy z pamięcią, dezorientacja, częste zapominanie, drętwienie rąk/nóg, silne zmęczenie) — to połączenie objawów + tego wyniku jest dobrym powodem, żeby poprosić lekarza o proste badanie krwi (B12, ewentualnie kwas metylomalonowy). To częsta i ODWRACALNA przyczyna problemów z pamięcią u starszych osób, łatwa do sprawdzenia i wyleczenia, jeśli faktycznie występuje.",
    },
    {
        "rsid": "rs58542926", "section": "uwaga", "icon": "🍷",
        "title": "Wątroba i alkohol",
        "trigger_risks": ["podwyzszone", "wysokie"],
        "text": "Ten gen realnie zwiększa ryzyko uszkodzenia wątroby (stłuszczenie, włóknienie, marskość) u osób regularnie pijących alkohol — przy tym samym poziomie picia, ryzyko jest wyższe niż u osoby bez tego wariantu. To nie znaczy, że uszkodzenie na pewno wystąpi, ale jest to konkretny, dodatkowy powód, żeby ograniczyć alkohol i raz w roku zrobić badanie prób wątrobowych (ALT, AST, GGTP) — zwłaszcza jeśli alkohol pojawia się w życiu regularnie, nie tylko okazjonalnie.",
        "diet": "Unikaj: regularnego picia alkoholu, szczególnie w większych ilościach. Pomaga: dieta uboga w cukry proste i tłuszcze nasycone (dodatkowo obciążają wątrobę), kawa (w umiarkowanych ilościach wiąże się w badaniach z ochronnym działaniem na wątrobę).",
    },
    {
        "rsid": "rs2231142", "section": "dobra_wiadomosc", "icon": "🦴",
        "title": "Dna moczanowa (kwas moczowy)",
        "trigger_risks": ["standardowe"],
        "text": "To najsilniejszy powszechny gen ryzyka dny moczanowej — i wynik jest tu korzystny (standardowe ryzyko). Jeśli występują bolesne zmiany/narośla na stawach palców (zwłaszcza stóp), to na podstawie samej genetyki dna moczanowa jest mniej prawdopodobnym wyjaśnieniem niż np. choroba zwyrodnieniowa stawów — ale to nadal wymaga oceny lekarza/reumatologa i najlepiej prostego badania krwi (poziom kwasu moczowego), a nie zgadywania.",
    },
    {
        "rsid": "rs2231142", "section": "uwaga", "icon": "🦴",
        "title": "Dna moczanowa (kwas moczowy)",
        "trigger_risks": ["podwyzszone", "wysokie"],
        "text": "Ten gen podwyższa ryzyko wysokiego kwasu moczowego i dny moczanowej — bolesnych napadów zapalenia stawów, klasycznie w dużym palcu u nogi, ale też innych stawach stóp. Jeśli występują bolesne zmiany/narośla na stawach palców stóp — warto zrobić proste badanie krwi (kwas moczowy) i skonsultować się z lekarzem/reumatologiem.",
        "diet": "Unikaj: alkoholu (zwłaszcza piwa), czerwonego mięsa i podrobów, słodzonych napojów (fruktoza podnosi kwas moczowy). Pomaga: dużo wody, produkty mleczne o obniżonej zawartości tłuszczu, wiśnie (w niektórych badaniach obniżają częstość napadów dny).",
    },
    {
        "rsid": "rs2476601", "section": "dobra_wiadomosc", "icon": "🛡️",
        "title": "Choroby autoimmunologiczne (w tym tarczycy)",
        "trigger_risks": ["standardowe"],
        "text": "To jeden z najsilniej potwierdzonych genów ryzyka chorób autoimmunologicznych (w tym Hashimoto/Graves-Basedowa) — i wynik jest tu korzystny. Jeśli w rodzinie już występuje choroba tarczycy lub inna autoimmunologiczna, to na podstawie tego akurat genu nie ma dodatkowego wytłumaczenia — przyczyna leży najpewniej gdzie indziej (dziesiątki innych genów + czynniki środowiskowe), co nie zmienia potrzeby dalszej opieki endokrynologicznej.",
    },
    {
        "rsid": "rs2476601", "section": "uwaga", "icon": "🛡️",
        "title": "Choroby autoimmunologiczne (w tym tarczycy)",
        "trigger_risks": ["lekko podwyzszone", "podwyzszone"],
        "text": "Ten gen podwyższa ryzyko całej grupy chorób autoimmunologicznych naraz — w tym zapalenia tarczycy typu Hashimoto i choroby Gravesa-Basedowa, ale też np. reumatoidalnego zapalenia stawów czy cukrzycy typu 1. Jeśli w rodzinie występuje już jedna choroba autoimmunologiczna, warto mieć na uwadze zwiększoną czujność na objawy innych (np. bóle/obrzęki stawów, nietypowe zmęczenie) i wspomnieć o tym lekarzowi rodzinnemu.",
    },
    {
        "rsid": "rs965513", "section": "dobra_wiadomosc", "icon": "🦋",
        "title": "Guzki tarczycy",
        "trigger_risks": ["standardowe"],
        "text": "Ten gen (jeden z najlepiej potwierdzonych wskaźników populacyjnego ryzyka guzków/raka tarczycy) pokazuje tu wynik korzystny — standardowe ryzyko. To dobra wiadomość w tle, ale NIE zastępuje regularnego monitorowania tarczycy, jeśli jest już prowadzone — kontynuuj zalecenia lekarza/endokrynologa bez zmian.",
    },
    {
        "rsid": "rs965513", "section": "uwaga", "icon": "🦋",
        "title": "Guzki tarczycy",
        "trigger_risks": ["lekko podwyzszone", "podwyzszone"],
        "text": "Ten gen wiąże się z nieco podwyższonym populacyjnym ryzykiem guzków tarczycy. BARDZO WAŻNE: to wynik dotyczący ogólnego, statystycznego ryzyka w populacji — w ŻADEN sposób nie mówi, czy jakikolwiek konkretny, już istniejący i monitorowany guzek jest łagodny czy złośliwy. O tym decyduje wyłącznie USG, biopsja i ocena endokrynologa. Ten wynik nie powinien ani uspokajać, ani niepokoić bardziej niż dotychczas — po prostu kontynuuj regularne kontrole, tak jak są już zaplanowane.",
    },
    {
        "rsid": "rs4988235", "section": "styl_zycia", "icon": "🥛",
        "title": "Tolerancja mleka (laktoza)",
        "trigger_risks": ["info"],
        "text": "Jeśli po mleku pojawiają się wzdęcia, gazy albo biegunka — to najpewniej nietolerancja laktozy, nie alergia na mleko.",
        "diet": "Pomaga wtedy: mleko/produkty bez laktozy, sery dojrzewające (mają mało laktozy), jogurt i kefir (bakterie częściowo rozkładają laktozę). Nie trzeba całkiem rezygnować z nabiału — wystarczy dobrać rodzaj.",
        "origin": "Tolerancja laktozy w dorosłości to stosunkowo świeża (ok. 7500 lat) mutacja, która pojawiła się w Europie Północnej — to dlatego u wielu Europejczyków jest normą, a w większości reszty świata (Azja, znaczna część Afryki) naturalnym stanem dorosłego człowieka jest nietolerancja.",
    },
    {
        "rsid": "rs762551", "section": "styl_zycia", "icon": "☕",
        "title": "Kawa i kofeina",
        "trigger_risks": ["info"],
        "text": "Przy wolniejszym metabolizmie kofeiny zostaje ona dłużej w organizmie — warto pić mniej kawy i unikać jej po południu/wieczorem (lepszy sen, mniejsze obciążenie serca). Przy szybkim metabolizmie kawa jest wydalana szybciej i szkodzi statystycznie mniej.",
    },
    {
        "rsid": "rs4149056", "section": "lekarz", "icon": "💊",
        "title": "Leki na cholesterol (statyny)",
        "trigger_risks": ["podwyzszone", "wysokie"],
        "text": "Przy lekach na cholesterol (statyny, np. simwastatyna) może częściej występować ból/osłabienie mięśni. Warto wspomnieć o tym lekarzowi przy przepisywaniu takich leków — czasem wystarczy inna statyna lub niższa dawka. Niektórzy lekarze przy takich dolegliwościach rozważają dodatkowo koenzym Q10 — warto o to zapytać, a nie suplementować na własną rękę.",
    },
    {
        "rsid": "rs1057910", "section": "lekarz", "icon": "💊",
        "title": "Metabolizm niektórych leków",
        "trigger_risks": ["info"],
        "text": "Organizm może inaczej niż przeciętnie przetwarzać niektóre leki (np. na rozrzedzenie krwi, przeciwbólowe, przeciwpadaczkowe). Warto o tym wspomnieć lekarzowi/farmaceucie przy wprowadzaniu nowego leku na stałe.",
    },
    {
        "rsid": "rs1805007", "section": "styl_zycia", "icon": "☀️",
        "title": "Wrażliwość skóry na słońce",
        "trigger_risks": ["podwyzszone", "info"],
        "text": "Skóra jest bardziej wrażliwa na słońce (łatwiej o oparzenia, piegi) i statystycznie wyższe jest ryzyko raka skóry przy dużej ekspozycji na słońce.",
        "diet": "Krem z filtrem SPF 30-50 to podstawa. Dodatkowo pomaga dieta bogata w antyoksydanty (kolorowe warzywa i owoce, pomidory, marchew) — wspiera naturalną ochronę skóry, choć nie zastępuje kremu.",
        "origin": "Silny wariant MC1R (rude włosy, piegi) to klasyczny marker pochodzenia celtycko-północnoeuropejskiego (Irlandia, Szkocja) — bardzo rzadki poza Europą.",
        "body_mind": "Dotyczy tylko ciała/skóry. Hobby na świeżym powietrzu — tak, ale najlepiej wcześnie rano/późnym popołudniem, z ochroną w pełnym słońcu.",
    },
    {
        "rsid": "rs20541", "section": "uwaga", "icon": "🤧",
        "title": "Alergie i astma",
        "trigger_risks": ["podwyzszone", "lekko podwyzszone"],
        "text": "Nieco wyższa skłonność do alergii, astmy, egzemy, kataru siennego. Jeśli występują nawracające problemy z oddychaniem/skórą/katarem — warto rozważyć konsultację alergologiczną.",
        "diet": "Dieta bogata w kwasy omega-3 (tłuste ryby, siemię lniane) bywa pomocna przy ogólnej skłonności do stanów zapalnych/alergicznych — jako uzupełnienie, nie zamiast leczenia.",
    },
    {
        "rsid": "rs2282679", "section": "styl_zycia", "icon": "🥗",
        "title": "Witamina D",
        "trigger_risks": ["lekko podwyzszone ryzyko niedoboru", "info"],
        "text": "Organizm może mieć niższy poziom witaminy D we krwi niż przeciętnie. W Polsce (północna szerokość geograficzna + mało słońca zimą) to podwójne ryzyko niedoboru dla każdego, a przy tym wariancie tym bardziej.",
        "diet": "Jedz: tłuste ryby (łosoś, śledź, makrela), jajka, wzbogacane produkty mleczne. Warto rozważyć suplementację od października do kwietnia i przy okazji badań krwi sprawdzić poziom 25(OH)D.",
    },
    {
        "rsid": "rs2802292", "section": "dobra_wiadomosc", "icon": "🎉",
        "title": "Długowieczność",
        "trigger_risks": ["info"],
        "text": "W dużym badaniu stulatków na Hawajach (Willcox i wsp., PNAS 2008) nosiciele tego wariantu częściej dożywali ok. 100 lat niż osoby bez niego — efekt potwierdzono też (choć słabszy) w Japonii, Niemczech i Włoszech. To realna, wielokrotnie powtórzona obserwacja, ale NIE gwarancja — styl życia (dieta, ruch, brak palenia) ma dużo większy wpływ na długość życia niż ten jeden gen.",
        "body_mind": "Dobra wiadomość dotyczy ogólnej kondycji, nie konkretnie ciała czy umysłu.",
    },
    {
        "rsid": "rs1229984", "section": "dobra_wiadomosc", "icon": "🎉",
        "title": "Ochrona przed nadużywaniem alkoholu",
        "trigger_risks": ["info"],
        "text": "Ten wariant wiąże się ze statystycznie niższym ryzykiem uzależnienia od alkoholu — organizm szybciej przetwarza alkohol na nieprzyjemny dla organizmu produkt uboczny, co naturalnie zniechęca do nadmiernego picia.",
        "origin": "Częstszy w populacjach wschodnioazjatyckich niż europejskich — to jeden z powodów niższych statystyk alkoholizmu w niektórych badaniach populacyjnych w Azji.",
    },
    {
        "rsid": "rs1815739", "section": "ciekawostka", "icon": "🏃",
        "title": "Typ sportowy",
        "trigger_risks": ["info"],
        "text": "To tzw. 'gen sprintera'. Warianty siłowo-szybkościowe sprzyjają dyscyplinom typu sprint, podnoszenie ciężarów, skoki. Warianty wytrzymałościowe sprzyjają długim biegom, jeździe na rowerze, pływaniu długodystansowemu.",
        "diet": "Typ siłowo-szybkościowy: więcej białka wspiera regenerację i budowę mięśni. Typ wytrzymałościowy: więcej węglowodanów złożonych (pełne ziarna, kasze) wspiera zapasy energii na długi wysiłek.",
        "body_mind": "To czysto fizyczna predyspozycja (nie umysłowa) — jeśli szukasz hobby ruchowego, wybór zgodny z tym typem zwykle daje więcej frajdy i szybsze efekty, choć każdy rodzaj ruchu jest lepszy niż brak ruchu.",
    },
    {
        "rsid": "rs4680", "section": "ciekawostka", "icon": "🧠",
        "title": "Typ radzenia sobie ze stresem ('wojownik' vs 'strateg')",
        "trigger_risks": ["info"],
        "text": "Ten gen (COMT) wpływa na to, jak mózg rozkłada dopaminę. Jeden typ ('wojownik') lepiej radzi sobie pod presją i w chaosie, ale bywa gorszy w spokojnych zadaniach wymagających skupienia. Drugi typ ('strateg'/'martwiący się') lepiej radzi sobie w spokojnych warunkach wymagających koncentracji, ale silniej odczuwa stres i ból.",
        "body_mind": "To wariant dotyczący umysłu, nie ciała. 'Wojownik': lepiej czuje się w zmiennych, dynamicznych sytuacjach (praca pod presją czasu, sport zespołowy, sytuacje kryzysowe). 'Strateg': lepiej czuje się przy dłuższej koncentracji w spokoju (czytanie, planowanie, praca analityczna) — warto dobrać hobby/aktywność zgodnie z tym, co daje lepsze samopoczucie, a nie zmuszać się do drugiego stylu.",
    },
    {
        "rsid": "rs12913832", "section": "ciekawostka", "icon": "👁️",
        "title": "Kolor oczu",
        "trigger_risks": ["info"],
        "text": "Ten gen w największym stopniu decyduje o kolorze oczu — niebieskim, brązowym lub czymś pomiędzy (zielony/orzechowy).",
        "origin": "Ciekawostka: wszystkie niebieskie oczy na świecie pochodzą od JEDNEJ wspólnej mutacji sprzed ok. 6-10 tysięcy lat w rejonie Morza Czarnego — wszyscy niebieskoocy ludzie mają tam wspólnego przodka (Eiberg i wsp., 2008).",
    },
    {
        "rsid": "rs17822931", "section": "ciekawostka", "icon": "👂",
        "title": "Woszczyna uszna i zapach potu",
        "trigger_risks": ["info"],
        "text": "Ten gen decyduje o tym, czy woszczyna uszna jest mokra czy sucha, a przy okazji wpływa też na intensywność zapachu potu spod pach. Czysta ciekawostka bez znaczenia zdrowotnego.",
        "origin": "Sucha woszczyna/słabszy zapach potu to wariant niemal powszechny w Azji Wschodniej (>95%) i u rdzennych Amerykanów, a rzadki w Europie i Afryce, gdzie dominuje wersja mokra.",
    },
    {
        "rsid": "rs713598", "section": "ciekawostka", "icon": "👅",
        "title": "Wyczuwanie goryczy",
        "trigger_risks": ["info"],
        "text": "Ten gen wpływa na to, jak mocno wyczuwa się gorzki smak (np. w brukselce, kapuście, grejpfrutach) — dlatego niektórzy naprawdę bardziej 'nie lubią' pewnych warzyw, to nie tylko kwestia gustu.",
    },
]
