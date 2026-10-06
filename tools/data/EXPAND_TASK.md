# Taak: korte activiteitenpagina's aanvullen en verifiëren (WebSearch)

Lees eerst `/home/user/niederau/tools/data/SPEC.md`. Input: `/home/user/niederau/tools/data/in4/wN.json` (15 items; schema zoals `ACT_TASK.md`; `_`-velden zijn hulpinfo). De intro's zijn te kort (< 85 woorden).

**Zoekbudget (streng):** maximaal 15 WebSearch-aanroepen totaal (`mode: "standard"`), ~1 per item; budget is gedeeld; geen WebFetch.

Per item: zoek aanvullende, bevestigde feiten (wat je ziet/doet, voor wie, seizoen, bijzonderheden, afstand tot Niederau) en schrijf de `intro` opnieuw in eigen woorden, 2 alinea's van samen 100–150 woorden in NL, EN en DE, op bevestigde feiten gebaseerd (niets verzinnen; kun je niets nieuws bevestigen, houd dan de bestaande feiten en breid alleen met algemene, voorzichtige context). Werk `tips` (3–4), `practical` en `faq` bij waar nuttig. Zet `verified: true` alleen als je het bevestigd hebt. Kun je het bestaan niet meer bevestigen: `drop: true`. Geen telefoonnummers, adressen, exacte prijzen of meta-opmerkingen ("niet bevestigd", "volgens de bron").

Output: `/home/user/niederau/tools/data/patches/wN.json` = JSON-lijst met voor elk input-item het volledige bijgewerkte item (zelfde id/schema, zonder `_`-velden). Valideer. Rapporteer in max 4 regels.
