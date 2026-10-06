#!/usr/bin/env python3
"""Genereert de activiteiten-, thema-, plaats- en regiopagina's (NL/EN/DE) uit tools/data/*.
Draai via tools/build.sh. Bestanden onder activiteiten/, omgeving/, regio/ en en|de/... nooit los bewerken."""
import datetime, glob, html, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "tools" / "data"
BASE = "https://niederau.nl"
TODAY = datetime.date.today().isoformat()
LANGS = ("nl", "en", "de")
OG = f"{BASE}/assets/img/niederau-wildschoenau-tirol-1200x630.jpg"
e = html.escape

DIRS = {"guide": {"nl": "gids", "en": "guides", "de": "ratgeber"},
        "events": {"nl": "agenda", "en": "events", "de": "veranstaltungen"},
        "act": {"nl": "activiteiten", "en": "activities", "de": "aktivitaeten"},
        "place": {"nl": "omgeving", "en": "nearby", "de": "umgebung"},
        "region": {"nl": "regio", "en": "region", "de": "region"}}
PREFIX = {"nl": "", "en": "en/", "de": "de/"}

UI = {
 "skip": ("Naar de inhoud", "Skip to content", "Zum Inhalt"),
 "menu": ("Menu", "Menu", "Menü"),
 "nav_label": ("Hoofdmenu", "Main menu", "Hauptmenü"),
 "n_home": ("Het dorp", "The village", "Das Dorf"),
 "n_act": ("Activiteiten", "Activities", "Aktivitäten"),
 "n_place": ("Omgeving", "Around Niederau", "Umgebung"),
 "events_h": ("Terugkerende evenementen", "Recurring events", "Wiederkehrende Veranstaltungen"),
 "guides_h": ("Handige gidsen", "Useful guides", "Hilfreiche Ratgeber"),
 "n_about": ("Over deze site", "About this site", "Über diese Seite"),
 "n_guides": ("Gidsen", "Guides", "Ratgeber"),
 "read_more": ("Lees meer", "Read more", "Mehr lesen"),
 "updated": ("Laatst bijgewerkt", "Last updated", "Zuletzt aktualisiert"),
 "n_events": ("Agenda", "Events", "Veranstaltungen"),
 "n_mb": ("Markbachjoch", "Markbachjoch", "Markbachjoch"),
 "toggle_label": ("Wissel tussen zomer- en winterversie", "Switch between summer and winter version", "Zwischen Sommer- und Winterversion wechseln"),
 "toggle_s": ("☀ Zomer", "☀ Summer", "☀ Sommer"), "toggle_w": ("❄ Winter", "❄ Winter", "❄ Winter"),
 "lang_label": ("Taal", "Language", "Sprache"),
 "home": ("Niederau", "Niederau", "Niederau"),
 "f_about": ("Onafhankelijke gids over Niederau in de Wildschönau, Tirol.", "Independent guide to Niederau in the Wildschönau, Tyrol.", "Unabhängiger Reiseführer zu Niederau in der Wildschönau, Tirol."),
 "f_back": ("Terug naar de hoofdpagina", "Back to the main page", "Zurück zur Hauptseite"),
 "copy": ("Onafhankelijke site, niet verbonden aan officiële instanties.", "Independent site, not affiliated with official bodies.", "Unabhängige Seite, nicht mit offiziellen Stellen verbunden."),
 "credits": ("Foto’s: Wildschönau Tourismus, Ski Juwel Alpbachtal Wildschönau, Hotel Wastlhof en eigen foto’s.", "Photos: Wildschönau Tourismus, Ski Juwel Alpbachtal Wildschönau, Hotel Wastlhof and own photos.", "Fotos: Wildschönau Tourismus, Ski Juwel Alpbachtal Wildschönau, Hotel Wastlhof und eigene Fotos."),
 "tips": ("Tips", "Tips", "Tipps"),
 "practical": ("Praktisch", "Practical", "Praktisches"),
 "facts": ("In het kort", "At a glance", "Auf einen Blick"),
 "age": ("Leeftijd", "Age", "Alter"), "duration": ("Duur", "Duration", "Dauer"), "price": ("Kosten", "Cost", "Kosten"),
 "distance": ("Afstand", "Distance", "Entfernung"), "season": ("Seizoen", "Season", "Saison"), "location": ("Locatie", "Location", "Ort"),
 "website": ("Officiële website", "Official website", "Offizielle Website"),
 "check": ("Controleer tijden, prijzen en openingsdata altijd vooraf bij de aanbieder; ze kunnen veranderen.",
           "Always check times, prices and opening dates with the provider beforehand; they can change.",
           "Zeiten, Preise und Öffnungszeiten bitte immer vorab beim Anbieter prüfen; sie können sich ändern."),
 "more_theme": ("Meer in dit thema", "More in this theme", "Mehr zu diesem Thema"),
 "near": ("Plaats", "Place", "Ort"),
 "faq": ("Veelgestelde vragen", "Frequently asked questions", "Häufige Fragen"),
 "winter": ("Winter", "Winter", "Winter"), "summer": ("Zomer", "Summer", "Sommer"), "both": ("Hele jaar", "All year", "Ganzjährig"),
 "all_act": ("Alle activiteiten", "All activities", "Alle Aktivitäten"),
 "all_place": ("Alle plaatsen in de omgeving", "All places nearby", "Alle Orte in der Umgebung"),
 "act_here": ("Activiteiten in en rond deze plaats", "Things to do in and around here", "Aktivitäten in und um diesen Ort"),
 "highlights": ("Wat is er te doen?", "What to see and do", "Was gibt es zu sehen und zu tun?"),
 "getting": ("Vanaf Niederau", "From Niederau", "Ab Niederau"),
 "best_for": ("Geschikt voor", "Best for", "Geeignet für"),
 "drive": ("Rijtijd vanaf Niederau", "Drive from Niederau", "Fahrzeit ab Niederau"),
 "elev": ("Hoogte", "Elevation", "Höhe"),
 "region": ("Regio", "Region", "Region"),
 "places_in": ("Plaatsen in deze regio", "Places in this region", "Orte in dieser Region"),
 "winter_h": ("Wintersport en winteractiviteiten", "Winter", "Winter"),
 "summer_h": ("Zomeractiviteiten", "Summer", "Sommer"),
 "more_region": ("Meer plaatsen in", "More places in", "Weitere Orte in"),
 "overviews": ("Handige overzichten", "Handy overviews", "Praktische Übersichten"),
 "themes": ("Thema’s", "Themes", "Themen"),
 "regions": ("Regio’s", "Regions", "Regionen"),
 "n_act_count": ("activiteiten", "activities", "Aktivitäten"),
 "min": ("min.", "min.", "Min."),
 "ca": ("ca.", "approx.", "ca."),
 "stay_h": ("Verblijf in Niederau", "Stay in Niederau", "Übernachten in Niederau"),
 "stay_p": ("Hotel Wastlhof, partner van Niederau.nl, is een familiehotel met binnen- en buitenzwembad, wellness en een eigen paardenstal, midden in het dorp. Voor meer overnachtingen en informatie kun je ook terecht bij het toeristenbureau van de Wildschönau. Persoonlijke aanbeveling, zonder vergoeding.",
            "Hotel Wastlhof, partner of Niederau.nl, is a family-run hotel with an indoor and an outdoor pool, wellness and its own riding stables, right in the village. For more places to stay and information you can also contact the Wildschönau tourist office. Personal recommendation, no payment involved.",
            "Das Hotel Wastlhof, Partner von Niederau.nl, ist ein Familienhotel mit Hallen- und Freibad, Wellness und eigenem Reitstall, mitten im Dorf. Weitere Unterkünfte und Informationen gibt es auch beim Tourismusverband Wildschönau. Persönliche Empfehlung, ohne Vergütung."),
 "stay_hotel": ("Naar Hotel Wastlhof", "To Hotel Wastlhof", "Zum Hotel Wastlhof"),
 "stay_vvv": ("Toeristenbureau Wildschönau", "Wildschönau tourist office", "Tourismusverband Wildschönau"),
 "stay_more": ("Meer over verblijven in Niederau", "More about staying in Niederau", "Mehr zu Unterkünften in Niederau"),
 "partner": ("Partner", "Partner", "Partner"),
 "act_in_theme": ("Activiteiten", "Activities", "Aktivitäten"),
}
def ui(k, lang): return UI[k][LANGS.index(lang)]


# ---------- foto-keuze uit eigen fotobibliotheek ----------
PHOTOS = json.load(open(ROOT / "tools" / "photo_catalog.json", encoding="utf-8"))
LOCAL_PLACES = {"niederau", "oberau", "auffach", "thierbach", "muehltal"}
LOCAL_WORDS = ("wildschönau", "niederau", "markbachjoch", "schatzberg", "auffach", "oberau", "thierbach", "mühltal", "kundler", "wastlhof")
WINTER_F = ("ski", "snow", "sneeuw", "winter", "pistes", "langlauf", "oefenlift", "lanerk", "snowboard")
SUMMER_F = ("wandel", "bloemen", "e-bike", "paard", "bergmeertje", "openluchtzwembad", "lente", "herfst", "alpenbloemen", "lama", "zomer", "krauting", "talfest", "sterren", "kapel", "brettljause", "premium")

def is_local(a):
    text = " ".join([L(a.get("title", {}), "nl"), L(a.get("tagline", {}), "nl")]).lower()
    return a.get("place") in LOCAL_PLACES or (not a.get("place") and any(w in text for w in LOCAL_WORDS))

def photo_for(a):
    """Beste eigen foto voor een activiteit in/bij Wildschönau; None als er geen passende is."""
    text = " ".join([L(a.get("title", {}), "nl"), L(a.get("tagline", {}), "nl"), a.get("theme", "")]).lower()
    local = a.get("place") in LOCAL_PLACES or (not a.get("place") and any(w in text for w in LOCAL_WORDS))
    if not local: return None
    best, score = [], 0
    for f, alts, kws, hotel in PHOTOS:
        if hotel != ("wastlhof" in text): continue
        w = any(k in f for k in WINTER_F); su = any(k in f for k in SUMMER_F)
        if hotel: w, su = "winter" in f, "zomer" in f
        if w and not su and a["season"] != "winter": continue
        if su and not w and a["season"] != "summer": continue
        sc = sum(1 for k in kws if k in text)
        if hotel:
            sc = 1 + (1 if "zwembad" in text and "zwembad" in f else 0) + (1 if ("wellness" in text or " spa" in text) and "wellness" in f else 0)
        if sc > score: best, score = [(f, alts, hotel)], sc
        elif sc == score and sc > 0: best.append((f, alts, hotel))
    if not best: return None
    return best[sum(map(ord, a["id"])) % len(best)]

def photo_html(f, lang):
    for ff, alts, _k, h in PHOTOS:
        if ff == f: return f'<img class="side-img" src="/assets/img/{f}.webp" width="1000" height="667" loading="lazy" alt="{e(alts[LANGS.index(lang)])}">'
    return ""

PLACE_PHOTO = {"oberau": "oberau-wildschoenau-winter", "thierbach": "thierbach-wildschoenau-sneeuwschoenwandelen", "auffach": "auffach-wildschoenau-e-bike", "muehltal": "muehltal-herfst-wandelen-gezin"}
REGION_PHOTO = {"wildschoenau": "niederau-wildschoenau-pistes-liften-winter"}

# thema-afbeeldingen (bestaande eigen/hotelfoto's) met beschrijvende alt
THEME_IMG = {
 "wandelen": ("wildschoenau-wandelpad-alm", ("Wandelpad door de weiden naar een alm", "Footpath through the meadows to an alpine hut", "Wanderweg über die Wiesen zu einer Alm")),
 "zwemmen": ("niederau-openluchtzwembad", ("Openluchtzwembad in Niederau", "Open-air pool in Niederau", "Freibad in Niederau")),
 "skieen": ("niederau-skien-markbachjoch", ("Skiërs op de zonnige pistes van het Markbachjoch", "Skiers on the sunny slopes of the Markbachjoch", "Skifahrer auf den sonnigen Pisten des Markbachjochs")),
 "winterpret": ("wildschoenau-langlaufloipe", ("Langlaufloipe in het dal", "Cross-country trail in the valley", "Langlaufloipe im Tal")),
 "fietsen": ("wildschoenau-e-bike-dal", ("Op de e-bike door het dal", "E-biking through the valley", "Mit dem E-Bike durchs Tal")),
 "avontuur": ("wildschoenau-bergmeertje", ("Bergmeertje in de Wildschönau", "Mountain lake in the Wildschönau", "Bergsee in der Wildschönau")),
 "dieren": ("wildschoenau-boerderijdieren-lama", ("Lama bij een boerderij", "Llama at a farm", "Lama auf einem Bauernhof")),
 "cultuur": ("niederau-talfest-optocht", ("Optocht tijdens het dalfeest in Niederau", "Parade during the valley festival in Niederau", "Umzug beim Talfest in Niederau")),
 "attracties": ("wildschoenau-premium-card-zomer", ("Zomerse dag in de Wildschönau", "A summer day in the Wildschönau", "Ein Sommertag in der Wildschönau")),
 "dagtochten": ("schoenangeralm-kapel-wildschoenau", ("Kapel bij de Schönangeralm", "Chapel near the Schönangeralm", "Kapelle bei der Schönangeralm")),
 "wellness": ("hotel-wastlhof-niederau-wellness", ("Wellnessruimte van Hotel Wastlhof", "Wellness area at Hotel Wastlhof", "Wellnessbereich des Hotels Wastlhof")),
 "workshops": ("tiroler-kaiserschmarrn", ("Tiroler Kaiserschmarrn", "Tyrolean Kaiserschmarrn", "Tiroler Kaiserschmarrn")),
 "golf": ("niederau-lente-bloemenweide", ("Groene bloemenweide in Niederau", "Green flower meadow in Niederau", "Grüne Blumenwiese in Niederau")),
}

def L(d, lang, default=""):
    if isinstance(d, dict):
        return d.get(lang) or d.get("nl") or default
    return d or default

def paras(text):
    return [p.strip() for p in (text or "").split("\n\n") if p.strip()]

def jload(pattern):
    out = []
    for f in sorted(glob.glob(str(DATA / pattern))):
        try:
            out += json.load(open(f, encoding="utf-8"))
        except Exception as ex:
            print("FOUT in", f, ex)
    return out

import unicodedata as _ud, re as _re0
def _slugify(x):
    x = _ud.normalize("NFKD", x).encode("ascii", "ignore").decode().lower()
    return "-".join(_re0.sub(r"[^a-z0-9]+", "-", x).strip("-").split("-")[:7])

def trim_desc(d, n=158):
    d = " ".join(d.split())
    if len(d) <= n: return d
    cut = d[:n - 1].rsplit(" ", 1)[0].rstrip(" ,;:.-")
    return cut + "…"

# ---------- data laden ----------
src = {o["id"]: o for o in json.load(open(DATA / "source_activities.json", encoding="utf-8"))}
EXCL = set(json.load(open(DATA / "exclude.json", encoding="utf-8"))["ids"]) if (DATA / "exclude.json").exists() else set()
PATCH = {}
for pt in jload("patches/*.json"):
    PATCH[pt.get("id") or pt.get("slug")] = pt
THEME_FIX = {"s224": "attracties", "s59": "attracties", "s223": "avontuur", "s77": "avontuur", "s97": "avontuur", "s100": "zwemmen", "s207": "attracties", "s189": "fietsen", "s295": "dieren", "s217": "dieren", "s182": "dieren"}
HARD = set(json.load(open(DATA / "exclude.json", encoding="utf-8")).get("hard", []))
acts = []
for a in jload("acts/*.json"):
    if a["id"] in HARD: continue
    patched = a["id"] in PATCH
    a = PATCH.get(a["id"], a)
    if a.get("drop") or (a["id"] in EXCL and not (patched and a.get("verified") is True)): continue
    s = src.get(a["id"])
    a["theme"] = THEME_FIX.get(a["id"]) or a.get("theme") or (s["theme"] if s else "avontuur")
    a["season"] = a.get("season") or (s["season"] if s else "summer")
    a["slug_nl"] = a.get("slug_nl") or (s["slug_nl"] if s else a["id"])
    a["title"] = a.get("title") or {}
    if not L(a["title"], "nl") and s: a["title"] = {"nl": s["src"]["t"]}
    acts.append(a)
_ids = {a["id"] for a in acts}
for k, pt in PATCH.items():
    if pt.get("id") and pt["id"] not in _ids and not pt.get("drop") and pt.get("new"):
        pt.setdefault("theme", "golf"); pt.setdefault("season", "summer")
        if not pt.get("slug_nl"): pt["slug_nl"] = _slugify(L(pt.get("title", {}), "nl")) or pt["id"]
        acts.append(pt)
places = [PATCH.get(p["slug"], p) for p in jload("places/*.json")]
places = [p for p in places if not p.get("drop") and p.get("verified") is not False]
tdata = jload("themes/*.json")
themes = {t["theme"]: t for t in tdata if t.get("kind") == "theme"}
regions = {t["region"]: t for t in tdata if t.get("kind") == "region"}
hubs = {t["scope"]: t for t in tdata if t.get("kind") == "hub"}
REGION_ORDER = ["wildschoenau", "alpbachtal", "brixental", "kufsteinerland", "inntal", "zillertal"]
place_by = {p["slug"]: p for p in places}
import re as _re
def _norm(x): return _re.sub(r"[^a-z]", "", x.lower().replace("ö", "o").replace("ü", "u").replace("ä", "a"))
_names = {p["slug"]: _norm(L(p["name"], "nl")) for p in places}
for _a in acts:
    if not _a.get("place"):
        _t = _norm(" ".join([L(_a.get("title", {}), "nl"), L(_a.get("location", {}), "nl")]))
        for _slug, _n in _names.items():
            if _n and len(_n) > 4 and _n in _t:
                _a["place"] = _slug
                break

def tslug(theme, lang):
    t = themes.get(theme, {})
    return t.get("slug_" + lang) or (theme if lang == "nl" else theme)

def aslug(a, lang):
    return a.get("slug_" + lang) or a["slug_nl"]

# uniek maken per (taal, thema)
for lang in LANGS:
    seen = set()
    for a in acts:
        s = aslug(a, lang); base = s; n = 2
        while (a["theme"], s) in seen:
            s = f"{base}-{n}"; n += 1
        seen.add((a["theme"], s)); a["slug_" + lang] = s

# ---------- URL's ----------
def u_hub(kind, lang): return f"/{PREFIX[lang]}{DIRS[kind][lang]}/"
def u_theme(theme, lang): return f"/{PREFIX[lang]}{DIRS['act'][lang]}/{tslug(theme, lang)}/"
def u_act(a, lang): return f"{u_theme(a['theme'], lang)}{a['slug_' + lang]}/"
def u_place(p, lang): return f"/{PREFIX[lang]}{DIRS['place'][lang]}/{p['slug']}/"
def u_region(r, lang): return f"/{PREFIX[lang]}{DIRS['region'][lang]}/{r}/"
STAY_URL = {"nl": "/#verblijf", "en": "/en/#stay", "de": "/de/#unterkunft"}
def home(lang): return "/" if lang == "nl" else f"/{lang}/"

registry = []  # (key, {lang: url}, lastmod)


def main_nav(lang):
    """Zelfde hoofdmenu als de hoofdpagina (uit de gebouwde index van die taal); Activiteiten wijst naar de hub."""
    f = ROOT / (PREFIX[lang] + "index.html")
    t = f.read_text(encoding="utf-8")
    nav = t[t.index('<nav class="nav"'):t.index('<button class="season-toggle"')]
    out = []
    for href, label in _re0.findall(r'<a href="([^"]+)">([^<]+)</a>', nav):
        if href.startswith("#"):
            url_ = f"{home(lang)}{href}"
            if href[1:] in ("activiteiten", "activities", "aktivitaeten"): url_ = u_hub("act", lang)
        else:
            url_ = f"/{PREFIX[lang]}{href}"
        out.append(f'<a href="{url_}">{label}</a>')
    return "\n      ".join(out)

def shell(lang, key, urls, title, desc, body, ld_graph, og_type="article", img=None):
    """key identificeert de pagina in alle talen; urls = {lang: pad}."""
    here = BASE + urls[lang]
    desc = trim_desc(desc)
    if len(title) > 70: title = title.replace(" | Niederau.nl", "")
    hl = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{BASE}{urls[c]}">' for c in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{urls["nl"]}">'
    cur = lambda c: ' aria-current="true"' if c == lang else ""
    lang_nav = "".join(f'<a href="{urls[c]}" hreflang="{c}" lang="{c}"{cur(c)}>{c.upper()}</a>' for c in LANGS)
    locale = {"nl": "nl_NL", "en": "en_GB", "de": "de_DE"}[lang]
    imgurl = f"{BASE}/assets/img/{img}.webp" if img else OG
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": "Niederau.nl", "inLanguage": ["nl", "en", "de"]}] + ld_graph}, ensure_ascii=False, indent=1)
    tog = f'<button class="season-toggle" type="button" aria-label="{e(ui("toggle_label", lang))}" title="{e(ui("toggle_label", lang))}"><span data-only="winter">{ui("toggle_s", lang)}</span><span data-only="summer">{ui("toggle_w", lang)}</span></button>'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{here}">
{hl}
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="{locale}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{here}">
<meta name="theme-color" content="#efece7">
<!-- SEO:START (gegenereerd door tools/pages.py) -->
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="AT-7">
<meta name="geo.placename" content="Niederau, Wildschönau, Tirol, Austria">
<meta name="geo.position" content="47.4446;12.0789">
<meta name="ICBM" content="47.4446, 12.0789">
<meta property="og:site_name" content="Niederau.nl">
<meta property="og:image" content="{imgurl}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{imgurl}">
<script type="application/ld+json">
{ld}
</script>
<!-- SEO:END -->
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-48.png" sizes="48x48" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="/assets/style.css">
<script>
  (function () {{ var m = new Date().getMonth(); document.documentElement.setAttribute('data-season', (m >= 9 || m <= 2) ? 'winter' : 'summer'); }})();
</script>
</head>
<body>
<a class="skip" href="#main">{ui("skip", lang)}</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{home(lang)}">
      <svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#b5222b"/><circle cx="46" cy="18" r="7" fill="#f5d27a"/><path d="M4 52 22 24l9 12 8-10 21 26z" fill="#fbfaf6"/></svg>
      <span>Niederau<small>Wildschönau · {"Tyrol" if lang == "en" else "Tirol"}</small></span>
    </a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">{ui("menu", lang)}</button>
    <nav class="nav" id="nav" aria-label="{ui("nav_label", lang)}">
      {main_nav(lang)}
      {tog}
      <div class="lang" role="group" aria-label="{ui("lang_label", lang)}">{lang_nav}</div>
    </nav>
  </div>
</header>
<main id="main">
<div class="page-hero" aria-hidden="true"></div>
{body}
<section aria-labelledby="h-stay"><div class="wrap"><div class="card stay-card"><h2 id="h-stay">{ui("stay_h", lang)} <span class="chip">{ui("partner", lang)}</span></h2><p>{ui("stay_p", lang)}</p><p><a href="https://www.hotelwastlhof.at/" rel="noopener" target="_blank">{ui("stay_hotel", lang)}</a> · <a href="https://www.wildschoenau.com/" rel="noopener" target="_blank">{ui("stay_vvv", lang)}</a> · <a href="{STAY_URL[lang]}">{ui("stay_more", lang)}</a></p></div></div></section>
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <h3>Niederau.nl</h3>
      <p>{ui("f_about", lang)}</p>
      <div class="lang" role="group" aria-label="{ui("lang_label", lang)}">{lang_nav}</div>
    </div>
    <div>
      <h3>Niederau</h3>
      <ul>
        <li><a href="{home(lang)}">{ui("f_back", lang)}</a></li>
        <li><a href="{u_hub("act", lang)}">{ui("n_act", lang)}</a></li>
        <li><a href="{u_hub("place", lang)}">{ui("n_place", lang)}</a></li>
        <li><a href="{u_events(lang)}">{ui("n_events", lang)}</a></li>
        <li><a href="{u_guides(lang)}">{ui("n_guides", lang)}</a></li>
        <li><a href="{u_about(lang)}">{ui("n_about", lang)}</a></li>
        <li><a href="/{PREFIX[lang]}markbachjoch/">{ui("n_mb", lang)}</a></li>
      </ul>
    </div>
    <p class="credits">{ui("credits", lang)}</p>
    <p class="updated">{ui("updated", lang)}: <time datetime="@@LASTMOD@@">@@LASTMOD_H@@</time></p>
    <p class="copyright">© <span data-year>{TODAY[:4]}</span> Niederau.nl · {ui("copy", lang)}</p>
  </div>
</footer>
<script src="/assets/main.js" defer></script>
</body>
</html>
'''

def crumbs(lang, items):
    """items: [(naam, url)] zonder Niederau; laatste zonder link."""
    parts = [f'<a href="{home(lang)}">Niederau</a>'] + [f'<a href="{u}">{e(n)}</a>' for n, u in items[:-1]] + [f'<span aria-current="page">{e(items[-1][0])}</span>']
    ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u}
        for i, (n, u) in enumerate([("Niederau", home(lang))] + items)]}
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " › ".join(parts) + "</nav>", ld

def faq_html(faq, lang):
    items = [(L(f["q"], lang), L(f["a"], lang)) for f in (faq or []) if f.get("q") and f.get("a")]
    if not items: return "", None
    h = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in items)
    ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return f'<section class="alt" aria-labelledby="h-faq"><div class="wrap"><h2 id="h-faq">{ui("faq", lang)}</h2><div class="faq">{h}</div></div></section>', ld

def card_list(items, lang):
    """items: [(titel, tagline, url, badge)]"""
    out = []
    for t, tag, url, badge in items:
        b = f'<span class="chip">{e(badge)}</span> ' if badge else ""
        out.append(f'<article class="card"><h3><a href="{url}">{e(t)}</a></h3><p>{b}{e(tag)}</p></article>')
    return '<div class="grid grid-3">' + "".join(out) + "</div>"

def write(url, content):
    rel = url.strip("/")
    p = ROOT / rel / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def season_badge(a, lang): return ui(a["season"], lang)

# ---------- pagina's ----------
def build_act(a):
    urls = {l: u_act(a, l) for l in LANGS}
    for lang in LANGS:
        title_n = L(a["title"], lang)
        th = themes.get(a["theme"], {})
        th_name = L(th.get("title", {}), lang, a["theme"]) if th else a["theme"]
        th_short = th_name
        p = place_by.get(a.get("place") or "")
        cr, cr_ld = crumbs(lang, [(ui("n_act", lang), u_hub("act", lang)), (th_short, u_theme(a["theme"], lang)), (title_n, urls[lang])])
        f = a.get("facts") or {}
        rows = []
        for k in ("age", "duration", "price", "distance", "season"):
            v = L(f.get(k, {}), lang) if f.get(k) else ""
            if v: rows.append(f"<li><strong>{ui(k, lang)}</strong><span>{e(v)}</span></li>")
        loc = L(a.get("location", {}), lang)
        if loc: rows.append(f"<li><strong>{ui('location', lang)}</strong><span>{e(loc)}</span></li>")
        facts = f'<ul class="facts" aria-label="{ui("facts", lang)}">{"".join(rows)}</ul>' if rows else ""
        intro = "".join(f"<p>{e(x)}</p>" for x in paras(L(a.get("intro", {}), lang)))
        tips = L(a.get("tips", {}), lang, [])
        tips_h = f'<h2>{ui("tips", lang)}</h2><ul class="check">' + "".join(f"<li>{e(x)}</li>" for x in tips) + "</ul>" if tips else ""
        pr = L(a.get("practical", {}), lang)
        pr_h = f'<h2>{ui("practical", lang)}</h2><p>{e(pr)}</p>' if pr else ""
        link = f'<p><a href="{e(a["url"])}" rel="noopener" target="_blank">{ui("website", lang)}</a></p>' if a.get("url") else ""
        pl = f'<p>{ui("near", lang)}: <a href="{u_place(p, lang)}">{e(L(p["name"], lang))}</a></p>' if p else ""
        rel = [x for x in acts if x is not a and x["theme"] == a["theme"]]
        rel.sort(key=lambda x: (x.get("place") != a.get("place"), x["season"] != a["season"], x["id"]))
        rel_h = ""
        if rel[:6]:
            rel_h = f'<section class="alt"><div class="wrap"><h2>{ui("more_theme", lang)}</h2>' + card_list([(L(x["title"], lang), L(x.get("tagline", {}), lang), u_act(x, lang), season_badge(x, lang)) for x in rel[:6]], lang) + f'<p><a href="{u_theme(a["theme"], lang)}">{ui("all_act", lang)} →</a></p></div></section>'
        faq_s, faq_ld = faq_html(a.get("faq"), lang)
        ph = photo_for(a)
        if ph: img, alt = ph[0], tuple(ph[1])
        elif is_local(a):
            gen = "niederau-wildschoenau-pistes-liften-winter" if a["season"] == "winter" else "wildschoenau-wandelpad-alm"
            img, alt = next((f, tuple(al)) for f, al, _k, _h in PHOTOS if f == gen)
        else: img, alt = None, ("", "", "")
        side = f'<img class="side-img" src="/assets/img/{img}.webp" width="1000" height="667" loading="lazy" alt="{e(alt[LANGS.index(lang)])}">' if img else ""
        body = f'''<section aria-labelledby="h-top"><div class="wrap split" style="align-items:start">
<div>{cr}<p class="eyebrow">{e(th_short)} · {season_badge(a, lang)}</p><h1 id="h-top">{e(title_n)}</h1><p class="lead">{e(L(a.get("tagline", {}), lang))}</p>{intro}{pl}{link}</div>
<div>{facts}{side}</div></div></section>
<section class="alt"><div class="wrap split" style="align-items:start"><div>{tips_h}</div><div>{pr_h}<p class="note">{ui("check", lang)}</p></div></div></section>
{faq_s}{rel_h}{guides_block(lang, GUIDE_BY_THEME.get(a["theme"], []))}'''
        desc = (L(a.get("tagline", {}), lang) + " " + " ".join(paras(L(a.get("intro", {}), lang)))[:170]).strip()[:300]
        ld_graph = [
            {"@type": "WebPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": title_n, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": "@@LASTMOD@@", "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
            dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"}),
            {"@type": ["TouristAttraction", "Place"], "name": title_n, "description": L(a.get("tagline", {}), lang), "url": BASE + urls[lang],
             **({"sameAs": a["url"]} if a.get("url") else {}),
             **({"image": f"{BASE}/assets/img/{img}.webp"} if img else {}),
             "containedInPlace": {"@type": "Place", "name": (L(p["name"], lang) if p else "Wildschönau") + ", Tirol, Austria"}},
        ] + ([dict(faq_ld, **{"@id": BASE + urls[lang] + "#faq"})] if faq_ld else [])
        write(urls[lang], shell(lang, a["id"], urls, f"{title_n} | Niederau.nl", desc, body, ld_graph, img=img))
    registry.append((a["id"], urls, img))

def build_place(p):
    urls = {l: u_place(p, l) for l in LANGS}
    for lang in LANGS:
        name = L(p["name"], lang)
        reg = regions.get(p.get("region"))
        reg_name = L(reg["name"], lang) if reg else ""
        items = [(ui("n_place", lang), u_hub("place", lang))]
        if reg: items.append((reg_name, u_region(p["region"], lang)))
        items.append((name, urls[lang]))
        cr, cr_ld = crumbs(lang, items)
        rows = []
        if p.get("drive_min"): rows.append(f"<li><strong>{ui('drive', lang)}</strong><span>{ui('ca', lang)} {p['drive_min']} {ui('min', lang)}</span></li>")
        if p.get("elevation_m"): rows.append(f"<li><strong>{ui('elev', lang)}</strong><span>{p['elevation_m']} m</span></li>")
        if reg_name: rows.append(f"<li><strong>{ui('region', lang)}</strong><span><a href=\"{u_region(p['region'], lang)}\">{e(reg_name)}</a></span></li>")
        bf = L(p.get("best_for", {}), lang)
        if bf: rows.append(f"<li><strong>{ui('best_for', lang)}</strong><span>{e(bf)}</span></li>")
        facts = f'<ul class="facts" aria-label="{ui("facts", lang)}">{"".join(rows)}</ul>' if rows else ""
        intro = "".join(f"<p>{e(x)}</p>" for x in paras(L(p.get("intro", {}), lang)))
        hl = L(p.get("highlights", {}), lang, [])
        hl_h = f'<h2>{ui("highlights", lang)}</h2><ul class="check">' + "".join(f"<li>{e(x)}</li>" for x in hl) + "</ul>" if hl else ""
        gt = L(p.get("getting_there", {}), lang)
        gt_h = f'<h2>{ui("getting", lang)}</h2><p>{e(gt)}</p>' if gt else ""
        link = f'<p><a href="{e(p["url"])}" rel="noopener" target="_blank">{ui("website", lang)}</a></p>' if p.get("url") else ""
        here_acts = [a for a in acts if a.get("place") == p["slug"]]
        act_h = ""
        if here_acts:
            act_h = f'<section class="alt"><div class="wrap"><h2>{ui("act_here", lang)}</h2>' + card_list([(L(x["title"], lang), L(x.get("tagline", {}), lang), u_act(x, lang), season_badge(x, lang)) for x in here_acts], lang) + "</div></section>"
        faq_s, faq_ld = faq_html(p.get("faq"), lang)
        sib = [x for x in places if x.get("region") == p.get("region") and x["slug"] != p["slug"]][:8]
        sib_h = ""
        if sib:
            sib_h = f'<section class="alt"><div class="wrap"><h2>{ui("more_region", lang)} {e(reg_name)}</h2>' + card_list([(L(x["name"], lang), L(x.get("tagline", {}), lang), u_place(x, lang), "") for x in sib], lang) + f'<p><a href="{u_region(p["region"], lang)}">{e(reg_name)} →</a></p></div></section>' if reg else ""
        body = f'''<section aria-labelledby="h-top"><div class="wrap split" style="align-items:start">
<div>{cr}<p class="eyebrow">{e(reg_name)}</p><h1 id="h-top">{e(name)}</h1><p class="lead">{e(L(p.get("tagline", {}), lang))}</p>{intro}{link}</div>
<div>{facts}{photo_html(PLACE_PHOTO.get(p["slug"], ""), lang) if PLACE_PHOTO.get(p["slug"]) else ""}</div></div></section>
<section class="alt"><div class="wrap split" style="align-items:start"><div>{hl_h}</div><div>{gt_h}<p class="note">{ui("check", lang)}</p></div></div></section>
{act_h}{faq_s}{sib_h}{guides_block(lang, PLACE_GUIDES)}'''
        desc = (L(p.get("tagline", {}), lang) + " " + " ".join(paras(L(p.get("intro", {}), lang)))[:170]).strip()[:300]
        ld_graph = [
            {"@type": "WebPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": "@@LASTMOD@@", "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
            dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"}),
            {"@type": ["TouristDestination", "Place"], "name": name, "description": L(p.get("tagline", {}), lang), "url": BASE + urls[lang],
             **({"sameAs": p["url"]} if p.get("url") else {}),
             "containedInPlace": {"@type": "AdministrativeArea", "name": "Tirol, Austria"}},
        ] + ([dict(faq_ld, **{"@id": BASE + urls[lang] + "#faq"})] if faq_ld else [])
        write(urls[lang], shell(lang, p["slug"], urls, f"{name}: {L(p.get('tagline', {}), lang)} | Niederau.nl"[:90] if False else f"{name} – {ui('n_place', lang)} Niederau | Niederau.nl", desc, body, ld_graph))
    registry.append(("place:" + p["slug"], urls, None))

def build_region(r):
    d = regions[r]
    urls = {l: u_region(r, l) for l in LANGS}
    ps = [p for p in places if p.get("region") == r]
    for lang in LANGS:
        name = L(d["name"], lang)
        cr, cr_ld = crumbs(lang, [(ui("n_place", lang), u_hub("place", lang)), (name, urls[lang])])
        intro = "".join(f"<p>{e(x)}</p>" for x in paras(L(d.get("intro", {}), lang)))
        hl = L(d.get("highlights", {}), lang, [])
        hl_h = f'<h2>{ui("highlights", lang)}</h2><ul class="check">' + "".join(f"<li>{e(x)}</li>" for x in hl) + "</ul>" if hl else ""
        gt = L(d.get("getting_there", {}), lang)
        gt_h = f'<h2>{ui("getting", lang)}</h2><p>{e(gt)}</p>' if gt else ""
        pl_h = ""
        if ps:
            pl_h = f'<section class="alt"><div class="wrap"><h2>{ui("places_in", lang)}</h2>' + card_list([(L(p["name"], lang), L(p.get("tagline", {}), lang), u_place(p, lang), "") for p in ps], lang) + "</div></section>"
        faq_s, faq_ld = faq_html(d.get("faq"), lang)
        body = f'''<section aria-labelledby="h-top"><div class="wrap split" style="align-items:start">
<div>{cr}<p class="eyebrow">{ui("region", lang)}</p><h1 id="h-top">{e(name)}</h1><p class="lead">{e(L(d.get("tagline", {}), lang))}</p>{intro}</div>
<div>{photo_html(REGION_PHOTO.get(r, ""), lang) if REGION_PHOTO.get(r) else ""}{hl_h}{gt_h}</div></div></section>
{pl_h}{faq_s}'''
        desc = (L(d.get("tagline", {}), lang) + " " + " ".join(paras(L(d.get("intro", {}), lang)))[:170]).strip()[:300]
        ld_graph = [
            {"@type": "WebPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": "@@LASTMOD@@", "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
            dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"}),
            {"@type": ["TouristDestination", "Place"], "name": name, "description": L(d.get("tagline", {}), lang), "url": BASE + urls[lang]},
        ] + ([dict(faq_ld, **{"@id": BASE + urls[lang] + "#faq"})] if faq_ld else [])
        write(urls[lang], shell(lang, "region:" + r, urls, f"{name} – {ui('n_place', lang)} Niederau | Niederau.nl", desc, body, ld_graph))
    registry.append(("region:" + r, urls, None))

def build_theme(t):
    d = themes[t]
    urls = {l: u_theme(t, l) for l in LANGS}
    ta = [a for a in acts if a["theme"] == t]
    for lang in LANGS:
        name = L(d["title"], lang)
        cr, cr_ld = crumbs(lang, [(ui("n_act", lang), u_hub("act", lang)), (name, urls[lang])])
        intro = "".join(f"<p>{e(x)}</p>" for x in paras(L(d.get("intro", {}), lang)))
        secs = "".join(f'<h2>{e(L(s["h"], lang))}</h2><p>{e(L(s["p"], lang))}</p>' for s in d.get("sections", []))
        tips = L(d.get("tips", {}), lang, [])
        tips_h = f'<h2>{ui("tips", lang)}</h2><ul class="check">' + "".join(f"<li>{e(x)}</li>" for x in tips) + "</ul>" if tips else ""
        lists = ""
        for season in ("winter", "summer"):
            sub = [a for a in ta if a["season"] == season]
            if sub:
                lists += f'<h2>{ui(season + "_h", lang)}</h2>' + card_list([(L(x["title"], lang), L(x.get("tagline", {}), lang), u_act(x, lang), "") for x in sub], lang)
        lists = f'<section class="alt"><div class="wrap">{lists}</div></section>' if lists else ""
        faq_s, faq_ld = faq_html(d.get("faq"), lang)
        img, alt = THEME_IMG.get(t, (None, ("", "", "")))
        side = f'<img class="side-img" src="/assets/img/{img}.webp" width="1000" height="667" loading="lazy" alt="{e(alt[LANGS.index(lang)])}">' if img else ""
        body = f'''<section aria-labelledby="h-top"><div class="wrap split" style="align-items:start">
<div>{cr}<p class="eyebrow">{ui("n_act", lang)}</p><h1 id="h-top">{e(name)}</h1><p class="lead">{e(L(d.get("tagline", {}), lang))}</p>{intro}</div>
<div>{side}{tips_h}</div></div></section>
<section><div class="wrap">{secs}</div></section>
{lists}{faq_s}{guides_block(lang, GUIDE_BY_THEME.get(t, []))}'''
        desc = (L(d.get("tagline", {}), lang) + " " + " ".join(paras(L(d.get("intro", {}), lang)))[:170]).strip()[:300]
        ld_graph = [
            {"@type": "CollectionPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": "@@LASTMOD@@", "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
            dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"}),
            {"@type": "ItemList", "name": name, "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + u_act(x, lang), "name": L(x["title"], lang)} for i, x in enumerate(ta)]},
        ] + ([dict(faq_ld, **{"@id": BASE + urls[lang] + "#faq"})] if faq_ld else [])
        write(urls[lang], shell(lang, "theme:" + t, urls, f"{name} | Niederau.nl", desc, body, ld_graph, img=img))
    registry.append(("theme:" + t, urls, None))

def build_hub(kind):
    d = hubs.get("activities" if kind == "act" else "places", {})
    urls = {l: u_hub(kind, l) for l in LANGS}
    for lang in LANGS:
        name = L(d.get("title", {}), lang, ui("n_act" if kind == "act" else "n_place", lang))
        cr, cr_ld = crumbs(lang, [(name, urls[lang])])
        intro = "".join(f"<p>{e(x)}</p>" for x in paras(L(d.get("intro", {}), lang)))
        if kind == "act":
            cards = []
            for t in themes:
                n = len([a for a in acts if a["theme"] == t])
                cards.append((L(themes[t]["title"], lang), L(themes[t].get("tagline", {}), lang), u_theme(t, lang), f"{n} {ui('n_act_count', lang)}"))
            ov = card_list([(COLL[c]["title"][LANGS.index(lang)], COLL[c]["tagline"][LANGS.index(lang)], u_coll(c, lang), f"{len(coll_acts(c))} {ui('n_act_count', lang)}") for c in COLL], lang)
            gd = card_list([(L(g["title"], lang), L(g.get("tagline", {}), lang), u_guide(g, lang), "") for g in GUIDES], lang) if GUIDES else ""
            content = (f'<h2>{ui("n_guides", lang)}</h2>' + gd if gd else "") + f'<h2>{ui("overviews", lang)}</h2>' + ov + f'<h2>{ui("themes", lang)}</h2>' + card_list(cards, lang)
        else:
            content = ""
            for r in REGION_ORDER:
                if r not in regions: continue
                ps = [p for p in places if p.get("region") == r]
                content += f'<h2><a href="{u_region(r, lang)}">{e(L(regions[r]["name"], lang))}</a></h2><p>{e(L(regions[r].get("tagline", {}), lang))}</p>' + card_list([(L(p["name"], lang), L(p.get("tagline", {}), lang), u_place(p, lang), "") for p in ps], lang)
        body = f'''<section aria-labelledby="h-top"><div class="wrap">{cr}<h1 id="h-top">{e(name)}</h1><p class="lead">{e(L(d.get("tagline", {}), lang))}</p>{intro}</div></section>
<section class="alt"><div class="wrap">{content}</div></section>'''
        desc = (L(d.get("tagline", {}), lang) + " " + " ".join(paras(L(d.get("intro", {}), lang)))[:170]).strip()[:300]
        ld_graph = [
            {"@type": "CollectionPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": "@@LASTMOD@@", "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
            dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"})]
        write(urls[lang], shell(lang, "hub:" + kind, urls, f"{name} | Niederau.nl", desc, body, ld_graph, og_type="website"))
    registry.append(("hub:" + kind, urls, None))


# ---------- collecties (seizoen, regendag, met kinderen) ----------
RAIN = "l2 l6 s68 s198 s232 s200 s170 w32 s292 s78 w39 s37 s69 w33 s257 s137 s190 s167 s172 s144 s122 s208".split()
KIDS = "l3 l4 l5 l9 l10 l12 s141 s182 s192 s202 s214 s219 s222 s56 s65 s72 s96 s11 s12 s119 s5 s101 s25 s18 s2 s20 w1 w30 w4 w5 w9 w11 w6 s217 s295 s175 s216 s169 s213 s144 s37 s6".split()
COLL = {
 "winter": {"slug": ("winter", "winter", "winter"), "season": "winter",
  "title": ("Winter in Niederau en omgeving", "Winter in Niederau and around", "Winter in Niederau und Umgebung"),
  "tagline": ("Skiën, rodelen, winterwandelen en meer", "Skiing, tobogganing, winter walks and more", "Skifahren, Rodeln, Winterwandern und mehr"),
  "intro": ("In de winter draait Niederau om sneeuw: skiën in het skigebied rond het Markbachjoch en bij Ski Juwel, rodelen, langlaufen en wandelen over geprepareerde winterpaden. Het skiseizoen loopt grofweg van december tot half april; de precieze data wisselen per jaar.\n\nOp deze pagina staan alle winteractiviteiten uit onze gids bij elkaar, in het dal én binnen een uur rijden. Voor wie even niet de berg op wil: wellness, musea en glasstad Rattenberg zijn ook in de winter een goede keuze.",
            "In winter, Niederau is all about snow: skiing in the ski area around the Markbachjoch and at Ski Juwel, tobogganing, cross-country skiing and walking on groomed winter paths. The ski season runs roughly from December to mid-April; exact dates vary from year to year.\n\nThis page gathers all winter activities from our guide, in the valley and within an hour’s drive. If you would rather stay off the mountain for a day: wellness, museums and the glass town of Rattenberg are good winter choices too.",
            "Im Winter dreht sich in Niederau alles um Schnee: Skifahren im Skigebiet rund ums Markbachjoch und im Ski Juwel, Rodeln, Langlaufen und Wandern auf geräumten Winterwegen. Die Skisaison dauert grob von Dezember bis Mitte April; die genauen Termine wechseln von Jahr zu Jahr.\n\nHier finden Sie alle Winteraktivitäten unseres Reiseführers, im Tal und im Umkreis von einer Stunde Fahrt. Wer einmal nicht auf den Berg möchte: Wellness, Museen und die Glasstadt Rattenberg sind auch im Winter eine gute Wahl."),
  "tips": (["Boek skiles en materiaalhuur vooraf in het hoogseizoen.", "Controleer sneeuw- en pistesituatie en het lawinerapport voor je vertrekt.", "Neem warme kleding en zonnebrandcrème mee: de zon is op hoogte sterk."], ["Book ski lessons and equipment rental ahead in high season.", "Check snow and slope conditions and the avalanche report before you set off.", "Bring warm clothing and sunscreen: the sun is strong at altitude."], ["Skikurse und Skiverleih in der Hochsaison vorab buchen.", "Schnee- und Pistenlage sowie den Lawinenbericht vor der Abfahrt prüfen.", "Warme Kleidung und Sonnencreme mitnehmen: Die Sonne ist in der Höhe stark."])},
 "zomer": {"slug": ("zomer", "summer", "sommer"), "season": "summer",
  "title": ("Zomer in Niederau en omgeving", "Summer in Niederau and around", "Sommer in Niederau und Umgebung"),
  "tagline": ("Wandelen, fietsen, zwemmen en uitstapjes", "Hiking, cycling, swimming and day trips", "Wandern, Radfahren, Baden und Ausflüge"),
  "intro": ("In de zomer is de Wildschönau een groen wandelgebied met alpenweiden, hutten en honderden kilometers bewegwijzerde paden. Je fietst of mountainbiket door het dal, zwemt in het openluchtbad of in een van de meren in de buurt en neemt de bergbaan naar de hoogte.\n\nHier vind je alle zomeractiviteiten uit onze gids op één plek: van de eerste wandeling vanaf het Markbachjoch tot dagtochten naar Innsbruck, Kitzbühel en het Zillertal.",
            "In summer the Wildschönau is a green hiking region with alpine pastures, huts and hundreds of kilometres of waymarked trails. You can cycle or mountain bike through the valley, swim in the open-air pool or one of the nearby lakes, and take the mountain lift up for the views.\n\nHere you will find all summer activities from our guide in one place: from the first walk at the Markbachjoch to day trips to Innsbruck, Kitzbühel and the Zillertal.",
            "Im Sommer ist die Wildschönau ein grünes Wandergebiet mit Almwiesen, Hütten und Hunderten Kilometern beschilderter Wege. Man radelt oder mountainbikt durchs Tal, badet im Freibad oder in einem der Seen in der Nähe und fährt mit der Bergbahn in die Höhe.\n\nHier finden Sie alle Sommeraktivitäten unseres Reiseführers an einem Ort: von der ersten Wanderung am Markbachjoch bis zu Tagesausflügen nach Innsbruck, Kitzbühel und ins Zillertal."),
  "tips": (["Begin wandelingen vroeg: in de zomer kunnen er ’s middags onweersbuien komen.", "Neem water, zonnebrand en een regenjas mee, ook bij mooi weer.", "Controleer de zomerdienstregeling van de bergbaan vooraf."], ["Start hikes early: afternoon thunderstorms can occur in summer.", "Take water, sunscreen and a rain jacket, even in good weather.", "Check the summer timetable of the mountain lift beforehand."], ["Wanderungen früh beginnen: Im Sommer sind nachmittags Gewitter möglich.", "Wasser, Sonnencreme und eine Regenjacke mitnehmen, auch bei schönem Wetter.", "Den Sommerfahrplan der Bergbahn vorher prüfen."])},
 "regendag": {"slug": ("regendag", "rainy-day", "regenwetter"), "ids": RAIN,
  "title": ("Wat te doen bij regen", "What to do when it rains", "Was tun bei Regen"),
  "tagline": ("Musea, wellness, glas en meer onder dak", "Museums, wellness, glass and more under cover", "Museen, Wellness, Glas und mehr unter Dach"),
  "intro": ("Een regenachtige dag hoeft niet verloren te zijn. In en rond Niederau vind je wellness en zwembaden, musea en kastelen, een zilvermijn en glasateliers in Rattenberg. Ook op deze bestemmingen is vaak buiten wat te doen, dus neem een regenjas mee.\n\nControleer altijd of de aanbieder open is: musea en attracties hebben vaak eigen sluitingsdagen en seizoenen.",
            "A rainy day does not have to be wasted. In and around Niederau you will find wellness and pools, museums and castles, a silver mine and glass workshops in Rattenberg. Many of these places also have something to do outdoors, so bring a rain jacket.\n\nAlways check that the provider is open: museums and attractions often have their own closing days and seasons.",
            "Ein Regentag muss kein verlorener Tag sein. In und um Niederau gibt es Wellness und Bäder, Museen und Schlösser, ein Silberbergwerk und Glaswerkstätten in Rattenberg. An vielen dieser Orte gibt es auch draußen etwas zu sehen, nehmen Sie also eine Regenjacke mit.\n\nBitte immer prüfen, ob der Anbieter geöffnet hat: Museen und Attraktionen haben oft eigene Ruhetage und Saisonzeiten."),
  "tips": (["Bel vooraf voor openingstijden en kaartjes bij populaire attracties.", "Combineer binnen en buiten: veel bestemmingen hebben ook een tuin of terras.", "Zwembad en wellness zijn goede opties voor de hele familie."], ["Call ahead for opening times and tickets at popular attractions.", "Combine indoors and outdoors: many places also have a garden or terrace.", "Pool and wellness are good options for the whole family."], ["Bei beliebten Attraktionen vorab Öffnungszeiten und Tickets erfragen.", "Drinnen und draußen verbinden: Viele Ziele haben auch Garten oder Terrasse.", "Schwimmbad und Wellness sind gute Optionen für die ganze Familie."])},
 "kinderen": {"slug": ("met-kinderen", "with-kids", "mit-kindern"), "ids": KIDS,
  "title": ("Met kinderen in Niederau en omgeving", "With kids in Niederau and around", "Mit Kindern in Niederau und Umgebung"),
  "tagline": ("Speelparken, dieren, zwemmen en sneeuwpret", "Play parks, animals, swimming and snow fun", "Spielparks, Tiere, Baden und Schneespaß"),
  "intro": ("Niederau is een fijn dorp voor gezinnen: kleine skischolen, speelplekken, dieren en kindvriendelijke wandelingen liggen vlakbij. Binnen een uur rijden zijn er meren, speelparken en de Alpenzoo in Innsbruck.\n\nHier staan de activiteiten uit onze gids die bij kinderen passen, in zomer en winter. Leeftijden en lengtes verschillen per aanbieder; kijk bij elke pagina of vraag het ter plaatse.",
            "Niederau is a lovely village for families: small ski schools, play areas, animals and child-friendly walks are close by. Within an hour’s drive there are lakes, play parks and the Alpenzoo in Innsbruck.\n\nHere are the activities from our guide that suit children, in summer and winter. Ages and height limits vary by provider; check each page or ask on the spot.",
            "Niederau ist ein schönes Dorf für Familien: kleine Skischulen, Spielplätze, Tiere und kinderfreundliche Wanderungen sind ganz in der Nähe. Im Umkreis von einer Stunde gibt es Seen, Spielparks und den Alpenzoo in Innsbruck.\n\nHier stehen die Aktivitäten unseres Reiseführers, die zu Kindern passen, im Sommer und im Winter. Alters- und Größenbeschränkungen sind je nach Anbieter verschieden; bitte auf der jeweiligen Seite nachsehen oder vor Ort erfragen."),
  "tips": (["Neem altijd reservekleding en een regenjas voor de kinderen mee.", "Plan na een lange wandeling een pauze bij een hut met speeltuin.", "Vraag vooraf naar minimumleeftijd en lengte, vooral bij avontuurlijke activiteiten."], ["Always bring spare clothes and a rain jacket for the children.", "After a long walk, plan a break at a hut with a playground.", "Ask beforehand about minimum age and height, especially for adventurous activities."], ["Immer Wechselkleidung und eine Regenjacke für die Kinder mitnehmen.", "Nach einer langen Wanderung eine Pause an einer Hütte mit Spielplatz einplanen.", "Vorab nach Mindestalter und Größe fragen, besonders bei abenteuerlichen Aktivitäten."])},
}
def coll_acts(c):
    d = COLL[c]
    if "season" in d: return [a for a in acts if a["season"] == d["season"]]
    ids = set(d["ids"]); return [a for a in acts if a["id"] in ids]
def u_coll(c, lang): return f"/{PREFIX[lang]}{DIRS['act'][lang]}/{COLL[c]['slug'][LANGS.index(lang)]}/"

def build_coll(c):
    d = COLL[c]; urls = {l: u_coll(c, l) for l in LANGS}; items = coll_acts(c)
    for lang in LANGS:
        i = LANGS.index(lang); name = d["title"][i]
        cr, cr_ld = crumbs(lang, [(ui("n_act", lang), u_hub("act", lang)), (name, urls[lang])])
        intro = "".join(f"<p>{e(x)}</p>" for x in paras(d["intro"][i]))
        tips = "".join(f"<li>{e(x)}</li>" for x in d["tips"][i])
        cards = card_list([(L(x["title"], lang), L(x.get("tagline", {}), lang), u_act(x, lang), season_badge(x, lang)) for x in sorted(items, key=lambda x: (x["theme"], x["id"]))], lang)
        body = f'''<section aria-labelledby="h-top"><div class="wrap split" style="align-items:start">
<div>{cr}<p class="eyebrow">{ui("n_act", lang)}</p><h1 id="h-top">{e(name)}</h1><p class="lead">{e(d["tagline"][i])}</p>{intro}</div>
<div><h2>{ui("tips", lang)}</h2><ul class="check">{tips}</ul><p class="note">{ui("check", lang)}</p></div></div></section>
<section class="alt"><div class="wrap"><h2>{ui("all_act", lang)} ({len(items)})</h2>{cards}</div></section>'''
        desc = (d["tagline"][i] + ". " + paras(d["intro"][i])[0])[:300]
        ld = [{"@type": "CollectionPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": "@@LASTMOD@@", "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
              dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"}),
              {"@type": "ItemList", "name": name, "itemListElement": [{"@type": "ListItem", "position": n + 1, "url": BASE + u_act(x, lang), "name": L(x["title"], lang)} for n, x in enumerate(items)]}]
        write(urls[lang], shell(lang, "coll:" + c, urls, f"{name} | Niederau.nl", desc, body, ld, og_type="website"))
    registry.append(("coll:" + c, urls, None))


# ---------- evenementenkalender ----------
EVENTS = json.load(open(DATA / "events.json", encoding="utf-8")) if (DATA / "events.json").exists() else []
EV_TXT = {
 "title": ("Evenementen en agenda in Niederau en omgeving", "Events and calendar in Niederau and around", "Veranstaltungen und Kalender in Niederau und Umgebung"),
 "tagline": ("Feesten, concerten en seizoensstarts door het jaar", "Festivals, concerts and season openings through the year", "Feste, Konzerte und Saisonstarts im Jahresverlauf"),
 "intro": ("Door het jaar heen valt er in de Wildschönau en omgeving van alles te beleven: van de Krautingerwoche en de adventstijd tot het Talfest en de Almabtrieb. Hieronder staan terugkerende evenementen, op volgorde vanaf de komende maanden. Datums kunnen per jaar verschillen; waar een datum is bevestigd, staat die erbij.\n\nControleer de actuele data altijd bij het toeristenbureau of de organisator voordat je plannen maakt.",
           "Through the year there is plenty to experience in the Wildschönau and around: from the Krautinger Week and Advent to the valley festival and the Almabtrieb. Below you will find recurring events, in order starting from the coming months. Dates can differ from year to year; where a date has been confirmed, it is given.\n\nAlways check current dates with the tourist office or the organiser before making plans.",
           "Im Lauf des Jahres gibt es in der Wildschönau und Umgebung viel zu erleben: von der Krautingerwoche und der Adventszeit bis zum Talfest und zum Almabtrieb. Unten stehen wiederkehrende Veranstaltungen, beginnend mit den kommenden Monaten. Termine können sich von Jahr zu Jahr unterscheiden; wo ein Datum bestätigt ist, wird es genannt.\n\nBitte aktuelle Termine immer beim Tourismusverband oder Veranstalter prüfen, bevor Sie planen."),
 "when": ("Wanneer", "When", "Wann"),
}
def u_events(lang): return f"/{PREFIX[lang]}{DIRS['events'][lang]}/"
def build_events():
    if not EVENTS: return
    urls = {l: u_events(l) for l in LANGS}
    cur = int(TODAY[5:7])
    evs = sorted(EVENTS, key=lambda x: ((x["month"] - cur) % 12, x["id"]))
    for lang in LANGS:
        i = LANGS.index(lang); name = EV_TXT["title"][i]
        cr, cr_ld = crumbs(lang, [(name, urls[lang])])
        intro = "".join(f"<p>{e(x)}</p>" for x in paras(EV_TXT["intro"][i]))
        cards = []
        for x in evs:
            pl = place_by.get(x.get("place") or "")
            plh = f'<p>{ui("near", lang)}: <a href="{u_place(pl, lang)}">{e(L(pl["name"], lang))}</a></p>' if pl else ""
            lk = f'<p><a href="{e(x["url"])}" rel="noopener" target="_blank">{ui("website", lang)}</a></p>' if x.get("url") else ""
            ds = "".join(f"<p>{e(t)}</p>" for t in paras(L(x["desc"], lang)))
            det = EV_BY_ID.get(x["id"])
            more = f'<p><a href="{u_event(det, lang)}">{ui("read_more", lang)} →</a></p>' if det else ""
            cards.append(f'<article class="card"><h3>{e(L(x["name"], lang))}</h3><p><span class="chip">{e(L(x["when"], lang))}</span></p>{ds}{plh}{more}{lk}</article>')
        body = f'''<section aria-labelledby="h-top"><div class="wrap">{cr}<h1 id="h-top">{e(name)}</h1><p class="lead">{e(EV_TXT["tagline"][i])}</p>{intro}</div></section>
<section class="alt"><div class="wrap"><h2>{ui("events_h", lang)}</h2><div class="grid grid-two">{"".join(cards)}</div><p class="note">{ui("check", lang)}</p></div></section>'''
        desc = (EV_TXT["tagline"][i] + ". " + paras(EV_TXT["intro"][i])[0])[:300]
        ld = [{"@type": "CollectionPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": "@@LASTMOD@@", "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
              dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"}),
              {"@type": "ItemList", "name": name, "itemListElement": [{"@type": "ListItem", "position": n + 1, "name": L(x["name"], lang)} for n, x in enumerate(evs)]}]
        write(urls[lang], shell(lang, "events", urls, f"{name} | Niederau.nl", desc, body, ld, og_type="website"))
    registry.append(("events", urls, None))

# ---------- gidspagina's ----------
GUIDES = jload("guides/*.json")
GH = {"title": ("Gidsen en praktische tips", "Guides and practical tips", "Ratgeber und praktische Tipps"),
      "tagline": ("Reistijd, reizen, eten, veiligheid en meer", "Best time to visit, travel, food, safety and more", "Reisezeit, Anreise, Essen, Sicherheit und mehr"),
      "intro": ("Hier vind je verdiepende gidsen bij je verblijf in Niederau en de Wildschönau: wanneer je het best komt, hoe je er komt, wat je eet en hoe je veilig de bergen in gaat. Ze vullen de pagina’s over activiteiten en dorpen aan.",
                "Here you will find in-depth guides for your stay in Niederau and the Wildschönau: when to come, how to get there, what to eat and how to stay safe in the mountains. They complement the pages about activities and villages.",
                "Hier finden Sie vertiefende Ratgeber für Ihren Aufenthalt in Niederau und der Wildschönau: wann man am besten kommt, wie man anreist, was man isst und wie man sicher in die Berge geht. Sie ergänzen die Seiten zu Aktivitäten und Orten.")}
def u_guide(g, lang): return f"/{PREFIX[lang]}{DIRS['guide'][lang]}/{g['slug'][lang]}/"
def u_guides(lang): return f"/{PREFIX[lang]}{DIRS['guide'][lang]}/"
def build_guides():
    if not GUIDES: return
    for g in GUIDES:
        urls = {l: u_guide(g, l) for l in LANGS}
        for lang in LANGS:
            name = L(g["title"], lang)
            cr, cr_ld = crumbs(lang, [(GH["title"][LANGS.index(lang)], u_guides(lang)), (name, urls[lang])])
            intro = "".join(f"<p>{e(x)}</p>" for x in paras(L(g.get("intro", {}), lang)))
            secs = "".join(f'<h2>{e(L(x["h"], lang))}</h2><p>{e(L(x["p"], lang))}</p>' for x in g.get("sections", []))
            tips = L(g.get("tips", {}), lang, [])
            tips_h = f'<h2>{ui("tips", lang)}</h2><ul class="check">' + "".join(f"<li>{e(t)}</li>" for t in tips) + "</ul>" if tips else ""
            faq_s, faq_ld = faq_html(g.get("faq"), lang)
            body = f'''<section aria-labelledby="h-top"><div class="wrap split" style="align-items:start">
<div>{cr}<p class="eyebrow">{GH["title"][LANGS.index(lang)]}</p><h1 id="h-top">{e(name)}</h1><p class="lead">{e(L(g.get("tagline", {}), lang))}</p>{intro}</div>
<div>{tips_h}<p class="note">{ui("check", lang)}</p></div></div></section>
<section class="alt"><div class="wrap">{secs}</div></section>{faq_s}'''
            desc = (L(g.get("tagline", {}), lang) + " " + " ".join(paras(L(g.get("intro", {}), lang)))[:170]).strip()[:300]
            ld = [{"@type": "Article", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "headline": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": "@@LASTMOD@@", "image": [OG], "mainEntityOfPage": BASE + urls[lang], "author": {"@type": "Organization", "name": "Niederau.nl"}, "publisher": {"@id": f"{BASE}/#website"}},
                  dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"})] + ([dict(faq_ld, **{"@id": BASE + urls[lang] + "#faq"})] if faq_ld else [])
            write(urls[lang], shell(lang, "guide:" + g["id"], urls, f"{name} | Niederau.nl", desc, body, ld))
        registry.append(("guide:" + g["id"], urls, None))
    urls = {l: u_guides(l) for l in LANGS}
    for lang in LANGS:
        i = LANGS.index(lang); name = GH["title"][i]
        cr, cr_ld = crumbs(lang, [(name, urls[lang])])
        cards = card_list([(L(g["title"], lang), L(g.get("tagline", {}), lang), u_guide(g, lang), "") for g in GUIDES], lang)
        body = f'''<section aria-labelledby="h-top"><div class="wrap">{cr}<h1 id="h-top">{e(name)}</h1><p class="lead">{e(GH["tagline"][i])}</p><p>{e(GH["intro"][i])}</p></div></section>
<section class="alt"><div class="wrap"><h2>{e(name)}</h2>{cards}</div></section>'''
        desc = (GH["tagline"][i] + ". " + GH["intro"][i])[:300]
        ld = [{"@type": "CollectionPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": "@@LASTMOD@@"},
              dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"})]
        write(urls[lang], shell(lang, "guides", urls, f"{name} | Niederau.nl", desc, body, ld, og_type="website"))
    registry.append(("guides", urls, None))

GUIDE_BY_THEME = {"wandelen": ["wandelroutes", "veilig-in-de-bergen", "wanneer-gaan"], "zwemmen": ["zwemmen-meren", "wanneer-gaan", "reizen-naar-niederau"],
 "skieen": ["ski-juwel", "skien-met-kinderen", "reizen-naar-niederau"], "winterpret": ["rodelen", "langlaufen-winterwandelen", "winterweek"],
 "fietsen": ["fietsroutes", "veilig-in-de-bergen", "zomerweek"], "dieren": ["met-je-hond", "paardrijden", "zomerweek"],
 "cultuur": ["dagtochten", "wildschoenau-card", "wanneer-gaan"], "attracties": ["dagtochten", "wildschoenau-card", "zomerweek"],
 "dagtochten": ["dagtochten", "reizen-naar-niederau", "wildschoenau-card"], "wellness": ["accommodatie-kiezen", "winterweek", "wanneer-gaan"],
 "workshops": ["eten-drinken", "wanneer-gaan"], "avontuur": ["veilig-in-de-bergen", "wildschoenau-card", "zomerweek"], "golf": ["dagtochten", "reizen-naar-niederau", "wanneer-gaan"]}
PLACE_GUIDES = ["dagtochten", "reizen-naar-niederau", "wanneer-gaan"]

def guides_block(lang, ids):
    gs = [g for i in ids for g in GUIDES if g["id"] == i]
    if not gs: return ""
    return f'<section class="alt"><div class="wrap"><h2>{ui("guides_h", lang)}</h2>' + card_list([(L(g["title"], lang), L(g.get("tagline", {}), lang), u_guide(g, lang), "") for g in gs[:3]], lang) + f'<p><a href="{u_guides(lang)}">{ui("n_guides", lang)} →</a></p></div></section>'

# ---------- evenement-detailpagina's ----------
EV_DETAIL = json.load(open(DATA / "events_detail.json", encoding="utf-8")) if (DATA / "events_detail.json").exists() else []
EV_BY_ID = {d["id"]: d for d in EV_DETAIL}
def u_event(d, lang): return f"/{PREFIX[lang]}{DIRS['events'][lang]}/{d['slug'][lang]}/"

def build_event_details():
    for d in EV_DETAIL:
        urls = {l: u_event(d, l) for l in LANGS}
        ev = next((x for x in EVENTS if x["id"] == d["id"]), None)
        for lang in LANGS:
            i = LANGS.index(lang); name = L(d["title"], lang)
            cr, cr_ld = crumbs(lang, [(EV_TXT["title"][i], u_events(lang)), (name, urls[lang])])
            intro = "".join(f"<p>{e(x)}</p>" for x in paras(L(d.get("intro", {}), lang)))
            secs = "".join(f'<h2>{e(L(x["h"], lang))}</h2><p>{e(L(x["p"], lang))}</p>' for x in d.get("sections", []))
            tips = L(d.get("tips", {}), lang, [])
            tips_h = f'<h2>{ui("tips", lang)}</h2><ul class="check">' + "".join(f"<li>{e(t)}</li>" for t in tips) + "</ul>" if tips else ""
            pl = place_by.get(d.get("place") or "")
            plh = f'<p>{ui("near", lang)}: <a href="{u_place(pl, lang)}">{e(L(pl["name"], lang))}</a></p>' if pl else ""
            when = f'<p><span class="chip">{e(L(d.get("date_label", {}), lang))}</span></p>' if d.get("date_label") else ""
            faq_s, faq_ld = faq_html(d.get("faq"), lang)
            body = f'''<section aria-labelledby="h-top"><div class="wrap split" style="align-items:start">
<div>{cr}<p class="eyebrow">{e(EV_TXT["title"][i])}</p><h1 id="h-top">{e(name)}</h1><p class="lead">{e(L(d.get("tagline", {}), lang))}</p>{when}{intro}{plh}</div>
<div>{tips_h}<p class="note">{ui("check", lang)}</p></div></div></section>
<section class="alt"><div class="wrap">{secs}</div></section>{faq_s}{guides_block(lang, ["wanneer-gaan", "reizen-naar-niederau", "wildschoenau-card"])}'''
            desc = (L(d.get("tagline", {}), lang) + " " + " ".join(paras(L(d.get("intro", {}), lang)))[:170]).strip()
            ld = [{"@type": "WebPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": trim_desc(desc), "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": "@@LASTMOD@@", "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
                  dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"})] + ([dict(faq_ld, **{"@id": BASE + urls[lang] + "#faq"})] if faq_ld else [])
            write(urls[lang], shell(lang, "event:" + d["id"], urls, f"{name} | Niederau.nl", desc, body, ld))
        registry.append(("event:" + d["id"], urls, None))

# ---------- over deze site (E-E-A-T) ----------
ABOUT = {
 "slug": ("over", "about", "ueber-uns"),
 "title": ("Over Niederau.nl", "About Niederau.nl", "Über Niederau.nl"),
 "tagline": ("Een persoonlijke, onafhankelijke gids over Niederau en de Wildschönau", "A personal, independent guide to Niederau and the Wildschönau", "Ein persönlicher, unabhängiger Reiseführer zu Niederau und der Wildschönau"),
 "intro": ("Niederau.nl is een persoonlijke gids over Niederau in de Wildschönau (Tirol). Ik kom er al ongeveer vijftig jaar en heb het dal in al die tijd zien veranderen. Ik wilde alles wat ik zelf graag had willen weten op één plek verzamelen, in het Nederlands, Engels en Duits, zodat je zonder zoeken je verblijf en je uitstapjes kunt plannen.",
           "Niederau.nl is a personal guide to Niederau in the Wildschönau (Tyrol). I have been coming here for about fifty years and have watched the valley change over that time. I wanted to gather everything I would have liked to know myself in one place, in Dutch, English and German, so that you can plan your stay and your outings without searching around.",
           "Niederau.nl ist ein persönlicher Reiseführer zu Niederau in der Wildschönau (Tirol). Ich komme seit etwa fünfzig Jahren hierher und habe das Tal in dieser Zeit sich verändern sehen. Ich wollte alles, was ich selbst gern gewusst hätte, an einem Ort sammeln, auf Niederländisch, Englisch und Deutsch, damit Sie Ihren Aufenthalt und Ihre Ausflüge ohne langes Suchen planen können."),
 "sections": [
  (("Onafhankelijk, met één partner", "Independent, with one partner", "Unabhängig, mit einem Partner"),
   ("Niederau.nl is een onafhankelijke site en niet verbonden aan een toeristenbureau of gemeente. Hotel Wastlhof in Niederau is partner van deze site en stelde foto’s beschikbaar. Dat is een persoonlijke aanbeveling: er is geen vergoeding betaald of ontvangen en er zijn geen affiliatelinks.",
    "Niederau.nl is an independent site and is not affiliated with a tourist office or municipality. Hotel Wastlhof in Niederau is a partner of this site and provided photos. This is a personal recommendation: no payment was made or received, and there are no affiliate links.",
    "Niederau.nl ist eine unabhängige Seite und nicht mit einem Tourismusverband oder einer Gemeinde verbunden. Das Hotel Wastlhof in Niederau ist Partner dieser Seite und hat Fotos zur Verfügung gestellt. Das ist eine persönliche Empfehlung: Es wurde keine Vergütung gezahlt oder erhalten, und es gibt keine Affiliate-Links.")),
  (("Hoe de teksten tot stand komen", "How the texts are made", "Wie die Texte entstehen"),
   ("De teksten zijn in eigen woorden geschreven, met hulp van AI-hulpmiddelen, en samengesteld uit toeristische bronnen zoals Wildschönau Tourismus, Ski Juwel en de toeristenorganisaties van de omliggende regio’s. Waar iets niet te bevestigen was, is het weggelaten of staat dat erbij. Tijden, prijzen en openingsdata veranderen; controleer ze daarom altijd bij de aanbieder. Op elke pagina staat wanneer deze voor het laatst is bijgewerkt.",
    "The texts are written in my own words, with the help of AI tools, and compiled from tourist sources such as Wildschönau Tourismus, Ski Juwel and the tourist organisations of the surrounding regions. Where something could not be confirmed, it has been left out or is marked as such. Times, prices and opening dates change, so always check them with the provider. Every page shows when it was last updated.",
    "Die Texte sind in eigenen Worten geschrieben, mit Unterstützung von KI-Werkzeugen, und aus touristischen Quellen wie Wildschönau Tourismus, Ski Juwel und den Tourismusorganisationen der umliegenden Regionen zusammengestellt. Was sich nicht bestätigen ließ, wurde weggelassen oder ist entsprechend gekennzeichnet. Zeiten, Preise und Öffnungsdaten ändern sich, bitte prüfen Sie sie deshalb immer beim Anbieter. Jede Seite zeigt, wann sie zuletzt aktualisiert wurde.")),
  (("Foto’s", "Photos", "Fotos"),
   ("Een deel van de foto’s heb ik zelf in Niederau gemaakt. De andere komen van Hotel Wastlhof, Wildschönau Tourismus, Ski Juwel Alpbachtal Wildschönau en de Wildschönauer Bergbahnen. Hartelijk dank aan Hotel Wastlhof voor het beschikbaar stellen van de foto’s. Foto’s staan alleen bij pagina’s waar ze echt bij horen.",
    "I took some of the photos myself in Niederau. The others come from Hotel Wastlhof, Wildschönau Tourismus, Ski Juwel Alpbachtal Wildschönau and the Wildschönauer Bergbahnen. Many thanks to Hotel Wastlhof for providing the photos. Photos are only shown on pages they genuinely belong to.",
    "Einen Teil der Fotos habe ich selbst in Niederau aufgenommen. Die anderen stammen vom Hotel Wastlhof, von Wildschönau Tourismus, vom Ski Juwel Alpbachtal Wildschönau und von den Wildschönauer Bergbahnen. Herzlichen Dank an das Hotel Wastlhof für die zur Verfügung gestellten Fotos. Fotos stehen nur dort, wo sie wirklich hingehören.")),
  (("Wat je hier vindt", "What you will find here", "Was Sie hier finden"),
   ("Het dorp en de seizoenen op de hoofdpagina, ruim tweehonderd activiteiten, gidsen voor alles van reistijd tot skiën met kinderen, en pagina’s over de dorpen en steden in de omgeving in Brixental, Inntal en Zillertal. Een agenda met terugkerende evenementen hoort er ook bij.",
    "The village and the seasons on the main page, over two hundred activities, guides for everything from the best time to visit to skiing with kids, and pages on the villages and towns around in the Brixental, Inn valley and Zillertal. There is also a calendar of recurring events.",
    "Das Dorf und die Jahreszeiten auf der Startseite, über zweihundert Aktivitäten, Ratgeber zu allem von der besten Reisezeit bis zum Skifahren mit Kindern sowie Seiten zu den Orten und Städten der Umgebung im Brixental, Inntal und Zillertal. Dazu gehört auch ein Kalender mit wiederkehrenden Veranstaltungen.")),
 ],
}
def u_about(lang): return f"/{PREFIX[lang]}{ABOUT['slug'][LANGS.index(lang)]}/"
def build_about():
    urls = {l: u_about(l) for l in LANGS}
    for lang in LANGS:
        i = LANGS.index(lang); name = ABOUT["title"][i]
        cr, cr_ld = crumbs(lang, [(name, urls[lang])])
        secs = "".join(f"<h2>{e(h[i])}</h2><p>{e(p[i])}</p>" for h, p in ABOUT["sections"])
        body = f'''<section aria-labelledby="h-top"><div class="wrap">{cr}<h1 id="h-top">{e(name)}</h1><p class="lead">{e(ABOUT["tagline"][i])}</p><p>{e(ABOUT["intro"][i])}</p></div></section>
<section class="alt"><div class="wrap">{secs}</div></section>'''
        desc = trim_desc(ABOUT["tagline"][i] + ". " + ABOUT["intro"][i])
        ld = [{"@type": "AboutPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": "@@LASTMOD@@", "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
              dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"})]
        write(urls[lang], shell(lang, "about", urls, f"{name} | Niederau.nl", desc, body, ld))
    registry.append(("about", urls, None))

def main():
    # oude uitvoer opruimen (alleen gegenereerde mappen)
    for kind in list(DIRS):
        for lang in LANGS:
            shutil.rmtree(ROOT / PREFIX[lang] / DIRS[kind][lang], ignore_errors=True)
    for a in acts: build_act(a)
    for p in places: build_place(p)
    for r in regions: build_region(r)
    for t in themes: build_theme(t)
    build_about()
    build_events()
    build_event_details()
    build_guides()
    for c in COLL: build_coll(c)
    if hubs.get("activities"): build_hub("act")
    if hubs.get("places"): build_hub("place")
    reg = [{"key": k, "urls": u, "img": i} for k, u, i in registry]
    json.dump(reg, open(DATA / "_registry.json", "w"), ensure_ascii=False)
    print(f"Pagina's gegenereerd: {len(acts)} activiteiten, {len(places)} plaatsen, {len(regions)} regio's, {len(themes)} thema's → {len(registry) * 3} bestanden")

if __name__ == "__main__":
    main()
