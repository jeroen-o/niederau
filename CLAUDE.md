# Werkafspraken Niederau.nl

- Bron is `index.html` (Nederlands). `en/index.html` en `de/index.html` worden gegenereerd: **nooit los bewerken**.
- Nieuwe of gewijzigde Nederlandse tekst: voeg in `tools/translate.py` de vertaalparen (NL → EN/DE) toe; vervallen NL-teksten horen in `OBSOLETE`.
- Na elke wijziging: `./tools/build.sh` (vertalen + SEO/GEO). Het script stopt als een NL-tekst niet gevonden wordt.
- **Altijd SEO en GEO meenemen**: titel en meta-description per taal, canonical/hreflang, geo-metatags, JSON-LD (`tools/seo.py`: WebPage, TouristDestination, dorpen, Hotel, FAQPage), `sitemap.xml`, `llms.txt` en `robots.txt`. Nieuwe feiten die AI-zoekmachines moeten kennen ook in `llms.txt` (via `tools/seo.py`) zetten.
- Seizoenen: 1 okt – 31 mrt winter, 1 apr – 30 sep zomer (`data-season` op `<html>`; elementen met `data-only="winter|summer"`).
- Huisstijl in lijn met Hotel Wastlhof (akkoord hotel); Hotel Wastlhof is partner en wordt zo gelabeld.
- Geen externe API's, geen build-stap voor de site zelf, geen localStorage; Nederlandse getalnotatie.
- Feiten alleen uit betrouwbare bron (hotel, toeristische organisatie of de eigenaar); onzekere feiten voorzichtig formuleren.
