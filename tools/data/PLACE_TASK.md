# Taak: plaatspagina's uitwerken

Lees eerst `/home/user/niederau/tools/data/SPEC.md`.

Je krijgt een lijst plaats-slugs (zie je opdracht). Zoek voor elke plaats met WebSearch (2–4 zoekopdrachten, `mode: "standard"`) betrouwbare feiten: ligging (dal/regio), ligging t.o.v. Niederau (ca. rijtijd per auto en globale route), hoogte, bekende bezienswaardigheden en activiteiten in zomer en winter, bekende evenementen of tradities, het officiële toeristenbureau/gemeente-website. Schrijf op basis daarvan een eigen, nuttige pagina voor gezinnen die in Niederau verblijven en een uitstapje willen plannen. Geen overdrijving; onzekere feiten voorzichtig.

Output: schrijf `/home/user/niederau/tools/data/places/<naam van je batch>.json` als JSON-lijst, één object per plaats:
{
 "slug": "westendorf",
 "region": "brixental",            // wildschoenau | alpbachtal | brixental | kufsteinerland | inntal | zillertal
 "drop": false,
 "name": {"nl": "Westendorf", "en": "Westendorf", "de": "Westendorf"},
 "tagline": {"nl": "...", "en": "...", "de": "..."},                 // één zin, max ~90 tekens
 "intro":   {"nl": "alinea 1\n\nalinea 2\n\nalinea 3", "en": "...", "de": "..."},   // 3 alinea's, samen 150–230 woorden: wat is het voor plaats, wat maakt het bijzonder, voor wie
 "highlights": {"nl": ["...", "... (4-6 punten, elk 1 zin)"], "en": [...], "de": [...]},   // bezienswaardigheden en activiteiten; noem in zomer/winter wat past
 "getting_there": {"nl": "...", "en": "...", "de": "..."},         // ca. rijtijd vanaf Niederau + globale route (bijv. via Wörgl); openbaar vervoer alleen als je het kunt bevestigen
 "best_for": {"nl": "...", "en": "...", "de": "..."},              // één korte zin: past bij ... (gezinnen, cultuur, ski, ...)
 "season": {"nl": "...", "en": "...", "de": "..."},                // korte zin: zomer/winter/hele jaar
 "drive_min": 25,                   // geschatte rijtijd in minuten vanaf Niederau (geheel getal)
 "elevation_m": 700,                // alleen als bevestigd, anders null
 "url": "https://...",              // officiële toeristische site die je gecontroleerd hebt, anders ""
 "faq": [ {"q": {"nl":"...","en":"...","de":"..."}, "a": {"nl":"...","en":"...","de":"..."}}, ... ]   // 2 echte vragen met antwoord, op bevestigde feiten gebaseerd
}
Valideer het JSON-bestand na schrijven. Rapporteer aan het eind in max 4 regels (aantal plaatsen, twijfelgevallen).
