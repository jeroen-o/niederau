# Taak: feiten controleren (Niederau.nl)

Controleer de feiten op bestaande pagina's tegen betrouwbare bronnen. **Wijzig geen bestanden in de repo** behalve je eigen outputbestand. Gebruik WebSearch (max ca. 30 zoekopdrachten); WebFetch werkt meestal niet (netwerk geblokkeerd), dus werk met zoekresultaten van officiële clubsites, tirol.at, salzburgerland.com, ÖGV/DGV, 1golf.eu, regio-toerisme.

Per item:
1. Lees het item in de genoemde bron (JSON) en noteer de claims: naam, plaats, aantal holes, par, lengte, openings-/herontwerpjaar, ontwerper, openbaar/clubbaan, datum/periode (events) en de link `url`.
2. Zoek bevestiging bij minimaal twee onafhankelijke bronnen. Zoek ook de **officiële website** van de baan/het evenement (domein van club of organisator).
3. Schrijf je bevindingen in je outputbestand als JSON-lijst, één object per item:
   `{"id": "...", "status": "ok" | "corrected" | "unclear", "official_url": "https://..." of "", "corrections": [{"field": "holes|par|length|year|designer|place|date|other", "old": "...", "new": "...", "evidence": "bron(nen) in een zin"}], "notes": "korte opmerking"}`.
   `status` = ok als alle claims kloppen; corrected als je een fout vond (met bewijs); unclear als bronnen elkaar tegenspreken of je geen bevestiging vond. Verzin niets; bij twijfel `unclear`.
4. Rapporteer aan het einde in max. 10 regels: aantallen per status en de belangrijkste correcties.
