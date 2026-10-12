# Taak: skiverhuur in de Wildschönau (Niederau.nl)

Zoek met WebSearch (max ca. 30 zoekopdrachten; WebFetch werkt meestal niet) welke skiverhuur-/sportwinkels er zijn in de Wildschönau: Niederau, Oberau, Auffach, Thierbach en Mühltal. Zoektermen in NL/EN/DE/FR: skiverhuur, Skiverleih, ski rental, location de ski, Sport Niederau Verleih, Skiservice, Skidepot. Bronnen: officiële websites van de verhuurders, wildschoenau.com/tirol.at-lijsten, Ski Juwel (skijuwel.com), Google-bedrijfsvermeldingen in zoekresultaten.

Per verhuurder, alleen bevestigde feiten:
`{"name": "...", "place": "niederau|oberau|auffach|thierbach|muehltal", "type": ["ski","snowboard","kinderen","langlauf","skiservice","depot","tourski","sneeuwschoenen"] (alleen wat bevestigd is), "near": "bij welk lift/dal/centrum (alleen als bevestigd)", "official_url": "https://..." (officieel domein; leeg als niet gevonden), "sources": ["bron 1", "bron 2"], "confidence": "ok|unclear", "notes": "korte opmerking"}`.

Regels: geen prijzen, geen telefoonnummers, geen e-mailadressen, geen openingstijden (veranderen), geen beoordelingen. Alleen echte bedrijven die in minimaal één betrouwbare bron voorkomen. Verzin niets; bij twijfel `unclear`. Zoek ook algemene feiten: of er in de Wildschönau verhuur aan het dalstation of in het dorp is, of reserveren online kan (alleen als de verhuurder dat zelf vermeldt) en of de skischool/skischoolgroepen verhuur combineren (alleen bevestigd).

Output: schrijf `tools/data/in8/rental.json` (lijst van bovenstaande objecten + sleutel `general`: lijst van bevestigde algemene feiten met bron). Raak geen andere bestanden aan. Rapporteer kort: aantal per plaats en welke twijfel er is.
