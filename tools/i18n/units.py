"""Gedeelde logica: vertaaleenheden uit een gebouwde EN-pagina halen en (vertaald) terugzetten.

Een eenheid is de innerHTML van een 'leaf-blok' (element zonder blok-kinderen) of een losse tekstnode,
plus tekst-attributen (alt, title, aria-label, placeholder, content van meta's) en JSON-LD-tekstvelden."""
import json, re
from bs4 import BeautifulSoup, NavigableString, Comment
from bs4.formatter import HTMLFormatter

class _Fmt(HTMLFormatter):
    def attributes(self, tag):  # originele volgorde behouden (standaard sorteert bs4)
        return list((tag.attrs or {}).items())

FMT = _Fmt(void_element_close_prefix=None)
PARSER = "html.parser"

def dump(soup): return soup.decode(formatter=FMT)

BLOCK = {"p","li","ul","ol","div","section","article","aside","header","footer","nav","main","h1","h2","h3","h4","h5","h6",
         "table","thead","tbody","tr","td","th","figure","figcaption","details","summary","dl","dt","dd","form","select","option",
         "button","label","blockquote","address","body","html","head","fieldset"}
SKIP = {"script","style","svg","noscript","template","code","pre"}
ATTRS = ("alt","title","aria-label","placeholder")
META_NAMES = {"description","twitter:title","twitter:description"}
META_PROPS = {"og:title","og:description","og:image:alt","og:site_name"}
LD_KEYS = {"name","description","headline","text","alternateName","caption","abstract","disambiguatingDescription","articleBody","slogan"}

def has_text(s): return bool(re.search(r"[A-Za-zÀ-ɏ]", s))

def has_block(e):
    return any(getattr(d, "name", None) in BLOCK for d in e.descendants)

def inner(e):
    out = "".join(c.decode(formatter=FMT) if not isinstance(c, NavigableString) else c.output_ready(formatter=FMT) for c in e.contents).strip()
    # vaste datum in 'laatst bijgewerkt' -> token, zodat finalize.py de datum per pagina zet
    return re.sub(r'(<time datetime=")\d{4}-\d\d-\d\d(">)[^<]*(</time>)', r'\1@@LASTMOD@@\2@@LASTMOD_H@@\3', out)

def walk(root, out):
    for c in list(root.children):
        if isinstance(c, Comment): continue
        if isinstance(c, NavigableString):
            if c.strip() and has_text(str(c)):
                out.append((("text", c), str(c).strip()))
            continue
        n = c.name
        if n in SKIP: continue
        for a in ATTRS:
            v = c.get(a)
            if v and has_text(v): out.append((("attr", c, a), v.strip()))
        if n == "br" or n == "img": continue
        if has_block(c):
            walk(c, out)
        elif c.get_text(strip=True) and has_text(c.get_text()):
            out.append((("inner", c), inner(c)))

def ld_walk(o, out, key=None):
    if isinstance(o, dict):
        for k, v in o.items(): ld_walk(v, out, k)
    elif isinstance(o, list):
        for v in o: ld_walk(v, out, key)
    elif isinstance(o, str) and key in LD_KEYS and has_text(o):
        out.append(o)

def extract(html):
    soup = BeautifulSoup(html, PARSER)
    out = []
    if soup.title and soup.title.string: out.append((("title", soup.title), soup.title.string.strip()))
    for m in soup.find_all("meta"):
        if (m.get("name") in META_NAMES or m.get("property") in META_PROPS) and m.get("content"):
            out.append((("attr", m, "content"), m["content"].strip()))
    if soup.body: walk(soup.body, out)
    for s in soup.find_all("script", type="application/ld+json"):
        strs = []; ld_walk(json.loads(s.string), strs)
        for t in strs: out.append((("ld", s, t), t))
    return soup, out

TAG = re.compile(r"<(/?)([a-zA-Z0-9]+)([^>]*)>")

def mask(s):
    s = re.sub(r"<br\s*/?>", "<br/>", s)
    s = s.replace("&amp;", "&")
    """Open-tags met attributen -> <tagN>; geeft (masked, [originele open-tags])."""
    store = []
    def r(m):
        if m.group(1): return m.group(0)
        if not m.group(3).strip() or m.group(2) == "br": return m.group(0)
        store.append(m.group(0))
        return f"<{m.group(2)}{len(store)}>"
    # closing tags van gemaskeerde tags blijven </a>; volgorde blijft gelijk
    return TAG.sub(r, s), store

def unmask(t, store):
    """Zet attributen terug; None als de tags niet kloppen."""
    def r(m):
        if m.group(1): return m.group(0)
        mm = re.fullmatch(r"([a-zA-Z]+)(\d+)", m.group(2))
        if mm and not m.group(3).strip():
            i = int(mm.group(2)) - 1
            if 0 <= i < len(store) and store[i].startswith("<" + mm.group(1)): return store[i]
            raise ValueError
        return m.group(0)
    try: out = TAG.sub(r, t)
    except ValueError: return None
    return out

def sig(s):
    return sorted(re.findall(r"<[^>]+>|@@\w+@@", mask(s)[0]))

def apply_unit(h, t, tr):
    """Zet de vertaling van één eenheid terug; geeft de bron-tekst terug als de vertaling ontbreekt, anders None."""
    m, store = mask(t)
    v = tr.get(m)
    if v is None: return t
    v = unmask(v, store)
    if v is None: return t
    k = h[0]
    if k == "text": h[1].replace_with(NavigableString(v))
    elif k == "attr": h[1][h[2]] = v
    elif k == "title": h[1].string = v
    elif k == "inner":
        h[1].clear()
        for ch in list(BeautifulSoup(v, PARSER).contents): h[1].append(ch)
    elif k == "ld":
        d = json.loads(h[1].string)
        def rep(o, key=None):
            if isinstance(o, dict): return {a: rep(b, a) for a, b in o.items()}
            if isinstance(o, list): return [rep(b, key) for b in o]
            if isinstance(o, str) and key in LD_KEYS and o == h[2]: return v
            return o
        h[1].string = json.dumps(rep(d), ensure_ascii=False)
    return None
