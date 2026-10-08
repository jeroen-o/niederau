# Taak: alle golfbanen binnen 75 km van Niederau (Niederau.nl)

Lees eerst `tools/data/SPEC.md` (regels, slugs, thema-slugs, taal) en bekijk het voorbeeld `tools/data/patches/golf-new.json` (8 bestaande golfbanen, id g1-g8: Kitzbühel-Schwarzsee, Eichenheim, Kaps, Westendorf, Ellmau Wilder Kaiser, Kaisergolf Ellmau par 3, Zillertal-Uderns, Kaiserwinkl Kössen). **Deze 8 bestaan al; maak ze niet opnieuw.**

Niederau ligt op 47.4446 N, 12.0789 E. "Straal van 75 km" = hemelsbreed (haversine). Reken per baan na en neem alleen banen op die binnen 75 km liggen. Neem 9- en 18-holesbanen, par-3-/korte banen en driving ranges met baan op; géén minigolf, frisbeegolf of indoor-simulatoren.

## Werkwijze
1. Zoek per baan met WebSearch (officiële clubsite, golf.at, Tirol.at, DGV/ÖGV, regio-toerisme) en controleer: exacte naam, plaats, aantal holes, par, lengte, jaar van opening/ontwerper (alleen als bevestigd), en of het een openbare baan is of een club met greenfee voor gasten. Geen prijzen noemen (veranderen), geen telefoonnummers/e-mail. Wel een link naar de officiële site in `url`.
2. Reken de afstand hemelsbreed en de rijtijd vanaf Niederau (afgerond, "ca. X min rijden") en zet die in `facts.distance` en `practical`.
3. Schrijf in eigen woorden (nooit zinnen overnemen). Elke tekst in NL/EN/DE. Toon: zakelijk, geen superlatieven die je niet kunt onderbouwen. Elke baan: unieke tekst, géén kopie-structuur van andere banen (varieer opbouw en zinnen). Noem Hotel Wastlhof niet.
4. `verified`: **true** alleen als de kernfeiten (naam, plaats, holes) door minimaal één betrouwbare bron zijn bevestigd; anders `drop: true` met `drop_reason`. Onzekere details laat je weg of formuleer je voorzichtig.
5. Gebruik exact de structuur van `golf-new.json`: velden `id, new: true, theme: "golf", season: "summer", drop, drop_reason, place, slug_en, slug_de, title{nl,en,de}, tagline, intro (2 alinea's, ca. 110-160 woorden per taal), tips{nl[],en[],de[]} (3-4), practical, facts{age,duration,price,distance,season}, location, url, faq[] (2 vragen), verified`. `price` = "Greenfee wisselt; informeer vooraf" (in de drie talen). `place` = slug uit SPEC.md of "" als de plaats er niet tussen staat (dan zet je de plaatsnaam in `location`). `slug_nl` laat je weg (wordt automatisch gemaakt uit de NL-titel); `slug_en`/`slug_de` maak je zelf, kleine letters, koppeltekens, uniek.
6. Schrijf geldige JSON (UTF-8) naar je eigen outputbestand; controleer met `python3 -c "import json;json.load(open(PAD))"`. Raak geen andere bestanden aan, draai geen git en bouw niets.
7. Rapporteer kort: per baan id, naam, afstand (km), verified ja/nee, en welke banen je liet vallen met reden (bijv. buiten 75 km, gesloten, niet te bevestigen).

## Regio per agent (zoek volledig; elke baan binnen 75 km die in je gebied valt)
- **A**: Kitzbühel en omgeving (Jochberg, Aurach, Reith, Kirchberg, Hopfgarten, Itter, Brixen, Westendorf, St. Johann, Oberndorf, Going, Ellmau, Scheffau, Söll), Pillerseetal/Fieberbrunn, Kaiserwinkl (Kössen, Walchsee, Schwendt, Reit im Winkl), Pinzgau/Salzburg (Mittersill, Zell am See, Kaprun, Saalfelden, Leogang). Output: `tools/data/in6/golf_A.json`, ids `g9`…`g29`.
- **B**: Inntal en Zillertal (Wörgl, Kundl, Rattenberg, Kramsach, Brixlegg, Jenbach, Schwaz, Pill, Hall, Innsbruck-Igls), Alpbachtal, Achensee, Zillertal (Uderns, Fügen, Zell, Mayrhofen). Output: `tools/data/in6/golf_B.json`, ids `g30`…`g50`.
- **C**: Kufsteinerland en Beieren (Kufstein, Thiersee, Erl, Oberaudorf, Bayrischzell, Rosenheim en omgeving, Chiemsee/Bernau/Prien, Aschau, Bad Feilnbach, Reit im Winkl-Ruhpolding, Inzell, Schleching). Output: `tools/data/in6/golf_C.json`, ids `g51`…`g71`.
