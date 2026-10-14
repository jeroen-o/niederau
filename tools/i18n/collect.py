#!/usr/bin/env python3
"""Verzamelt de unieke (gemaskeerde) tekstblokken van alle gebouwde EN-pagina's en schrijft ontbrekende vertalingen
als brokken naar <scratch>/chunks/<taal>-NNN.json. Gebruik: collect.py <scratch-dir> [chunkgrootte]"""
import collections, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from units import extract, mask

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "tools" / "data" / "i18n"
PRIO = [".", "webcam", "ski-rental-niederau", "ski-area-niederau-map", "markbachjoch", "about", "photos"]
CORE = {".", "webcam", "ski-rental-niederau", "ski-area-niederau-map", "markbachjoch", "about", "photos", "legal-notice", "privacy-policy",
        "family-story-wastlhof", "hotel-on-the-slopes-wildschonau", "ski-pass-prices-niederau", "historic-photos-niederau",
        "activities", "nearby", "guides", "events", "region", "activities/huts"}
def phase_ok(rel, phase):
    if phase == "all": return True
    core = rel in CORE or rel.startswith("activities/huts/")
    if phase == "core": return core
    if phase == "guides": return rel.startswith("guides/")
    return core or rel.startswith("guides/")  # "kern": core + guides

def pages(phase="all"):
    ps = sorted((ROOT / "en").rglob("index.html"), key=lambda f: (f.relative_to(ROOT / "en").parent.as_posix() not in PRIO and 1 or 0,
                len(f.relative_to(ROOT / "en").parts), f.as_posix()))
    return [f for f in ps if phase_ok(f.relative_to(ROOT / "en").parent.as_posix(), phase)]

def collect(phase="all"):
    seen = collections.OrderedDict()
    for f in pages(phase):
        _, items = extract(f.read_text(encoding="utf-8"))
        for h, t in items:
            if "hreflang=" in t: continue
            seen.setdefault(mask(t)[0], 0)
    return list(seen)

if __name__ == "__main__":
    # gebruik: collect.py <scratch> [chunkgrootte] [talen,komma] [fase: core|guides|kern|all]
    scratch = pathlib.Path(sys.argv[1]); n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    langs = sys.argv[3].split(",") if len(sys.argv) > 3 else ["fr", "pl"]
    phase = sys.argv[4] if len(sys.argv) > 4 else "all"
    (scratch / "chunks").mkdir(parents=True, exist_ok=True)
    allu = collect(phase)
    for lang in langs:
        have = json.loads((D / f"{lang}.json").read_text()) if (D / f"{lang}.json").exists() else {}
        have = {k.replace("&amp;", "&") for k in have}
        todo = [u for u in allu if u.replace("&amp;", "&") not in have]
        for i in range(0, len(todo), n):
            ch = {str(j + 1): u for j, u in enumerate(todo[i:i + n])}
            (scratch / "chunks" / f"{lang}-{i // n:03d}.json").write_text(json.dumps(ch, ensure_ascii=False, indent=0))
        print(lang, len(allu), "totaal,", len(todo), "te vertalen,", -(-len(todo) // n), "brokken")
