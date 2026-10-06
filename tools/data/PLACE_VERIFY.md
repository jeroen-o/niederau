# Taak: plaatspagina's verifiëren en aanvullen (WebSearch)

Lees eerst `/home/user/niederau/tools/data/SPEC.md`. Input: de bestaande plaatsen in `/home/user/niederau/tools/data/places/<bestand>.json` (jouw bestand + slugs staan in je opdracht). Schema: zie `PLACE_TASK.md` in dezelfde map.

**Zoekbudget (streng):** maximaal 2 WebSearch-aanroepen per plaats (`mode: "standard"`), totaal niet meer dan het dubbele aantal plaatsen; dit budget is gedeeld met andere agents. Geen WebFetch (geblokkeerd).

Per plaats: bevestig/corrigeer met zoekresultaten de feiten (ligging, hoogte, bekende bezienswaardigheden, evenementen, officiële toeristensite, rijtijd vanaf Niederau), schrijf de pagina opnieuw in eigen woorden zodat de intro 3 alinea's van 150–220 woorden heeft in alle drie de talen, vul `elevation_m` en `url` (officiële toeristische/gemeente-site uit de zoekresultaten) in als bevestigd, zet `"verified": true` voor wat je bevestigd hebt, verwijder meta-opmerkingen en onzeker materiaal. Onzekere details laat je weg of formuleer je voorzichtig.

Output: schrijf `/home/user/niederau/tools/data/patches/<naam>.json` = JSON-lijst met voor elke plaats uit je opdracht het volledige bijgewerkte object (zelfde schema en `slug`). Valideer de JSON. Rapporteer in max 4 regels.
