# Taak: een eigen pagina per berghut/skihut in Ski Juwel Alpbachtal Wildschönau (Niederau.nl)

Lees eerst `tools/data/SPEC.md` (regels, plaats-slugs, taal) en bekijk de structuur van `tools/data/patches/golf-new.json` (één item = één pagina). Je schrijft nu **hutten** (thema `hutten`), niet golf.

## Context
De officiële interactieve kaart van Ski Juwel (https://map.skijuwel.com/) toont onder "Hütten" de hutten van het skigebied, per regio (Wildschönau en Alpbachtal). Jij krijgt een deel van die lijst. Elke hut krijgt een eigen pagina in NL/EN/DE voor gezinnen (vooral Nederlandstalig) die in Niederau verblijven.

## Harde regels
- **Niet noemen: openingsstatus, openingstijden, seizoensdata, "open/gesloten", dagen/uren.** De eigenaar wil dit nadrukkelijk niet op de pagina's. Ook niet in `facts.season`. Verwijs voor actuele informatie niet naar een status, alleen: "informeer bij de hut of via de officiële site".
- Geen prijzen, geen telefoonnummers of e-mailadressen. Wel een link naar een officiële site of toeristische pagina in `url` (alleen als je die via WebSearch hebt gezien en de naam klopt; anders `""`).
- Eigen woorden; nooit zinnen overnemen. Alleen feiten uit betrouwbare bronnen (officiële site van de hut, skijuwel.com, wildschoenau.com, alpbachtal.at, Tirol.at, skiresort.info). Onzekere details weglaten of voorzichtig formuleren ("volgens de officiële pagina…").
- Elke hut: unieke tekst, géén kopie-structuur van andere hutten (varieer opbouw en zinnen). Geen superlatieven die je niet kunt onderbouwen. Noem Hotel Wastlhof niet.
- Kernfeiten per hut (naam correct gespeld, plaats/dal, ligging aan welke lift of piste, soort: berggasthof/alm/skihut/apres-skibar/zelfbediening, bijzonderheden zoals terras, speeltuin, dierenweide, specialiteiten, ook zomer bereikbaar te voet) moeten door minstens één betrouwbare bron zijn bevestigd. Lukt dat niet: `drop: true` met `drop_reason` en `verified: false`.
- Er bestaan al passages over Rübezahl-Hütte, Markbachjochalm, Schnapshütte en Norderbergalm op de Markbachjochpagina (zie `tools/subpages.py`, zoek op "Rübezahl"); houd feiten consistent en spreek ze niet tegen.
- Afstand tot Niederau (`facts.distance`): bij benadering, bijvoorbeeld "bij het bergstation van de Markbachjochbahn" of "ca. X minuten rijden naar het dalstation + lift". Alleen wat je kunt onderbouwen.

## Velden (exact zoals golf-new.json)
`id, new: true, theme: "hutten", season: "both" (of "winter" als de hut alleen in de skitijd een rol speelt, "summer" als alleen zomer; kies zonder openingstijden te noemen), drop, drop_reason, place, slug_en, slug_de, title{nl,en,de}, tagline{nl,en,de}, intro{nl,en,de} (2 alinea's gescheiden door \n\n, ca. 110-160 woorden per taal), tips{nl[],en[],de[]} (3 tips), practical{nl,en,de} (1-2 zinnen: hoe kom je er), facts{age:{}, duration:{}, price:{}, distance{nl,en,de}, season:{}}, location{nl,en,de} (plaats/dal), url, faq[] (2 vragen met q/a in nl,en,de), verified: true/false, checked: "2026-10"`.
- `place` = slug uit SPEC.md (niederau, oberau, auffach, thierbach, muehltal, alpbach …) of "" als niet passend.
- `slug_en`/`slug_de`: korte kleine-letter slugs met koppeltekens (bijv. `ruebezahl-huette-markbachjoch`, `ruebezahlhuette-markbachjoch`), uniek over alle hutten. `slug_nl` weglaten.
- Geen HTML-tags, alinea's met lege regel. Nederlandse getalnotatie in NL.
- Schrijf geldige JSON (UTF-8) naar je eigen outputbestand, controleer met `python3 -c "import json;json.load(open(PAD))"`. Raak geen andere bestanden aan, geen git, geen build.
- Rapporteer kort: per hut id, naam, verified ja/nee, en welke hutten je liet vallen met reden.
