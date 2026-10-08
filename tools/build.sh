#!/bin/sh
# Bouwt alle pagina's: EN/DE uit index.html, losse pagina's (Markbachjoch, activiteiten, plaatsen) en SEO/GEO.
# Altijd draaien na een wijziging aan index.html of tools/data.
set -e
cd "$(dirname "$0")/.."
python3 tools/translate.py
python3 tools/subpages.py
python3 tools/pages.py
python3 tools/seo.py
python3 tools/finalize.py
python3 tools/search.py
