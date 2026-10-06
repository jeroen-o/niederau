# Taak: activiteitenbatch uitwerken

Lees eerst `/home/user/niederau/tools/data/SPEC.md` (regels, plaats-slugs, thema's).

Input: `/home/user/niederau/tools/data/in/batch-NN.json` (lijst met ca. 25 items). Elk item heeft `id`, `season` (winter/summer), `theme`, `slug_nl` en `src` met de oorspronkelijke Nederlandse velden (t = titel, tag = ondertitel, desc, tips, route, how, age, dur, cost, loc, adr, phone, url, e = emoji, cat).

Voor elk item:
1. Zoek met WebSearch (1–2 keer) of de activiteit/plek bestaat en wat de feiten zijn (ligging, wat je er doet, doelgroep, seizoen). Controleer ook of de officiële website klopt.
2. Schrijf een nieuwe, eigen pagina-inhoud in NL, EN en DE (zie schema). Herschrijf `desc` en `tips` in eigen woorden; breid zinvol uit met bevestigde feiten (wat is het, voor wie, wat kun je verwachten, wanneer, bijzonderheden), zodat de tekst op zichzelf een bruikbare pagina vormt: `intro` 2 alinea's (samen 90–150 woorden), 3–4 `tips`, `practical` 1 korte alinea (hoe er te komen/bereikbaarheid in grote lijnen, "ca." afstand vanaf Niederau).
3. `drop: true` als het item niet bestaat/niet te vinden is, of een dubbel is van een ander item uit je batch.

Output: schrijf `/home/user/niederau/tools/data/acts/batch-NN.json` als JSON-lijst, één object per input-item, in dezelfde volgorde, exact dit schema:
{
 "id": "w1",
 "drop": false, "drop_reason": "",
 "place": "niederau",              // zie plaats-slugs
 "slug_en": "children-ski-school-niederau",   // kleine letters, ascii, koppeltekens, max 6 woorden, uniek binnen je batch
 "slug_de": "kinderskischule-niederau",       // idem
 "title":   {"nl": "...", "en": "...", "de": "..."},   // korte naam, max ~60 tekens
 "tagline": {"nl": "...", "en": "...", "de": "..."},   // één zin, max ~90 tekens
 "intro":   {"nl": "alinea 1\n\nalinea 2", "en": "...", "de": "..."},
 "tips":    {"nl": ["...","..."], "en": [...], "de": [...]},   // 3-4 korte tips (elk 1 zin)
 "practical": {"nl": "...", "en": "...", "de": "..."},
 "facts": {                                      // alleen bevestigde of voorzichtig geformuleerde feiten
   "age":      {"nl": "Vanaf ca. 3 jaar", "en": "...", "de": "..."},   // leeg object {} als onbekend
   "duration": {"nl": "...", "en": "...", "de": "..."},
   "price":    {"nl": "Prijs wisselt; informeer vooraf", "en": "...", "de": "..."},
   "distance": {"nl": "Ca. 25 min rijden", "en": "...", "de": "..."},
   "season":   {"nl": "Hele jaar / Zomer / Winter", "en": "...", "de": "..."}
 },
 "location": {"nl": "plaats/gebied", "en": "...", "de": "..."},
 "url": "https://...",             // alleen een officiële site die je gecontroleerd hebt, anders ""
 "faq": [ {"q": {"nl":"...","en":"...","de":"..."}, "a": {"nl":"...","en":"...","de":"..."}} ]   // 1 of 2 echte vragen met antwoord, gebaseerd op bevestigde feiten
}
Werk alle items af. Werk efficiënt: geen lange tussenrapporten. Rapporteer aan het eind in max 5 regels: aantal items, aantal gedropt (met id's), en eventuele twijfelgevallen.
