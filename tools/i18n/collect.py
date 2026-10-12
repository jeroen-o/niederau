#!/usr/bin/env python3
"""Verzamelt de unieke (gemaskeerde) tekstblokken van alle gebouwde EN-pagina's en schrijft ontbrekende vertalingen
als brokken naar <scratch>/chunks/<taal>-NNN.json. Gebruik: collect.py <scratch-dir> [chunkgrootte]"""
import collections, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from units import extract, mask

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "tools" / "data" / "i18n"
PRIO = ["", "webcam", "ski-rental-niederau", "ski-area-niederau-map", "markbachjoch", "about", "photos"]

def pages():
    ps = sorted((ROOT / "en").rglob("index.html"), key=lambda f: (f.relative_to(ROOT / "en").parent.as_posix() not in PRIO and 1 or 0,
                len(f.relative_to(ROOT / "en").parts), f.as_posix()))
    return ps

def collect():
    seen = collections.OrderedDict()
    for f in pages():
        _, items = extract(f.read_text(encoding="utf-8"))
        for h, t in items:
            if "hreflang=" in t: continue
            seen.setdefault(mask(t)[0], 0)
    return list(seen)

if __name__ == "__main__":
    scratch = pathlib.Path(sys.argv[1]); n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    (scratch / "chunks").mkdir(parents=True, exist_ok=True)
    allu = collect()
    for lang in ("fr", "pl"):
        have = json.loads((D / f"{lang}.json").read_text()) if (D / f"{lang}.json").exists() else {}
        todo = [u for u in allu if u not in have]
        for i in range(0, len(todo), n):
            ch = {str(j + 1): u for j, u in enumerate(todo[i:i + n])}
            (scratch / "chunks" / f"{lang}-{i // n:03d}.json").write_text(json.dumps(ch, ensure_ascii=False, indent=0))
        print(lang, len(allu), "totaal,", len(todo), "te vertalen,", -(-len(todo) // n), "brokken")
