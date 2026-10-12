#!/usr/bin/env python3
"""Bouwt /fr/ en /pl/ uit de gebouwde EN-pagina's met de vertalingen in tools/data/i18n/<taal>.json.

Een pagina wordt alleen gepubliceerd als ALLE tekstblokken vertaald zijn. Daarna worden intern /en/-links naar
de nieuwe taal omgezet (waar de doelpagina bestaat; anders blijven ze naar EN wijzen), en krijgen alle pagina's
(NL/EN/DE/FR/PL) een volledige hreflang-set, taalkiezer en sitemap-alternates. Draait na imgopt, voor finalize."""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from units import extract, apply_unit, dump

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = ROOT / "tools" / "data" / "i18n"
NEW = ("fr", "pl")
SITE = "https://niederau.nl"
LOCALE = {"fr": "fr_FR", "pl": "pl_PL"}
LABEL = {"nl": "NL", "en": "EN", "de": "DE", "fr": "FR", "pl": "PL"}
ORDER = ("nl", "en", "de", "fr", "pl")

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
    en_pages = {path_of(f): f for f in sorted((ROOT / "en").rglob("index.html"))}
    trs = {l: {k.replace("&amp;", "&"): v for k, v in (json.loads((D / f"{l}.json").read_text()) if (D / f"{l}.json").exists() else {}).items()} for l in NEW}
    # pass 1: welke pagina's zijn volledig vertaald?
    soups = {l: {} for l in NEW}
    for l in NEW:
        for p, f in en_pages.items():
            soup, miss = render(f, l, trs[l])
            if not miss: soups[l][p] = soup
    exist = {l: {p.replace("/en/", f"/{l}/", 1) for p in soups[l]} for l in NEW}
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
            if en and en in soups[l]: g[l] = en.replace("/en/", f"/{l}/", 1)
        for lg, pp in g.items(): of_page[pp] = nlp

    def switcher(g, cur):
        a = []
        for lg in ORDER:
            if lg not in g: continue
            cur_attr = ' aria-current="true"' if lg == cur else ""
            a.append(f'<a href="{g[lg]}" hreflang="{lg}" lang="{lg}"{cur_attr}>{LABEL[lg]}</a>')
        return "".join(a)

    def hreflangs(g):
        out = [f'<link rel="alternate" hreflang="{lg}" href="{SITE}{g[lg]}">' for lg in ORDER if lg in g]
        out.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{g["nl"]}">')
        return "\n".join(out)

    def retarget(html, lang):
        """/en/-links -> /lang/ waar de doelpagina bestaat."""
        def r(m):
            full = m.group(0); rest = m.group(2)
            p = "/en/" + rest
            q = p.split("#")[0].split("?")[0]
            if q in soups[lang]: return m.group(1) + f"/{lang}/" + rest
            return full
        return re.sub(r'((?:https://niederau\.nl)?)/en/([^"\'\s<>\\]*)', r, html)

    def fix_head(html, g, cur):
        html = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]*">\n?', "", html)
        html = re.sub(r'(<link rel="canonical" href="[^"]*">)', lambda m: m.group(1) + "\n" + hreflangs(g), html, 1)
        html = re.sub(r'<div class="lang" role="group" aria-label="([^"]*)">.*?</div>',
                      lambda m: f'<div class="lang" role="group" aria-label="{m.group(1)}">{switcher(g, cur)}</div>', html, flags=re.S)
        return html

    n_new = {}
    for l in NEW:
        n = 0
        for p, soup in soups[l].items():
            lp = p.replace("/en/", f"/{l}/", 1)
            html = dump(soup)
            if not html.lower().startswith("<!doctype"): html = "<!doctype html>\n" + html
            html = re.sub(r'<html lang="en"', f'<html lang="{l}"', html, 1)
            html = html.replace('content="en_GB"', f'content="{LOCALE[l]}"')
            html = re.sub(r'("inLanguage": ?)"en"', lambda m: m.group(1) + f'"{l}"', html)
            html = html.replace(f"{SITE}{p}", f"{SITE}{lp}")
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
            alts = "\n".join(f'    <xhtml:link rel="alternate" hreflang="{lg}" href="{SITE}{g[lg]}"/>' for lg in ORDER if lg in g)
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{g["nl"]}"/>'
            multi = "\n    <xhtml:link" in b
            new = alts if multi else alts.replace("\n    ", "").replace("    <xhtml", "<xhtml")
            b = re.sub(r'(\s*<xhtml:link rel="alternate"[^>]*/>)+', lambda m: ("\n" if multi else "") + new, b, 1)
        out.append(b)
        if g and loc == g.get("en"):
            for l in NEW:
                if l in g:
                    out.append(b.replace(f"<loc>{SITE}{loc}</loc>", f"<loc>{SITE}{g[l]}</loc>"))
    s = s.replace("".join(blocks), "".join(out))
    sm.write_text(s, encoding="utf-8")
    tot = len(en_pages)
    print("i18n:", ", ".join(f"{l}: {n_new[l]}/{tot} pagina's" for l in NEW))

if __name__ == "__main__":
    main()
