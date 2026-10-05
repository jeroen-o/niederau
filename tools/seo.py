#!/usr/bin/env python3
"""SEO en GEO voor Niederau.nl (draai na translate.py).

Per taalpagina:
- geo-metatags (regio, plaats, coördinaten), Open Graph-afbeelding, Twitter Card, robots
- JSON-LD @graph: WebSite, WebPage, TouristDestination (Niederau) met de vier dorpen,
  Hotel (partner) en FAQPage, opgebouwd uit de zichtbare FAQ op de pagina
Daarnaast llms.txt (samenvatting voor AI-zoekmachines) en sitemap.xml met lastmod.
Het script is idempotent: het vervangt het blok tussen <!-- SEO:START --> en <!-- SEO:END -->.
"""
import datetime, html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://niederau.nl"
TODAY = datetime.date.today().isoformat()
LAT, LON, ELEV = 47.4446, 12.0789, 828
OG_IMAGE = f"{BASE}/assets/img/niederau-wildschoenau-tirol-1200x630.jpg"

LANGS = {
    "nl": {"file": "index.html", "url": f"{BASE}/", "locale": "nl_NL",
           "region": "Niederau, Wildschönau, Tirol, Oostenrijk",
           "dest": "Bergdorp op 828 meter in de Wildschönau, Kitzbüheler Alpen, Tirol (Oostenrijk). Zonnig en sneeuwzeker; skiën, langlaufen, rodelen, wandelen en mountainbiken.",
           "villages": {"Niederau": "Eerste en meest toeristische dorp van de Wildschönau, met de gondel naar het Markbachjoch.",
                        "Oberau": "Bestuurlijk hart van de Wildschönau met de grote parochiekerk.",
                        "Auffach": "Achter in het dal, aan de voet van de Schatzberg en de verbinding met het Alpbachtal.",
                        "Thierbach": "Kleinste en hoogst gelegen dorp van de Wildschönau."},
           "hotel": "Familiebedrijf en viersterren-wellnesshotel in Niederau, met het skigebied vanaf de voordeur.",
           "img_alt": "Besneeuwde pistes en liften in Niederau, Wildschönau"},
    "en": {"file": "en/index.html", "url": f"{BASE}/en/", "locale": "en_GB",
           "region": "Niederau, Wildschönau, Tyrol, Austria",
           "dest": "Mountain village at 828 metres in the Wildschönau valley, Kitzbühel Alps, Tyrol (Austria). Sunny and snow-sure; skiing, cross-country skiing, tobogganing, hiking and mountain biking.",
           "villages": {"Niederau": "First and most visited village of the Wildschönau, with the gondola to the Markbachjoch.",
                        "Oberau": "Administrative heart of the Wildschönau with the large parish church.",
                        "Auffach": "At the far end of the valley, at the foot of the Schatzberg and the link to the Alpbach valley.",
                        "Thierbach": "Smallest and highest village of the Wildschönau."},
           "hotel": "Family-run four-star wellness hotel in Niederau, with ski-in access from the front door.",
           "img_alt": "Snowy slopes and lifts in Niederau, Wildschönau"},
    "de": {"file": "de/index.html", "url": f"{BASE}/de/", "locale": "de_DE",
           "region": "Niederau, Wildschönau, Tirol, Österreich",
           "dest": "Bergdorf auf 828 Metern in der Wildschönau, Kitzbüheler Alpen, Tirol (Österreich). Sonnig und schneesicher; Skifahren, Langlaufen, Rodeln, Wandern und Mountainbiken.",
           "villages": {"Niederau": "Erstes und touristischstes Dorf der Wildschönau, mit der Gondel zum Markbachjoch.",
                        "Oberau": "Verwaltungszentrum der Wildschönau mit der großen Pfarrkirche.",
                        "Auffach": "Hinten im Tal, am Fuß des Schatzbergs und der Verbindung ins Alpbachtal.",
                        "Thierbach": "Kleinstes und höchstgelegenes Dorf der Wildschönau."},
           "hotel": "Familienbetrieb und Vier-Sterne-Wellnesshotel in Niederau, Skigebiet ab der Haustür.",
           "img_alt": "Verschneite Pisten und Lifte in Niederau, Wildschönau"},
}


def text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def build(lang, cfg, page):
    title = text(re.search(r"<title>(.*?)</title>", page, re.S).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', page, re.S).group(1))
    faq = [{"@type": "Question", "name": text(q),
            "acceptedAnswer": {"@type": "Answer", "text": text(a)}}
           for q, a in re.findall(r"<details>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>", page, re.S)]
    graph = [
        {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": "Niederau.nl",
         "inLanguage": ["nl", "en", "de"], "publisher": {"@id": f"{BASE}/#organisatie"}},
        {"@type": "Organization", "@id": f"{BASE}/#organisatie", "name": "Niederau.nl", "url": f"{BASE}/",
         "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/icon-512.png", "width": 512, "height": 512}},
        {"@type": "WebPage", "@id": cfg["url"] + "#webpage", "url": cfg["url"], "name": title,
         "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"},
         "about": {"@id": f"{BASE}/#niederau"}, "dateModified": TODAY,
         "primaryImageOfPage": {"@type": "ImageObject", "url": OG_IMAGE}},
        {"@type": ["TouristDestination", "Place"], "@id": f"{BASE}/#niederau", "name": "Niederau",
         "description": cfg["dest"],
         "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON, "elevation": ELEV},
         "image": [f"{BASE}/assets/img/niederau-winter-bauernhuis-hero-2048.webp", f"{BASE}/assets/img/markbachjoch-bergmeer-zomer-hero-2048.webp", OG_IMAGE],
         "address": {"@type": "PostalAddress", "addressLocality": "Wildschönau", "postalCode": "6314",
                     "addressRegion": "Tirol", "addressCountry": "AT"},
         "containedInPlace": {"@type": "AdministrativeArea", "name": "Wildschönau",
                              "containedInPlace": {"@type": "AdministrativeArea", "name": "Tirol"}},
         "touristType": ["Wintersport", "Hiking", "Families"],
         "includesAttraction": [{"@type": "TouristAttraction", "name": n} for n in
                                ("Markbachjoch", "Lanerköpfl", "Ski Juwel Alpbachtal Wildschönau", "Kundler Klamm", "Rodelbahn Lanerköpfl", "Drachental", "Bergbauernmuseum z'Bach")]},
        {"@type": "ItemList", "name": "Wildschönau",
         "itemListElement": [{"@type": "ListItem", "position": i + 1,
                              "item": {"@type": "Place", "name": n, "description": d}}
                             for i, (n, d) in enumerate(cfg["villages"].items())]},
        {"@type": "Hotel", "@id": f"{BASE}/#hotel-wastlhof", "name": "Hotel Wastlhof",
         "description": cfg["hotel"], "url": "https://www.hotelwastlhof.at/",
         "telephone": "+43 5339 8247", "email": "info@hotelwastlhof.at",
         "starRating": {"@type": "Rating", "ratingValue": 4},
         "image": f"{BASE}/assets/img/hotel-wastlhof-niederau-zomer.webp",
         "address": {"@type": "PostalAddress", "streetAddress": "Wildschönauerstraße Niederau 206",
                     "postalCode": "6314", "addressLocality": "Wildschönau", "addressCountry": "AT"},
         "containedInPlace": {"@id": f"{BASE}/#niederau"}},
    ]
    if faq:
        graph.append({"@type": "FAQPage", "@id": cfg["url"] + "#faq", "inLanguage": lang, "mainEntity": faq})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return f'''<!-- SEO:START (gegenereerd door tools/seo.py) -->
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="AT-7">
<meta name="geo.placename" content="{cfg["region"]}">
<meta name="geo.position" content="{LAT};{LON}">
<meta name="ICBM" content="{LAT}, {LON}">
<meta property="og:site_name" content="Niederau.nl">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{cfg["img_alt"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<script type="application/ld+json">
{ld}
</script>
<!-- SEO:END -->'''


for lang, cfg in LANGS.items():
    path = ROOT / cfg["file"]
    page = path.read_text(encoding="utf-8")
    # oud losse JSON-LD-blok en eerder gegenereerd blok verwijderen
    page = re.sub(r"<!-- SEO:START.*?<!-- SEO:END -->\n?", "", page, flags=re.S)
    page = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", page, flags=re.S)
    block = build(lang, cfg, page)
    page = page.replace('<link rel="icon"', block + '\n<link rel="icon"', 1)
    path.write_text(page, encoding="utf-8")
    print("SEO/GEO bijgewerkt:", cfg["file"])

# sitemap met lastmod
urls = "".join(f'''  <url><loc>{c["url"]}</loc><lastmod>{TODAY}</lastmod>
    <xhtml:link rel="alternate" hreflang="nl" href="{BASE}/"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE}/en/"/>
    <xhtml:link rel="alternate" hreflang="de" href="{BASE}/de/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/en/"/>
    <image:image><image:loc>{BASE}/assets/img/niederau-winter-bauernhuis-hero-2048.webp</image:loc></image:image>
    <image:image><image:loc>{BASE}/assets/img/markbachjoch-bergmeer-zomer-hero-2048.webp</image:loc></image:image>
    <image:image><image:loc>{OG_IMAGE}</image:loc></image:image></url>
''' for c in LANGS.values())
(ROOT / "sitemap.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
{urls}</urlset>
''', encoding="utf-8")

# llms.txt: compacte, feitelijke samenvatting voor AI-zoekmachines (GEO)
(ROOT / "llms.txt").write_text(f"""# Niederau.nl

> Independent guide to Niederau, a mountain village at 828 m in the Wildschönau valley (Kitzbühel Alps, Tyrol, Austria). Available in Dutch, English and German. Last updated {TODAY}.

## Key facts
- Location: Niederau, municipality of Wildschönau, district of Kufstein, Tyrol, Austria ({LAT} N, {LON} E), about 15 minutes by road from Wörgl (A12, exit Wörgl-Ost).
- The Wildschönau consists of four church villages: Niederau, Oberau, Auffach and Thierbach, plus the hamlet of Mühltal. The valley won first prize from the ADAC in the "Klein & Fein" category.
- Winter: Markbachjochbahn gondola from Niederau to the Markbachjoch; ski area Ski Juwel Alpbachtal Wildschönau (145 km of slopes, 47 lifts, 24 ski huts, 3 snow parks); three toboggan runs in the valley, including the Lahnerköpfl run in Niederau; some 30–40 km of cross-country trails, with the Penningberg trail (12 km) starting in Niederau.
- Summer: more than 300 km of waymarked trails, (e-)mountain biking, alpine huts, the Kundler Klamm gorge walk; heated open-air pool between Niederau and Oberau with three basins and more than 1,000 m² of water; Talfest in August (rotating between Niederau, Oberau and Auffach).
- Wildschönau Premium Card (from participating accommodation): free use of the summer mountain lifts in Niederau and Auffach, hiking bus, open-air pools, Bergbauernmuseum z'Bach in Oberau and the Drachenclub for children aged 5–14.
- Local specialities: Krautinger (turnip schnapps), Kaiserschmarrn, Kaspressknödel, Tiroler Gröstl.
- Getting there: train to Wörgl Hbf, then regional bus; nearest airports Innsbruck, Salzburg, Munich. Austrian motorways require a vignette.
- Emergency numbers: 112 (general), 140 (mountain rescue).

## Things to do nearby (approx. driving time from Niederau)
- In the valley: Drachental family park with the Drachenflitzer alpine coaster (Oberau), Bergbauernmuseum z'Bach (Oberau), Kundler Klamm gorge walk to Kundl, sleigh rides, ice skating, ski touring, Krautinger tasting.
- Rattenberg, Austria's smallest town, glassblowers (~30 min); Kufstein fortress with the Heldenorgel at noon (~30 min); Hohe Salve above Hopfgarten (~30 min); Museum Tiroler Bauernhöfe in Kramsach (~30 min).
- Alpbach (~40 min, or on skis via Ski Juwel); Zillertal steam train from Jenbach (~40 min); Swarovski Kristallwelten in Wattens (~45 min); Kitzbühel (~45 min); Achensee (~50 min); Innsbruck with Goldenes Dachl, Nordkettenbahn and Alpenzoo (~1 hour).

## History
- 1193–1195: first written mention of the Wildschönau.
- 16th century: silver and copper mining on the Gratlspitz near Thierbach.
- 18th century: Empress Maria Theresa granted 51 farmers the right to distil Krautinger; around fifteen still use it.
- 1811: the Wildschönau became an independent municipality.
- Early 20th century: road through the Kundler Klamm to the Inn valley (covered wooden bridge 1913/14); today a footpath.
- 14 January 1947: the first chairlift in Tyrol opened in Niederau (Niederau–Markbachjoch), built by engineer Sepp Hochmuth; the start of tourism in the valley.
- 1995: an eight-seater gondola replaced the chairlift (today's Markbachjochbahn); 2022: 75th anniversary.
- 2008/09: on the Lanerköpfl (also Lahnerköpfl), Niederau's home mountain, a fast four-seater chairlift with bubble (843–1,560 m, 1,400 persons/hour) replaced the old single chairlift. Demanding north slopes (Hochberg run); natural toboggan run of almost 6 km (736 m descent, average 14%) from the top station past Gseng-Alm and Laner-Alm.

## Partner
- Hotel Wastlhof (partner of Niederau.nl): four-star wellness hotel run by the Brunner family for three generations, with indoor and year-round heated outdoor pool and its own riding stables (about 15 horses, including Haflingers), Wildschönauerstraße Niederau 206, 6314 Wildschönau, +43 5339 8247, info@hotelwastlhof.at, https://www.hotelwastlhof.at/

## Pages
- [Nederlands]({BASE}/): Niederau en de Wildschönau
- [English]({BASE}/en/): Niederau and the Wildschönau
- [Deutsch]({BASE}/de/): Niederau und die Wildschönau
""", encoding="utf-8")
print("sitemap.xml en llms.txt bijgewerkt")
