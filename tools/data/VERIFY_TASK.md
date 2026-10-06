# Taak: activiteiten verifiëren en verbeteren (WebSearch)

Lees eerst `/home/user/niederau/tools/data/SPEC.md` (regels; let op: eigen woorden, voorzichtige feiten).

Input: `/home/user/niederau/tools/data/in2/vN.json` (≈15 items). Elk item is de huidige, nog onbevestigde pagina-inhoud (schema zoals in `ACT_TASK.md`; extra velden `_theme`, `_season`, `_orig_title`, `_orig_loc` zijn hulpinfo).

**Zoekbudget (streng):** je mag in totaal maximaal 16 WebSearch-aanroepen doen (`mode: "standard"`), ongeveer één per item; dit budget is gedeeld met andere agents, dus overschrijd het niet. Zoek gericht (naam + plaats + "Tirol"). Gebruik WebFetch niet (geblokkeerd).

Per item:
- Bevestigt een zoekresultaat dat de activiteit/plek bestaat (en past bij seizoen/plaats)? Dan: verbeter de tekst met bevestigde feiten (wat, voor wie, seizoen, bijzonderheden), schrijf in eigen woorden, verwijder meta-opmerkingen als "niet bevestigd" / "volgens de bron", zet `"verified": true`, zet `url` op de officiële site als die in de zoekresultaten staat (anders ""), en corrigeer `place`, `facts.distance` ("ca. X min rijden" vanaf Niederau, schatting is oké) en `location`. Houd de lengte van `intro` rond 90–150 woorden (2 alinea's) in alle drie de talen.
- Kon je het niet bevestigen of bestaat het niet (of is het gesloten): zet `"drop": true` met `"drop_reason"` (het item wordt dan niet gepubliceerd).
- Geen telefoonnummers/straatadressen/exacte prijzen of openingstijden tenzij letterlijk bevestigd in zoekresultaten.

Output: schrijf `/home/user/niederau/tools/data/patches/vN.json` = JSON-lijst met voor elk input-item het volledige, bijgewerkte item (zelfde `id`, zelfde schema; verwijder de hulpvelden die met `_` beginnen). Valideer de JSON. Rapporteer in max 5 regels: aantal bevestigd/gedropt en opvallende correcties.
