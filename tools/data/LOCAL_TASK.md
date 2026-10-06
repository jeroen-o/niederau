# Taak: lokale Wildschönau-activiteiten (nieuwe pagina's, WebSearch)

Lees eerst `/home/user/niederau/tools/data/SPEC.md` en `/home/user/niederau/tools/data/ACT_TASK.md` (schema). Dit zijn NIEUWE activiteitenpagina's (id's l1, l2, …) voor kernattracties van de Wildschönau die nog geen eigen pagina hebben. Lees ook `/home/user/niederau/index.html` en `/home/user/niederau/omgeving/oberau/index.html`, `/muehltal/`, `/auffach/` voor al aanwezige, betrouwbare feiten.

**Zoekbudget (streng):** maximaal 14 WebSearch-aanroepen totaal (`mode: "standard"`), ~2 per item; geen WebFetch; budget is gedeeld. Neem alleen items op die je kunt bevestigen; kun je een item niet bevestigen, laat het weg (geen drop-entry nodig, noem het in je rapport).

Voor elk item schema volgens ACT_TASK.md plus extra velden: `"new": true`, `"theme"` (wandelen | zwemmen | skieen | winterpret | fietsen | avontuur | dieren | cultuur | attracties | dagtochten | wellness | workshops), `"season"` ("summer" of "winter"; bij jaarrond-items kies het hoofdseizoen en noem het in `facts.season`), `"place"` (slug uit SPEC), `"verified": true`, `slug_en`, `slug_de`, `slug_nl` (kleine letters ascii koppeltekens), intro 2 alinea's 100–150 woorden in NL/EN/DE, 3–4 tips, practical, 2 faq, facts (age/duration/price/distance/season), location, url alleen als bevestigd officieel. Eigen woorden; geen telefoonnummers/adressen/exacte prijzen/openingstijden; geen meta-opmerkingen.

Output: JSON-lijst in het bestand uit je opdracht. Valideer. Rapporteer in max 4 regels (welke items opgenomen/weggelaten).
