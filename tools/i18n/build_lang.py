#!/usr/bin/env python3
"""Bouwt /fr/ en /pl/ uit de gebouwde EN-pagina's met de vertalingen in tools/data/i18n/<taal>.json.

Een pagina wordt alleen gepubliceerd als ALLE tekstblokken vertaald zijn. Daarna worden intern /en/-links naar
de nieuwe taal omgezet (waar de doelpagina bestaat; anders blijven ze naar EN wijzen), en krijgen alle pagina's
(NL/EN/DE/FR/PL) een volledige hreflang-set, taalkiezer en sitemap-alternates. Draait na imgopt, voor finalize."""
import html as htmllib, json, pathlib, re, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from units import extract, apply_unit, dump

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "tools" / "data" / "i18n"
NEW = ("fr", "pl", "es", "it", "sv", "no", "fi", "da")
# Alleen deze talen worden geïndexeerd (hreflang, sitemap). De machinevertaalde talen (NEW) blijven bereikbaar via de taalkiezer,
# maar staan op noindex tot ze redactioneel zijn nagekeken en Search Console (Domain-property) laat zien welke taal verkeer oplevert.
# Terugdraaien: zet INDEX_ALL = True.
INDEX_ALL = False
INDEXED = ("nl", "en", "de")
MT_NOTE = {
    "fr": "Cette page est une traduction automatique du texte original (néerlandais, anglais ou allemand) et n’a pas été relue par un locuteur natif. En cas de doute, la version originale fait foi.",
    "pl": "Ta strona jest tłumaczeniem maszynowym oryginału (niderlandzkiego, angielskiego lub niemieckiego) i nie została sprawdzona przez native speakera. W razie wątpliwości obowiązuje wersja oryginalna.",
    "es": "Esta página es una traducción automática del texto original (neerlandés, inglés o alemán) y no ha sido revisada por un hablante nativo. En caso de duda, prevalece la versión original.",
    "it": "Questa pagina è una traduzione automatica del testo originale (olandese, inglese o tedesco) e non è stata rivista da un madrelingua. In caso di dubbio fa fede la versione originale.",
    "sv": "Den här sidan är en maskinöversättning av originaltexten (nederländska, engelska eller tyska) och har inte granskats av en person med språket som modersmål. Vid tveksamhet gäller originalversionen.",
    "no": "Denne siden er en maskinoversettelse av originalteksten (nederlandsk, engelsk eller tysk) og er ikke gjennomgått av en morsmålsbruker. Ved tvil gjelder originalversjonen.",
    "fi": "Tämä sivu on alkuperäisen tekstin (hollanti, englanti tai saksa) konekäännös, jota äidinkielinen puhuja ei ole tarkistanut. Epäselvissä tapauksissa alkuperäinen versio on ensisijainen.",
    "da": "Denne side er en maskinoversættelse af den originale tekst (nederlandsk, engelsk eller tysk) og er ikke gennemgået af en modersmålstalende. Ved tvivl gælder den originale version.",
}
SITE = "https://niederau.nl"
LOCALE = {"fr": "fr_FR", "pl": "pl_PL", "es": "es_ES", "it": "it_IT", "sv": "sv_SE", "no": "nb_NO", "fi": "fi_FI", "da": "da_DK"}
LABEL = {"nl": "NL", "en": "EN", "de": "DE", "fr": "FR", "pl": "PL", "es": "ES", "it": "IT", "sv": "SV", "no": "NO", "fi": "FI", "da": "DA"}
ORDER = ("nl", "en", "de", "fr", "pl", "es", "it", "sv", "no", "fi", "da")
OGLOC = {"nl": "nl_NL", "en": "en_GB", "de": "de_DE", "fr": "fr_FR", "pl": "pl_PL", "es": "es_ES", "it": "it_IT", "sv": "sv_SE", "no": "nb_NO", "fi": "fi_FI", "da": "da_DK"}
# Zoekvriendelijke slugs per taal voor de pagina's die op zoekopdrachten als "location de ski niederau" mikken
SLUG = {
    "fr": {"ski-rental-niederau": "location-ski-niederau", "ski-area-niederau-map": "plan-des-pistes-niederau", "webcam": "webcam-niederau",
           "hotel-on-the-slopes-wildschonau": "hotel-aux-pieds-des-pistes-wildschonau", "ski-pass-prices-niederau": "prix-forfait-ski-niederau"},
    "pl": {"ski-rental-niederau": "wypozyczalnia-nart-niederau", "ski-area-niederau-map": "mapa-tras-niederau", "webcam": "kamery-niederau",
           "hotel-on-the-slopes-wildschonau": "hotel-przy-stoku-wildschonau", "ski-pass-prices-niederau": "cennik-karnetow-niederau"},
    "es": {"ski-rental-niederau": "alquiler-esqui-niederau", "ski-area-niederau-map": "mapa-pistas-niederau", "webcam": "webcam-niederau",
           "hotel-on-the-slopes-wildschonau": "hotel-a-pie-de-pista-wildschonau", "ski-pass-prices-niederau": "precio-forfait-niederau"},
    "it": {"ski-rental-niederau": "noleggio-sci-niederau", "ski-area-niederau-map": "mappa-piste-niederau", "webcam": "webcam-niederau",
           "hotel-on-the-slopes-wildschonau": "hotel-sulle-piste-wildschonau", "ski-pass-prices-niederau": "prezzo-skipass-niederau"},
    "sv": {"ski-rental-niederau": "skiduthyrning-niederau", "ski-area-niederau-map": "pistkarta-niederau", "webcam": "webbkamera-niederau",
           "hotel-on-the-slopes-wildschonau": "hotell-vid-pisten-wildschonau", "ski-pass-prices-niederau": "skidpass-pris-niederau"},
    "no": {"ski-rental-niederau": "skiutleie-niederau", "ski-area-niederau-map": "pistekart-niederau", "webcam": "webkamera-niederau",
           "hotel-on-the-slopes-wildschonau": "hotell-ved-bakken-wildschonau", "ski-pass-prices-niederau": "skipass-pris-niederau"},
    "fi": {"ski-rental-niederau": "hiihtovalineiden-vuokraus-niederau", "ski-area-niederau-map": "rinnekartta-niederau", "webcam": "verkkokamera-niederau",
           "hotel-on-the-slopes-wildschonau": "hotelli-rinteen-vieressa-wildschonau", "ski-pass-prices-niederau": "hissilipun-hinta-niederau"},
    "da": {"ski-rental-niederau": "skiudleje-niederau", "ski-area-niederau-map": "pistekort-niederau", "webcam": "webcam-niederau",
           "hotel-on-the-slopes-wildschonau": "hotel-ved-pisten-wildschonau", "ski-pass-prices-niederau": "skipas-pris-niederau"},
}
PLACENAME = {"fr": "Niederau, Wildschönau, Tyrol, Autriche", "pl": "Niederau, Wildschönau, Tyrol, Austria", "es": "Niederau, Wildschönau, Tirol, Austria",
             "it": "Niederau, Wildschönau, Tirolo, Austria", "sv": "Niederau, Wildschönau, Tyrolen, Österrike", "no": "Niederau, Wildschönau, Tirol, Østerrike",
             "fi": "Niederau, Wildschönau, Tirol, Itävalta", "da": "Niederau, Wildschönau, Tyrol, Østrig"}

def locpath(p, l):
    """/en/<segment>/... -> /<l>/<lokale slug>/..."""
    rest = p[len("/en/"):]
    seg, sep, tail = rest.partition("/")
    seg = SLUG.get(l, {}).get(seg, seg)
    return f"/{l}/{seg}{sep}{tail}"

def trim_meta(html):
    """Titel en description beperken tot wat zoekmachines tonen (vertalingen zijn vaak langer)."""
    def short(d, n=158):
        if len(d) <= n: return d
        cut = d[:n]
        m = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
        if m >= 80: return cut[:m + 1]
        return cut[:cut.rfind(" ")].rstrip(" ,;:–-") + "…"
    def d(m):
        v = htmllib.unescape(m.group(2))
        return m.group(1) + htmllib.escape(short(v), quote=True) + m.group(3)
    html = re.sub(r'(<meta name="description" content=")([^"]*)(")', d, html, 1)
    html = re.sub(r'(<meta property="og:description" content=")([^"]*)(")', d, html, 1)
    def t(m):
        v = m.group(2)
        if len(v) > 65 and v.endswith(" | Niederau.nl"): v = v[:-len(" | Niederau.nl")]
        return m.group(1) + v + m.group(3)
    return re.sub(r'(<title>)(.*?)(</title>)', t, html, 1, flags=re.S)

def path_of(f):
    rel = f.relative_to(ROOT).as_posix()
    return "/" + rel[:-len("index.html")]

def lang_of(path):
    m = re.match(r"/(en|de|fr|pl)/", path)
    return m.group(1) if m else "nl"

def render(f, lang, tr):
    """Geeft (html, ontbrekend) voor een EN-pagina in `lang`."""
    soup, items = extract(f.read_text(encoding="utf-8"))
    miss = []
    for h, t in items:
        if "hreflang=" in t: continue
        v = apply_unit(h, t, tr)
        if v: miss.append(v)
    return soup, miss

def main():
    for l in NEW:
        shutil.rmtree(ROOT / l, ignore_errors=True)  # volledig gegenereerd; oude slugs mogen niet blijven staan
    en_pages = {path_of(f): f for f in sorted((ROOT / "en").rglob("index.html"))}
    trs = {l: {k.replace("&amp;", "&"): v for k, v in (json.loads((D / f"{l}.json").read_text()) if (D / f"{l}.json").exists() else {}).items()} for l in NEW}
    # pass 1: welke pagina's zijn volledig vertaald?
    soups = {l: {} for l in NEW}
    for l in NEW:
        for p, f in en_pages.items():
            soup, miss = render(f, l, trs[l])
            if not miss: soups[l][p] = soup
    exist = {l: {locpath(p, l) for p in soups[l]} for l in NEW}
    # groepen: nl-pad -> {taal: pad}
    groups = {}; of_page = {}
    pat = re.compile(r'<link rel="alternate" hreflang="(\w\w)" href="https://niederau\.nl([^"]*)">')
    allfiles = [f for f in ROOT.rglob("index.html") if not f.relative_to(ROOT).parts[0] in ("node_modules", "tools", ".git", "fr", "pl")]
    for f in allfiles:
        g = dict(pat.findall(f.read_text(encoding="utf-8")))
        if "nl" not in g: continue
        groups.setdefault(g["nl"], {}).update({k: v for k, v in g.items()})
    for nlp, g in groups.items():
        en = g.get("en")
        for l in NEW:
            if en and en in soups[l]: g[l] = locpath(en, l)
        for lg, pp in g.items(): of_page[pp] = nlp

    def switcher(g, cur):
        a = []
        for lg in ORDER:
            if lg not in g: continue
            cur_attr = ' aria-current="true"' if lg == cur else ""
            a.append(f'<a href="{g[lg]}" hreflang="{lg}" lang="{lg}"{cur_attr}>{LABEL[lg]}</a>')
        return "".join(a)

    def hreflangs(g):
        out = [f'<link rel="alternate" hreflang="{lg}" href="{SITE}{g[lg]}">' for lg in ORDER if lg in g and (INDEX_ALL or lg in INDEXED)]
        out.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{g["nl"]}">')
        return "\n".join(out)

    def retarget(html, lang):
        """/en/-links -> /lang/ waar de doelpagina bestaat."""
        def r(m):
            full = m.group(0); rest = m.group(2)
            p = "/en/" + rest
            q = p.split("#")[0].split("?")[0]
            if q in soups[lang]: return m.group(1) + locpath(p, lang)
            return full
        return re.sub(r'((?:https://niederau\.nl)?)/en/([^"\'\s<>\\]*)', r, html)

    def fix_head(html, g, cur):
        html = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]*">\n?', "", html)
        if INDEX_ALL or cur in INDEXED:  # noindex-pagina's krijgen geen hreflang
            html = re.sub(r'(<link rel="canonical" href="[^"]*">)', lambda m: m.group(1) + "\n" + hreflangs(g), html, 1)
        html = re.sub(r'<meta property="og:locale:alternate" content="[^"]*">\n?', "", html)
        alt = "".join(f'<meta property="og:locale:alternate" content="{OGLOC[lg]}">\n' for lg in ORDER if lg in g and lg != cur and (INDEX_ALL or lg in INDEXED))
        html = re.sub(r'(<meta property="og:locale" content="[^"]*">\n?)', lambda m: m.group(1).rstrip("\n") + "\n" + alt.rstrip("\n") + "\n", html, 1)
        html = re.sub(r'<div class="lang" role="group" aria-label="([^"]*)">.*?</div>',
                      lambda m: f'<div class="lang" role="group" aria-label="{m.group(1)}">{switcher(g, cur)}</div>', html, flags=re.S)
        return html

    n_new = {}
    for l in NEW:
        n = 0
        for p, soup in soups[l].items():
            lp = locpath(p, l)
            html = dump(soup)
            if not html.lower().startswith("<!doctype"): html = "<!doctype html>\n" + html
            html = re.sub(r'<html lang="en"', f'<html lang="{l}"', html, 1)
            html = html.replace('content="en_GB"', f'content="{LOCALE[l]}"')
            html = re.sub(r'("inLanguage": ?)"en"', lambda m: m.group(1) + f'"{l}"', html)
            html = html.replace(f"{SITE}{p}", f"{SITE}{lp}")
            if p == "/en/":  # relatieve links op de startpagina: lokale pagina als die bestaat, anders de Engelse
                def rel(m):
                    ref = m.group(1)
                    if re.match(r"(/|#|[a-z]+:|\.)", ref) or not ref: return m.group(0)
                    path, sep, frag = ref.partition("#")
                    q = "/en/" + path
                    tgt = locpath(q, l) if q in soups[l] else q
                    return f'href="{tgt}{sep}{frag}"'
                html = re.sub(r'href="([^"]*)"', rel, html)
            html = trim_meta(html)
            if not INDEX_ALL:
                html = html.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex, follow">', 1)
                html = re.sub(r'(<main id="main">\s*)', lambda m: m.group(1) + f'<p class="mt-note" role="note">{MT_NOTE[l]}</p>\n    ', html, 1)
            if l in PLACENAME: html = html.replace('name="geo.placename" content="Niederau, Wildschönau, Tyrol, Austria"', f'name="geo.placename" content="{PLACENAME[l]}"')
            html = retarget(html, l)
            g = groups[of_page[p]]
            html = fix_head(html, g, l)
            out = ROOT / lp.strip("/") / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8"); n += 1
        n_new[l] = n
    # bestaande pagina's: hreflang + taalkiezer uitbreiden
    for f in allfiles:
        t = f.read_text(encoding="utf-8")
        p = path_of(f)
        if p not in of_page: continue
        g = groups[of_page[p]]
        if not any(l in g for l in NEW): continue
        f.write_text(fix_head(t, g, lang_of(p)), encoding="utf-8")
    # sitemap
    sm = ROOT / "sitemap.xml"; s = sm.read_text(encoding="utf-8")
    blocks = re.findall(r"  <url>.*?</url>\n", s, re.S)
    out = []
    for b in blocks:
        loc = re.search(r"<loc>https://niederau\.nl([^<]*)</loc>", b).group(1)
        g = groups.get(of_page.get(loc, ""), None)
        if g:
            alts = "\n".join(f'    <xhtml:link rel="alternate" hreflang="{lg}" href="{SITE}{g[lg]}"/>' for lg in ORDER if lg in g and (INDEX_ALL or lg in INDEXED))
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{g["nl"]}"/>'
            multi = "\n    <xhtml:link" in b
            new = alts if multi else alts.replace("\n    ", "").replace("    <xhtml", "<xhtml")
            b = re.sub(r'(\s*<xhtml:link rel="alternate"[^>]*/>)+', lambda m: ("\n" if multi else "") + new, b, 1)
        out.append(b)
        if g and loc == g.get("en") and INDEX_ALL:
            for l in NEW:
                if l in g:
                    out.append(b.replace(f"<loc>{SITE}{loc}</loc>", f"<loc>{SITE}{g[l]}</loc>"))
    s = s.replace("".join(blocks), "".join(out))
    sm.write_text(s, encoding="utf-8")
    tot = len(en_pages)
    print("i18n:", ", ".join(f"{l}: {n_new[l]}/{tot}" for l in NEW))

if __name__ == "__main__":
    main()
