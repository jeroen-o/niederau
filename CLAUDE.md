# Werkafspraken Niederau.nl

- Bron is `index.html` (Nederlands). `en/index.html` en `de/index.html` worden gegenereerd: **nooit los bewerken**.
- Nieuwe of gewijzigde Nederlandse tekst: voeg in `tools/translate.py` de vertaalparen (NL → EN/DE) toe; vervallen NL-teksten horen in `OBSOLETE`.
- Na elke wijziging: `./tools/build.sh` (vertalen + SEO/GEO). Het script stopt als een NL-tekst niet gevonden wordt.
- **Altijd SEO en GEO meenemen**: titel en meta-description per taal, canonical/hreflang, geo-metatags, JSON-LD (`tools/seo.py`: WebPage, TouristDestination, dorpen, Hotel, FAQPage), `sitemap.xml`, `llms.txt` en `robots.txt`. Nieuwe feiten die AI-zoekmachines moeten kennen ook in `llms.txt` (via `tools/seo.py`) zetten.
- Seizoenen: 1 okt – 31 mrt winter, 1 apr – 30 sep zomer (`data-season` op `<html>`; elementen met `data-only="winter|summer"`).
- Huisstijl in lijn met Hotel Wastlhof (akkoord hotel); Hotel Wastlhof is partner en wordt zo gelabeld.
- Geen externe API's, geen build-stap voor de site zelf, geen localStorage; Nederlandse getalnotatie.
- Feiten alleen uit betrouwbare bron (hotel, toeristische organisatie of de eigenaar); onzekere feiten voorzichtig formuleren.
- Schrijf alle teksten zelf, in eigen woorden. Neem nooit teksten over van hotelwastlhof.at, wildschoenau.com of andere sites; alleen feiten. Controleer met de 6-woordenscan tegen de hotelexport als die beschikbaar is.
- De losse pagina `markbachjoch/` (NL) met `en/markbachjoch/` en `de/markbachjoch/` wordt volledig gegenereerd door `tools/subpages.py` (teksten per taal naast elkaar, eigen SEO/GEO-blok); die drie bestanden nooit los bewerken. Sitemap en llms.txt staan in `tools/seo.py`.
- Activiteiten-, thema-, plaats- en regiopagina's (`activiteiten/`, `omgeving/`, `regio/` en de EN/DE-equivalenten) worden gegenereerd door `tools/pages.py` uit `tools/data/` (acts, places, themes); nooit los bewerken. `tools/data/exclude.json` bevat ids die niet gepubliceerd mogen worden (niet bevestigd). Items met `verified: false` zijn nog niet via een bron gecontroleerd: eerst verifiëren (WebSearch), dan pas uit exclude halen.
