#!/bin/sh
# Bouwt de Engelse en Duitse pagina uit index.html en werkt daarna SEO/GEO bij.
# Altijd draaien na een wijziging aan index.html.
set -e
cd "$(dirname "$0")/.."
python3 tools/translate.py
python3 tools/seo.py
python3 tools/subpages.py
