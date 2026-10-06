# Taak: gidspagina schrijven (WebSearch)

Lees eerst `/home/user/niederau/tools/data/SPEC.md` (regels, eigen woorden, voorzichtig met onzekere feiten). Je schrijft één gidspagina voor Niederau.nl (gezinnen in Niederau, Wildschönau, Tirol, 828 m). Zoekbudget (streng): maximaal het aantal WebSearch-aanroepen uit je opdracht (`mode: "standard"`), geen WebFetch; budget is gedeeld.

Schema (één JSON-object in een lijst):
{
 "id": "...", "slug": {"nl": "...", "en": "...", "de": "..."},   // kleine letters, ascii, koppeltekens
 "title": {"nl","en","de"}, "tagline": {"nl","en","de"},          // tagline max ~100 tekens
 "intro": {"nl","en","de"},                                       // 2-3 alinea's gescheiden door \n\n, samen 150-220 woorden
 "sections": [ {"h": {"nl","en","de"}, "p": {"nl","en","de"}} ], // 5-8 kopjes, elk 60-110 woorden
 "tips": {"nl": [4-5 tips], "en": [...], "de": [...]},
 "faq": [ {"q": {...}, "a": {...}} ]                              // 3 vragen
}
Alles in NL, EN en DE (zelfde inhoud, natuurlijke formulering). Alleen bevestigde feiten; onzekere dingen voorzichtig ("meestal", "ca.", "informeer vooraf"). Geen prijzen/telefoonnummers/adressen, geen meta-opmerkingen over bronnen. Valideer je JSON. Rapporteer in max 3 regels.
