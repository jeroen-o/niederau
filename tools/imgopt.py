#!/usr/bin/env python3
"""Voegt srcset/sizes toe aan <img>-tags van foto's in assets/img (alleen waar verkleinde varianten bestaan)."""
import pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
_w = {}

def width(name):
    if name not in _w:
        out = subprocess.run(["identify", "-format", "%w", str(IMG / name) + "[0]"], capture_output=True, text=True).stdout
        _w[name] = int(out) if out.strip().isdigit() else 0
    return _w[name]

GRID_SIZES = "(max-width: 760px) 50vw, 300px"

def sizes_for(tag):
    if 'class="card-img"' in tag: return "(max-width: 760px) calc(100vw - 32px), 420px"
    if 'class="side-img"' in tag: return "(max-width: 860px) calc(100vw - 32px), 560px"
    return "(max-width: 800px) calc(100vw - 32px), 640px"

def fix(tag, sizes=None):
    if "srcset=" in tag: return tag
    s = re.search(r'src="((?:\.\./)*/?assets/img/)([^"/]+)\.webp"', tag)
    if not s: return tag
    pre, stem = s.group(1), s.group(2)
    if re.search(r"-(480|900|hero-\d+)$", stem): return tag
    parts = [f"{pre}{stem}-{t}.webp {t}w" for t in (480, 900) if (IMG / f"{stem}-{t}.webp").exists()]
    if not parts: return tag
    parts.append(f"{pre}{stem}.webp {width(stem + '.webp')}w")
    return tag.replace(s.group(0), s.group(0) + f' srcset="{", ".join(parts)}" sizes="{sizes or sizes_for(tag)}"', 1)

def process(h):
    h = re.sub(r'(<a class="g-item"[^>]*>\s*)(<img\b[^>]*>)', lambda m: m.group(1) + fix(m.group(2), GRID_SIZES), h)
    return re.sub(r"<img\b[^>]*>", lambda m: fix(m.group(0)), h)

def main():
    n = 0
    for p in ROOT.rglob("index.html"):
        if p.relative_to(ROOT).parts[0] in ("assets", "tools"): continue
        h = p.read_text(encoding="utf-8")
        h2 = process(h)
        if h2 != h:
            p.write_text(h2, encoding="utf-8"); n += 1
    print(f"srcset toegevoegd in {n} pagina's")

if __name__ == "__main__":
    main()
