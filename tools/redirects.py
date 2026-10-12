#!/usr/bin/env python3
"""Maakt redirectpagina's (GitHub Pages kent geen server-redirects): meta refresh + canonical + JS-fallback.
Voeg oude/alternatieve URL's toe aan REDIRECTS. Deze pagina's staan niet in de sitemap of zoekindex."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REDIRECTS = {
    "/winter/webcams/": "/webcam/",
}

TPL = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Doorverwijzing | Niederau.nl</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://niederau.nl{to}">
<meta http-equiv="refresh" content="0; url={to}">
<script>location.replace({to!r});</script>
</head>
<body>
<p>Deze pagina is verplaatst naar <a href="{to}">niederau.nl{to}</a>.</p>
</body>
</html>
"""

for src, to in REDIRECTS.items():
    out = ROOT / src.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TPL.format(to=to), encoding="utf-8")
print(f"redirects: {len(REDIRECTS)}")
