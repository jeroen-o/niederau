# Inhoudsspecificatie voor Niederau.nl (activiteiten- en plaatspagina's)

Je schrijft inhoud (JSON) voor losse webpagina's in **NL, EN en DE**. Een generator (`tools/pages.py`) maakt er HTML van. Je raakt geen andere bestanden aan, draait geen git en bouwt niets.

## Regels (verplicht)
- **Eigen woorden.** Kopieer geen zinnen van websites of uit de bronbestanden; herschrijf. Alleen feiten mogen overgenomen worden.
- **Betrouwbaarheid.** De bronbestanden (uit een eerdere, niet-gecontroleerde tekst) bevatten prijzen, adressen, telefoonnummers, openingstijden en namen die deels onjuist kunnen zijn. Controleer met WebSearch (1–2 zoekopdrachten per item; gebruik `mode: "standard"`). Neem alleen over wat je kunt bevestigen. Kun je iets niet bevestigen: laat het weg of formuleer voorzichtig ("rond", "vaak", "informeer vooraf"). **Geen telefoonnummers, geen straatadressen, geen exacte prijzen of openingstijden tenzij bevestigd.** Bestaat de activiteit/plek niet of kun je hem niet vinden, zet `"drop": true` en leg kort uit in `"drop_reason"`.
- Uitgangspunt: gezinnen (vooral Nederlandstalig) die in Niederau (Wildschönau, Tirol, 828 m) verblijven. Geef bij elke pagina een indicatie van de afstand/rijtijd vanaf Niederau (bij benadering, "ca.").
- Toon: helder, zakelijk, vriendelijk, geen overdrijving, geen superlatieven die je niet kunt onderbouwen. Nederlandse getalnotatie in NL-tekst (€ 15, 1.200 m, 2,5 km). EN gebruikt Britse spelling, DE gebruikt "ß" waar het hoort en Duitse getalnotatie.
- Geen emoji in de lopende tekst.
- Geen HTML-tags in tekst, alleen platte tekst; alinea's scheid je met een lege regel (`\n\n`).
- Elke tekst in alle drie de talen, inhoudelijk gelijk, natuurlijk geformuleerd (geen woord-voor-woord vertaling). Eigennamen (Ski Juwel, Wildschönau, Kitzbühel, Markbachjoch…) blijven zoals ze zijn.
- Je voert alleen je eigen toegewezen output-bestand uit. Schrijf het bestand met geldige JSON (UTF-8). Controleer na schrijven met `python3 -c "import json;json.load(open(PAD))"`.

## Vaste plaats-slugs (veld `place` = de plaats waar het item ligt of het dichtst bij ligt)
wildschoenau-dal: niederau, oberau, auffach, thierbach, muehltal
alpbachtal: alpbach, reith-im-alpbachtal, brixlegg, rattenberg, kramsach, kundl
brixental/kitzbueheler-alpen: hopfgarten, itter, brixen-im-thale, westendorf, kirchberg-in-tirol, kitzbuehel
kufsteinerland/wilder-kaiser: kufstein, soell, ellmau, koessen, walchsee, thiersee
inntal: woergl, jenbach, schwaz, wattens, hall-in-tirol, innsbruck
zillertal: fuegen, kaltenbach, zell-am-ziller, gerlos, mayrhofen, hintertux
Past geen van deze, gebruik dan `"place": ""`.

## Thema-slugs (veld `theme`; ook gegeven in de input)
wandelen, zwemmen, skieen, winterpret, fietsen, avontuur, dieren, cultuur, attracties, dagtochten, wellness, workshops, golf
