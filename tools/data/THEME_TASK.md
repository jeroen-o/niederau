# Taak: themapagina's / regiopagina's uitwerken

Lees eerst `/home/user/niederau/tools/data/SPEC.md`. Je schrijft overzichtspagina's voor gezinnen in Niederau. De afzonderlijke activiteitenpagina's worden door anderen geschreven en automatisch onder jouw thema gelinkt; jij schrijft de inleiding en de algemene gids per thema. Zoek met WebSearch (2–3 keer per thema, `mode: "standard"`) betrouwbare algemene feiten (seizoenen, niveau, regels, kosten-indicaties, veiligheid, wat typisch is voor Wildschönau/Tirol/Alpbachtal). Eigen woorden, voorzichtig bij onzekere feiten.

Schema voor een thema (lijst in je outputbestand):
{
 "kind": "theme", "theme": "wandelen",
 "slug_en": "hiking", "slug_de": "wandern", "slug_nl": "wandelen",   // slug_nl = thema-slug uit de spec
 "title": {"nl": "Wandelen in de Wildschönau en omgeving", "en": "...", "de": "..."},
 "tagline": {"nl": "...", "en": "...", "de": "..."},                 // één zin, max ~100 tekens
 "intro": {"nl": "alinea 1\n\nalinea 2\n\nalinea 3", "en": "...", "de": "..."},   // 3 alinea's, 180–260 woorden totaal
 "sections": [ {"h": {"nl":"...","en":"...","de":"..."}, "p": {"nl":"...","en":"...","de":"..."}} ],   // 2-3 korte kopjes met elk 60–110 woorden (bv. Wanneer? Voor wie? Veiligheid & regels)
 "tips": {"nl": ["... 4-5 korte tips"], "en": [...], "de": [...]},
 "faq": [ {"q": {...}, "a": {...}}, ... ]                           // 3 vragen
}
Schema voor een regio (alleen als je opdracht dat noemt):
{ "kind": "region", "region": "zillertal", "slug_en": "zillertal", "slug_de": "zillertal", "slug_nl": "zillertal",
  "name": {...}, "tagline": {...}, "intro": {...3 alinea's, 150-220 woorden}, "highlights": {nl:[4-6], en:[...], de:[...]},
  "getting_there": {...}, "faq": [2 items] }
Schrijf je outputbestand met geldige JSON (UTF-8) en valideer. Rapporteer in max 4 regels.
