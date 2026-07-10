# -*- coding: utf-8 -*-
import json
from variants_db import VARIANTS, COMBO_APOE

def load_raw(path):
    data = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or line.startswith("rsid"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 5:
                continue
            rsid, chrom, pos, a1, a2 = parts
            data[rsid] = (a1, a2)
    return data

def genotype_str(a1, a2):
    return "".join(sorted([a1, a2]))

COMPLEMENT = {"A": "T", "T": "A", "C": "G", "G": "C"}

def complement_genotype(gt):
    return "".join(sorted(COMPLEMENT.get(b, b) for b in gt))

def _normalize_dict(genotypes_dict):
    return {"".join(sorted(k)): v for k, v in genotypes_dict.items()}

def match_genotype(observed, genotypes_dict):
    # observed is alphabetically sorted; dict keys may not be (e.g. "GA" written by hand) -> normalize both
    norm = _normalize_dict(genotypes_dict)
    if observed in norm:
        return norm[observed], False
    # Ancestry sometimes reports on the opposite (complementary) DNA strand
    # relative to the reference strand used by dbSNP/literature - try that too.
    comp = complement_genotype(observed)
    if comp in norm:
        return norm[comp], True
    return None, False

def analyze_person(raw):
    results = []
    for v in VARIANTS:
        rsid = v["rsid"]
        if rsid not in raw:
            results.append({
                "rsid": rsid, "gene": v["gene"], "category": v["category"],
                "name": v["name"], "genotype": None, "risk": "brak_danych",
                "desc": "Ten SNP nie wystepuje w danych surowych (nie byl mierzony na tym chipie).",
                "note": v.get("note", "")
            })
            continue
        a1, a2 = raw[rsid]
        if a1 == "0" or a2 == "0":
            results.append({
                "rsid": rsid, "gene": v["gene"], "category": v["category"],
                "name": v["name"], "genotype": "--", "risk": "brak_odczytu",
                "desc": "Brak poprawnego odczytu (no-call) dla tego markera.",
                "note": v.get("note", "")
            })
            continue
        gt = genotype_str(a1, a2)
        match, flipped = (match_genotype(gt, v["genotypes"]) if v["genotypes"] else (None, False))
        if match is None:
            results.append({
                "rsid": rsid, "gene": v["gene"], "category": v["category"],
                "name": v["name"], "genotype": gt, "risk": "nieznany",
                "desc": f"Genotyp {gt} nie jest opisany w bazie dla tego wariantu.",
                "note": v.get("note", "")
            })
            continue
        risk, desc = match
        results.append({
            "rsid": rsid, "gene": v["gene"], "category": v["category"],
            "name": v["name"], "genotype": gt + (" (odczyt na przeciwnej nici)" if flipped else ""),
            "risk": risk, "desc": desc,
            "note": v.get("note", "")
        })

    # APOE combo interpretation
    apoe_combo = None
    if "rs429358" in raw and "rs7412" in raw:
        g1 = genotype_str(*raw["rs429358"])
        g2 = genotype_str(*raw["rs7412"])
        combo_map = COMBO_APOE[("rs429358", "rs7412")]
        interp = combo_map.get((g1, g2))
        if interp is None:
            # try both orders since genotype strings already sorted; just report raw
            interp = f"Kombinacja rs429358={g1}, rs7412={g2} nie jest w standardowej tabeli referencyjnej (mozliwy rzadki/niejednoznaczny uklad)."
        apoe_combo = {"rs429358": g1, "rs7412": g2, "interpretation": interp}

    return results, apoe_combo

def run(name, path):
    raw = load_raw(path)
    results, apoe = analyze_person(raw)
    return {"name": name, "total_snps": len(raw), "results": results, "apoe": apoe}

if __name__ == "__main__":
    mama = run("Mama", "mama/AncestryDNA.txt")
    tata = run("Tata", "tata/AncestryDNA.txt")
    with open("report_data.json", "w", encoding="utf-8") as f:
        json.dump({"mama": mama, "tata": tata}, f, ensure_ascii=False, indent=2)
    print("mama SNPs:", mama["total_snps"], " tata SNPs:", tata["total_snps"])
    print("Zapisano report_data.json")
