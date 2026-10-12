#!/usr/bin/env python3
"""Voegt vertaalde brokken (<scratch>/out/<taal>-NNN.json) samen in tools/data/i18n/<taal>.json na tag-controle.
Gebruik: ingest.py <scratch-dir>"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from units import sig

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "tools" / "data" / "i18n"
scratch = pathlib.Path(sys.argv[1])
bad = 0; ok = 0
for out in sorted((scratch / "out").glob("*.json")):
    lang = out.name[:2]
    src = json.loads((scratch / "chunks" / out.name).read_text())
    try: tr = json.loads(out.read_text())
    except Exception as e: print("ONLEESBAAR", out.name, e); continue
    f = D / f"{lang}.json"
    have = json.loads(f.read_text()) if f.exists() else {}
    for k, en in src.items():
        t = tr.get(k)
        if not isinstance(t, str) or not t.strip(): bad += 1; continue
        t = t.strip()
        if sig(t) != sig(en): bad += 1; print("TAGS", out.name, k, en[:60], "|", t[:60]); continue
        have[en] = t; ok += 1
    f.write_text(json.dumps(have, ensure_ascii=False, indent=0, sort_keys=True))
print("ok", ok, "afgekeurd", bad)
