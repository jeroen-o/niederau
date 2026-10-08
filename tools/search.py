#!/usr/bin/env python3
"""Bouwt de zoekindex (assets/search-nl|en|de.json) uit de gebouwde HTML-pagina's. Draait na finalize.py."""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
LANGS = ("nl", "en", "de")
KINDS = {  # eerste padsegment (na taalprefix) -> soort
    "activiteiten": "act", "activities": "act", "aktivitaeten": "act",
    "omgeving": "place", "nearby": "place", "umgebung": "place",
    "regio": "region", "region": "region", "gebiet": "region",
    "gids": "guide", "guides": "guide", "ratgeber": "guide",
    "agenda": "event", "events": "event", "veranstaltungen": "event",
    "foto": "other", "fotos": "other", "photos": "other",
}

def clean(s):
    s = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()

def entry(path, lang):
    h = path.read_text(encoding="utf-8")
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    title = clean(m.group(1)).replace(" | Niederau.nl", "") if m else ""
    d = re.search(r'<meta name="description" content="([^"]*)"', h)
    desc = html.unescape(d.group(1)) if d else ""
    c = re.search(r'<link rel="canonical" href="https://niederau\.nl([^"]*)"', h)
    if not c or "noindex" in h[:3000] and 'name="robots" content="noindex' in h: return None
    url = c.group(1)
    mm = re.search(r"<main\b.*?</main>", h, re.S)
    body = mm.group(0) if mm else h
    heads = " · ".join(dict.fromkeys(clean(x) for x in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", body, re.S)))[:420]
    text = clean(re.sub(r"<(h[1-6])\b.*?</\1>", " ", body, flags=re.S))[:520]
    parts = [p for p in url.strip("/").split("/") if p]
    if parts and parts[0] in ("en", "de"): parts = parts[1:]
    kind = KINDS.get(parts[0], "other") if parts else "home"
    if len(parts) == 1 and kind in ("act", "place", "region", "guide", "event"): kind = kind + "-hub"
    if parts[:1] == ["markbachjoch"]: kind = "other"
    return [title, url, kind, desc, heads, text]

def main():
    total = 0
    for lang in LANGS:
        base = ROOT if lang == "nl" else ROOT / lang
        files = [base / "index.html"]
        for p in sorted(base.rglob("index.html")):
            rel = p.relative_to(ROOT).parts
            if lang == "nl" and rel[0] in ("en", "de", "assets", "tools"): continue
            if p != base / "index.html": files.append(p)
        rows = [r for r in (entry(p, lang) for p in files) if r]
        (ROOT / "assets" / f"search-{lang}.json").write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        total += len(rows)
    print(f"zoekindex: {total} pagina's (3 talen)")

if __name__ == "__main__":
    main()
