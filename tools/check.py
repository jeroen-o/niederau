#!/usr/bin/env python3
"""Controleert de gebouwde site: kapotte interne links en afbeeldingen, sitemap, canonical/hreflang, JSON-LD, dubbele titels.
Exitcode 1 bij fouten. Draai na ./tools/build.sh (ook in GitHub Actions)."""
import html, json, pathlib, re, sys
from collections import defaultdict
from urllib.parse import urldefrag, urlparse, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://niederau.nl"
errors, warns = [], []

pages = [p for p in ROOT.rglob("index.html") if p.relative_to(ROOT).parts[0] not in ("assets", "tools", ".git", "node_modules")]
pages.append(ROOT / "404.html") if (ROOT / "404.html").exists() else None

def url_of(p):
    rel = p.relative_to(ROOT).as_posix()
    return "/" if rel == "index.html" else "/" + rel[:-len("index.html")] if rel.endswith("index.html") else "/" + rel

def target_exists(base_dir, ref):
    ref = unquote(ref)
    path = ref if ref.startswith("/") else (base_dir / ref).as_posix()
    f = (ROOT / path.lstrip("/")) if ref.startswith("/") else pathlib.Path(path)
    f = pathlib.Path(f)
    return f.is_file() or (f.is_dir() and (f / "index.html").is_file())

titles = defaultdict(list)
ids_cache = {}
for p in pages:
    h = p.read_text(encoding="utf-8")
    here = url_of(p)
    # 1. interne links en afbeeldingen
    for attr, ref in re.findall(r'\b(href|src)="([^"]+)"', h):
        if re.match(r"(https?:|mailto:|tel:|data:|javascript:|//)", ref) or ref.startswith("#"): continue
        ref0, _ = urldefrag(html.unescape(ref))
        if not ref0 or "?" in ref0: ref0 = ref0.split("?")[0]
        if ref0 and not target_exists(p.parent, ref0): errors.append(f"{here}: kapotte {attr} -> {ref}")
    for ref in re.findall(r'srcset="([^"]+)"', h):
        for part in ref.split(","):
            u = part.strip().split(" ")[0]
            if u and not target_exists(p.parent, u): errors.append(f"{here}: kapotte srcset -> {u}")
    # 2. anker op dezelfde pagina
    ids = set(re.findall(r'\bid="([^"]+)"', h))
    for a in re.findall(r'href="#([^"]+)"', h):
        if a and a not in ids and a != "top": warns.append(f"{here}: anker #{a} bestaat niet")
    # 3. canonical, titel, beschrijving, alt
    c = re.search(r'<link rel="canonical" href="([^"]+)"', h)
    if p.name == "index.html":
        if not c: errors.append(f"{here}: geen canonical")
        elif c.group(1) != BASE + here: errors.append(f"{here}: canonical {c.group(1)} wijkt af")
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    if not t or not t.group(1).strip(): errors.append(f"{here}: lege titel")
    else: titles[(here.split('/')[1] if here.startswith(('/en/', '/de/')) else 'nl', t.group(1).strip())].append(here)
    if p.name == "index.html" and not re.search(r'<meta name="description" content="[^"]{20,}"', h): errors.append(f"{here}: beschrijving ontbreekt of te kort")
    for tag in re.findall(r"<img\b[^>]*>", h):
        if " alt=" not in tag: errors.append(f"{here}: img zonder alt: {tag[:80]}")
    # 4. hreflang verwijst naar bestaande pagina's
    for u in re.findall(r'<link rel="alternate" hreflang="[^"]+" href="https://niederau\.nl([^"]*)"', h):
        if not target_exists(ROOT, u): errors.append(f"{here}: hreflang -> {u} bestaat niet")
    # 5. JSON-LD
    for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: json.loads(blob)
        except Exception as e: errors.append(f"{here}: ongeldige JSON-LD ({e})")

for (lang_, t), urls in titles.items():
    if len(urls) > 1: warns.append(f"dubbele titel in {lang_} ({len(urls)}×): {t[:70]} -> {urls[:3]}")

# 6. sitemap
sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
for u in locs:
    path = urlparse(u).path
    if not target_exists(ROOT, path): errors.append(f"sitemap: {u} bestaat niet")
indexable = {BASE + url_of(p) for p in pages if p.name == "index.html"}
missing = indexable - set(locs)
if missing: warns.append(f"{len(missing)} pagina's niet in de sitemap, bijv. {sorted(missing)[:2]}")

print(f"{len(pages)} pagina's gecontroleerd, {len(locs)} sitemap-URL's")
for w in warns[:25]: print("WAARSCHUWING", w)
if len(warns) > 25: print(f"... en {len(warns) - 25} waarschuwingen meer")
for e in errors[:50]: print("FOUT", e)
if len(errors) > 50: print(f"... en {len(errors) - 50} fouten meer")
print(f"{len(errors)} fouten, {len(warns)} waarschuwingen")
sys.exit(1 if errors else 0)
