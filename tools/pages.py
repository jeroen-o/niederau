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

DIRS = {"act": {"nl": "activiteiten", "en": "activities", "de": "aktivitaeten"},
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
 "themes": ("Thema’s", "Themes", "Themen"),
 "regions": ("Regio’s", "Regions", "Regionen"),
 "n_act_count": ("activiteiten", "activities", "Aktivitäten"),
 "min": ("min.", "min.", "Min."),
 "ca": ("ca.", "approx.", "ca."),
 "act_in_theme": ("Activiteiten", "Activities", "Aktivitäten"),
}
def ui(k, lang): return UI[k][LANGS.index(lang)]

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

# ---------- data laden ----------
src = {o["id"]: o for o in json.load(open(DATA / "source_activities.json", encoding="utf-8"))}
EXCL = set(json.load(open(DATA / "exclude.json", encoding="utf-8"))["ids"]) if (DATA / "exclude.json").exists() else set()
PATCH = {}
for pt in jload("patches/*.json"):
    PATCH[pt.get("id") or pt.get("slug")] = pt
acts = []
for a in jload("acts/*.json"):
    patched = a["id"] in PATCH
    a = PATCH.get(a["id"], a)
    if a.get("drop") or (a["id"] in EXCL and not (patched and a.get("verified") is True)): continue
    s = src.get(a["id"])
    a["theme"] = a.get("theme") or (s["theme"] if s else "avontuur")
    a["season"] = a.get("season") or (s["season"] if s else "summer")
    a["slug_nl"] = a.get("slug_nl") or (s["slug_nl"] if s else a["id"])
    a["title"] = a.get("title") or {}
    if not L(a["title"], "nl") and s: a["title"] = {"nl": s["src"]["t"]}
    acts.append(a)
_ids = {a["id"] for a in acts}
for k, pt in PATCH.items():
    if pt.get("id") and pt["id"] not in _ids and not pt.get("drop") and pt.get("new"):
        pt.setdefault("theme", "golf"); pt.setdefault("season", "summer"); pt.setdefault("slug_nl", pt["id"])
        acts.append(pt)
places = [PATCH.get(p["slug"], p) for p in jload("places/*.json")]
places = [p for p in places if not p.get("drop")]
tdata = jload("themes/*.json")
themes = {t["theme"]: t for t in tdata if t.get("kind") == "theme"}
regions = {t["region"]: t for t in tdata if t.get("kind") == "region"}
hubs = {t["scope"]: t for t in tdata if t.get("kind") == "hub"}
REGION_ORDER = ["wildschoenau", "alpbachtal", "brixental", "kufsteinerland", "inntal", "zillertal"]
place_by = {p["slug"]: p for p in places}

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
def home(lang): return "/" if lang == "nl" else f"/{lang}/"

registry = []  # (key, {lang: url}, lastmod)

def shell(lang, key, urls, title, desc, body, ld_graph, og_type="article", img=None):
    """key identificeert de pagina in alle talen; urls = {lang: pad}."""
    here = BASE + urls[lang]
    hl = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{BASE}{urls[c]}">' for c in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{urls["en"]}">'
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
      <a href="{home(lang)}">{ui("n_home", lang)}</a>
      <a href="{u_hub("act", lang)}">{ui("n_act", lang)}</a>
      <a href="{u_hub("place", lang)}">{ui("n_place", lang)}</a>
      <a href="/{PREFIX[lang]}markbachjoch/">{ui("n_mb", lang)}</a>
      {tog}
      <div class="lang" aria-label="{ui("lang_label", lang)}">{lang_nav}</div>
    </nav>
  </div>
</header>
<main id="main">
<section class="page-hero" aria-hidden="true"></section>
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <h3>Niederau.nl</h3>
      <p>{ui("f_about", lang)}</p>
      <div class="lang" aria-label="{ui("lang_label", lang)}">{lang_nav}</div>
    </div>
    <div>
      <h3>Niederau</h3>
      <ul>
        <li><a href="{home(lang)}">{ui("f_back", lang)}</a></li>
        <li><a href="{u_hub("act", lang)}">{ui("n_act", lang)}</a></li>
        <li><a href="{u_hub("place", lang)}">{ui("n_place", lang)}</a></li>
        <li><a href="/{PREFIX[lang]}markbachjoch/">{ui("n_mb", lang)}</a></li>
      </ul>
    </div>
    <p class="credits">{ui("credits", lang)}</p>
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
        img, alt = THEME_IMG.get(a["theme"], (None, ("", "", "")))
        side = f'<img class="side-img" src="/assets/img/{img}.webp" width="1000" height="667" loading="lazy" alt="{e(alt[LANGS.index(lang)])}">' if img else ""
        body = f'''<section aria-labelledby="h-top"><div class="wrap split" style="align-items:start">
<div>{cr}<p class="eyebrow">{e(th_short)} · {season_badge(a, lang)}</p><h1 id="h-top">{e(title_n)}</h1><p class="lead">{e(L(a.get("tagline", {}), lang))}</p>{intro}{pl}{link}</div>
<div>{facts}{side}</div></div></section>
<section class="alt"><div class="wrap split" style="align-items:start"><div>{tips_h}</div><div>{pr_h}<p class="note">{ui("check", lang)}</p></div></div></section>
{faq_s}{rel_h}'''
        desc = (L(a.get("tagline", {}), lang) + " " + " ".join(paras(L(a.get("intro", {}), lang)))[:170]).strip()[:300]
        ld_graph = [
            {"@type": "WebPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": title_n, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": TODAY, "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
            dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"}),
            {"@type": ["TouristAttraction", "Place"], "name": title_n, "description": L(a.get("tagline", {}), lang), "url": BASE + urls[lang],
             **({"sameAs": a["url"]} if a.get("url") else {}),
             "containedInPlace": {"@type": "Place", "name": (L(p["name"], lang) if p else "Wildschönau") + ", Tirol, Austria"}},
        ] + ([dict(faq_ld, **{"@id": BASE + urls[lang] + "#faq"})] if faq_ld else [])
        write(urls[lang], shell(lang, a["id"], urls, f"{title_n} | Niederau.nl", desc, body, ld_graph, img=img))
    registry.append((a["id"], urls))

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
        body = f'''<section aria-labelledby="h-top"><div class="wrap split" style="align-items:start">
<div>{cr}<p class="eyebrow">{e(reg_name)}</p><h1 id="h-top">{e(name)}</h1><p class="lead">{e(L(p.get("tagline", {}), lang))}</p>{intro}{link}</div>
<div>{facts}</div></div></section>
<section class="alt"><div class="wrap split" style="align-items:start"><div>{hl_h}</div><div>{gt_h}<p class="note">{ui("check", lang)}</p></div></div></section>
{act_h}{faq_s}'''
        desc = (L(p.get("tagline", {}), lang) + " " + " ".join(paras(L(p.get("intro", {}), lang)))[:170]).strip()[:300]
        ld_graph = [
            {"@type": "WebPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": TODAY, "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
            dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"}),
            {"@type": ["TouristDestination", "Place"], "name": name, "description": L(p.get("tagline", {}), lang), "url": BASE + urls[lang],
             **({"sameAs": p["url"]} if p.get("url") else {}),
             **({"geo": {"@type": "GeoCoordinates", "elevation": p["elevation_m"]}} if p.get("elevation_m") else {}),
             "containedInPlace": {"@type": "AdministrativeArea", "name": "Tirol, Austria"}},
        ] + ([dict(faq_ld, **{"@id": BASE + urls[lang] + "#faq"})] if faq_ld else [])
        write(urls[lang], shell(lang, p["slug"], urls, f"{name}: {L(p.get('tagline', {}), lang)} | Niederau.nl"[:90] if False else f"{name} – {ui('n_place', lang)} Niederau | Niederau.nl", desc, body, ld_graph))
    registry.append(("place:" + p["slug"], urls))

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
<div>{hl_h}{gt_h}</div></div></section>
{pl_h}{faq_s}'''
        desc = (L(d.get("tagline", {}), lang) + " " + " ".join(paras(L(d.get("intro", {}), lang)))[:170]).strip()[:300]
        ld_graph = [
            {"@type": "WebPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": TODAY, "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
            dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"}),
            {"@type": ["TouristDestination", "Place"], "name": name, "description": L(d.get("tagline", {}), lang), "url": BASE + urls[lang]},
        ] + ([dict(faq_ld, **{"@id": BASE + urls[lang] + "#faq"})] if faq_ld else [])
        write(urls[lang], shell(lang, "region:" + r, urls, f"{name} – {ui('n_place', lang)} Niederau | Niederau.nl", desc, body, ld_graph))
    registry.append(("region:" + r, urls))

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
{lists}{faq_s}'''
        desc = (L(d.get("tagline", {}), lang) + " " + " ".join(paras(L(d.get("intro", {}), lang)))[:170]).strip()[:300]
        ld_graph = [
            {"@type": "CollectionPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": TODAY, "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
            dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"}),
            {"@type": "ItemList", "name": name, "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + u_act(x, lang), "name": L(x["title"], lang)} for i, x in enumerate(ta)]},
        ] + ([dict(faq_ld, **{"@id": BASE + urls[lang] + "#faq"})] if faq_ld else [])
        write(urls[lang], shell(lang, "theme:" + t, urls, f"{name} | Niederau.nl", desc, body, ld_graph, img=img))
    registry.append(("theme:" + t, urls))

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
            content = f'<h2>{ui("themes", lang)}</h2>' + card_list(cards, lang)
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
            {"@type": "CollectionPage", "@id": BASE + urls[lang] + "#webpage", "url": BASE + urls[lang], "name": name, "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"}, "dateModified": TODAY, "breadcrumb": {"@id": BASE + urls[lang] + "#bc"}},
            dict(cr_ld, **{"@id": BASE + urls[lang] + "#bc"})]
        write(urls[lang], shell(lang, "hub:" + kind, urls, f"{name} | Niederau.nl", desc, body, ld_graph, og_type="website"))
    registry.append(("hub:" + kind, urls))

def main():
    # oude uitvoer opruimen (alleen gegenereerde mappen)
    for kind in DIRS:
        for lang in LANGS:
            shutil.rmtree(ROOT / PREFIX[lang] / DIRS[kind][lang], ignore_errors=True)
    for a in acts: build_act(a)
    for p in places: build_place(p)
    for r in regions: build_region(r)
    for t in themes: build_theme(t)
    if hubs.get("activities"): build_hub("act")
    if hubs.get("places"): build_hub("place")
    reg = [{"key": k, "urls": u} for k, u in registry]
    json.dump(reg, open(DATA / "_registry.json", "w"), ensure_ascii=False)
    print(f"Pagina's gegenereerd: {len(acts)} activiteiten, {len(places)} plaatsen, {len(regions)} regio's, {len(themes)} thema's → {len(registry) * 3} bestanden")

if __name__ == "__main__":
    main()
