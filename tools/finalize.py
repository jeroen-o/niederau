#!/usr/bin/env python3
"""Zet per pagina een echte 'laatst gewijzigd'-datum.

Elke gegenereerde pagina bevat tijdelijke tokens (@@LASTMOD@@, @@LASTMOD_H@@). Dit script hasht de pagina
(zonder datum); is de hash gelijk aan die in tools/data/_lastmod.json, dan blijft de oude datum staan,
anders wordt het vandaag. Daarna worden de tokens vervangen (JSON-LD dateModified, zichtbare 'Laatst
bijgewerkt') en krijgt elke URL in sitemap.xml dezelfde datum als lastmod."""
import datetime, hashlib, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAN = ROOT / "tools" / "data" / "_lastmod.json"
TODAY = datetime.date.today()
manifest = json.loads(MAN.read_text()) if MAN.exists() else {}

MONTHS = {
    "nl": ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    "it": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"],
    "sv": ["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"],
    "no": ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"],
    "fi": ["tammikuuta", "helmikuuta", "maaliskuuta", "huhtikuuta", "toukokuuta", "kesäkuuta", "heinäkuuta", "elokuuta", "syyskuuta", "lokakuuta", "marraskuuta", "joulukuuta"],
    "da": ["januar", "februar", "marts", "april", "maj", "juni", "juli", "august", "september", "oktober", "november", "december"],
    "pl": ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca", "sierpnia", "września", "października", "listopada", "grudnia"],
}

def human(d, lang):
    if lang == "en": return f"{d.day} {MONTHS['en'][d.month - 1]} {d.year}"
    if lang == "fr": return f"{d.day if d.day > 1 else '1er'} {MONTHS['fr'][d.month - 1]} {d.year}"
    if lang == "es": return f"{d.day} de {MONTHS['es'][d.month - 1]} de {d.year}"
    if lang in ("it", "sv"): return f"{d.day} {MONTHS[lang][d.month - 1]} {d.year}"
    if lang in ("no", "da", "fi"): return f"{d.day}. {MONTHS[lang][d.month - 1]} {d.year}"
    if lang == "pl": return f"{d.day} {MONTHS['pl'][d.month - 1]} {d.year}"
    if lang == "de": return f"{d.day}. {MONTHS['de'][d.month - 1]} {d.year}"
    return f"{d.day} {MONTHS['nl'][d.month - 1]} {d.year}"

dates = {}
new_manifest = {}
for f in sorted(ROOT.rglob("index.html")):
    rel = f.relative_to(ROOT).as_posix()
    if rel.startswith(("node_modules/", ".git/")): continue
    t = f.read_text(encoding="utf-8")
    if "@@LASTMOD@@" not in t:
        continue
    h = hashlib.sha1(t.encode("utf-8")).hexdigest()
    old = manifest.get(rel)
    date = old["date"] if old and old["hash"] == h else TODAY.isoformat()
    new_manifest[rel] = {"hash": h, "date": date}
    lang = (re.search(r'<html lang="(\w+)"', t) or [None, "nl"])[1]
    d = datetime.date.fromisoformat(date)
    t = t.replace("@@LASTMOD_H@@", human(d, lang)).replace("@@LASTMOD@@", date)
    f.write_text(t, encoding="utf-8")
    dates["/" + rel[:-len("index.html")]] = date

MAN.write_text(json.dumps(new_manifest, indent=0, sort_keys=True))

sm = ROOT / "sitemap.xml"
s = sm.read_text(encoding="utf-8")
def fix(m):
    path = m.group(1).replace("https://niederau.nl", "")
    return m.group(0).replace(m.group(2), dates.get(path, m.group(2)))
s = re.sub(r"<loc>(.*?)</loc><lastmod>(.*?)</lastmod>", fix, s)
sm.write_text(s, encoding="utf-8")
print(f"lastmod gezet voor {len(dates)} pagina's ({sum(1 for p in new_manifest.values() if p['date'] == TODAY.isoformat())} gewijzigd vandaag)")
