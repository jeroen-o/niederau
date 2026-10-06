# Taak: dunne activiteitenpagina's verdiepen (WebSearch)

Lees eerst `/home/user/niederau/tools/data/SPEC.md`. Input: `/home/user/niederau/tools/data/in5/xN.json` (15 items; schema zoals `ACT_TASK.md`; `_`-velden zijn hulpinfo). De pagina's zijn te dun (weinig tekst); ze moeten inhoudelijk uitgebreid worden voor SEO, met uitsluitend bevestigde feiten.

**Zoekbudget (streng):** maximaal 15 WebSearch-aanroepen totaal (`mode: "standard"`), ~1 per item; budget is gedeeld; geen WebFetch.

Per item: zoek aanvullende bevestigde feiten (wat je ziet/doet, voor wie, seizoen, bijzonderheden, geschiedenis/achtergrond, ligging, bereikbaarheid, wat je meeneemt) en schrijf in eigen woorden:
- `intro`: 3 alinea's samen 170–230 woorden (NL, EN, DE; zelfde inhoud, natuurlijke formulering),
- `tips`: 4–5 tips (elk 1 zin, per pagina verschillend),
- `practical`: 60–90 woorden (bereikbaarheid in grote lijnen, ca. rijtijd vanaf Niederau, parkeren/ov alleen als bevestigd),
- `faq`: 3 vragen met antwoord (verschillende vragen per pagina, gebaseerd op bevestigde feiten).
Behoud de bestaande bevestigde feiten; verwijder niets wat bevestigd is. Kun je niets nieuws bevestigen, voeg dan alleen algemene, nuttige context toe zonder nieuwe feitelijke claims. Geen telefoonnummers/adressen/exacte prijzen/openingstijden, geen meta-opmerkingen ("bronnen", "niet bevestigd"). Vermijd standaardzinnen die op meerdere pagina's identiek zijn (bijna-dubbele pagina's zijn slecht voor SEO). Zet `verified: true` alleen als je het item hebt bevestigd; kun je het bestaan niet bevestigen: `drop: true`.

Output: `/home/user/niederau/tools/data/patches/xN.json` = JSON-lijst met voor elk input-item het volledige bijgewerkte item (zelfde id/schema, zonder `_`-velden). Valideer. Rapporteer in max 4 regels.
