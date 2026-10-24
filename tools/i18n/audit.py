#!/usr/bin/env python3
"""SEO/GEO-audit over alle talen: titel/description, h1, canonical, hreflang (wederkerig + x-default), og:locale(+alternate),
geo-tags, JSON-LD (geldig, inLanguage), sitemap-dekking en taalkiezer. Gebruik: python3 tools/i18n/audit.py"""
import collections, html as _html, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
LANGS = ["nl", "en", "de", "fr", "pl", "es", "it", "sv", "no", "fi", "da"]
SKIP = {"tools", "assets", "node_modules", ".git"}

def lang_of(rel):
    m = re.match(r"(en|de|fr|pl|es|it|sv|no|fi|da)/", rel)
    return m.group(1) if m else "nl"

pages = {}
for f in ROOT.rglob("index.html"):
    rel = f.relative_to(ROOT).as_posix()
    if rel.split("/")[0] in SKIP: continue
    h = f.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in h: continue
    pages[rel] = h
url_of = lambda rel: "/" + rel[:-len("index.html")]
sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
sm_urls = set(re.findall(r"<loc>https://niederau\.nl([^<]*)</loc>", sm))
llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
stat = {l: collections.Counter() for l in LANGS}
count = collections.Counter(); ex = collections.defaultdict(list)
def bad(l, key, rel):
    stat[l][key] += 1
    if len(ex[(l, key)]) < 2: ex[(l, key)].append(url_of(rel))
by_url = {url_of(r): r for r in pages}
for rel, h in pages.items():
    l = lang_of(rel); count[l] += 1; u = url_of(rel)
    if f'<html lang="{ "nb" if False else l}"' not in h: bad(l, "html lang fout", rel)
    t = re.search(r"<title>(.*?)</title>", h, re.S); t = _html.unescape(t.group(1)) if t else ""
    d = re.search(r'<meta name="description" content="([^"]*)"', h); d = _html.unescape(d.group(1)) if d else ""
    if not t: bad(l, "geen title", rel)
    elif len(t) > 70: bad(l, "title>70", rel)
    if not d: bad(l, "geen description", rel)
    elif len(d) > 165: bad(l, "desc>165", rel)
    elif len(d) < 60: bad(l, "desc<60", rel)
    if h.count("<h1") != 1: bad(l, "h1!=1", rel)
    c = re.search(r'<link rel="canonical" href="https://niederau\.nl([^"]*)"', h)
    if not c or c.group(1) != u: bad(l, "canonical", rel)
    alts = dict((a, b) for a, b in re.findall(r'<link rel="alternate" hreflang="([\w-]+)" href="https://niederau\.nl([^"]*)">', h))
    noidx = 'name="robots" content="noindex' in h
    if noidx:
        if alts: bad(l, "noindex-pagina met hreflang", rel)
        if 'class="mt-note"' not in h: bad(l, "geen machinevertaling-melding", rel)
        alts = {}
    if not noidx and "x-default" not in alts: bad(l, "geen x-default", rel)
    if not noidx and alts.get(l) != u: bad(l, "hreflang zelf", rel)
    for lg, tu in alts.items():
        if lg == "x-default": continue
        tr = by_url.get(tu)
        if tr is None: bad(l, "hreflang naar bestaat niet", rel); continue
        back = dict((a, b) for a, b in re.findall(r'<link rel="alternate" hreflang="([\w-]+)" href="https://niederau\.nl([^"]*)">', pages[tr]))
        if back.get(l) != u: bad(l, "hreflang niet wederkerig", rel)
    if 'property="og:locale"' not in h: bad(l, "geen og:locale", rel)
    n_alt = len(re.findall(r'og:locale:alternate', h))
    if not noidx and n_alt != len(alts) - 2: bad(l, "og:locale:alternate aantal", rel)
    for k in ("geo.region", "geo.placename", "geo.position", "ICBM"):
        if f'name="{k}"' not in h: bad(l, "geen " + k, rel)
    if "og:image" not in h: bad(l, "geen og:image", rel)
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    if not lds: bad(l, "geen JSON-LD", rel)
    for s in lds:
        try: j = json.loads(s)
        except Exception: bad(l, "JSON-LD ongeldig", rel); continue
        langs_in = set(re.findall(r'"inLanguage": ?"([\w-]+)"', s))
        if langs_in and langs_in - {l, "nb" if l == "no" else l}: bad(l, "inLanguage ≠ taal", rel)
    if not noidx and u not in sm_urls: bad(l, "niet in sitemap", rel)
    if noidx and u in sm_urls: bad(l, "noindex-pagina staat in sitemap", rel)
    sw = re.search(r'<div class="lang"[^>]*>(.*?)</div>', h, re.S)
    if not sw or 'aria-current="true"' not in sw.group(1): bad(l, "taalkiezer", rel)
print(f"{'taal':5}{'pagina':>7}  problemen")
for l in LANGS:
    probs = ", ".join(f"{k}×{v}" for k, v in stat[l].items()) or "geen"
    print(f"{l:5}{count[l]:>7}  {probs}")
tot = sum(sum(c.values()) for c in stat.values())
print("sitemap-URL's:", len(sm_urls), "| llms.txt noemt:", ", ".join(l for l in LANGS if f"/{l}/" in llms or l == "nl"))
for (l, k), v in list(ex.items())[:12]: print("  voorbeeld", l, k, v)
print("TOTAAL problemen:", tot)
