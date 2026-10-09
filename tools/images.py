#!/usr/bin/env python3
"""Maakt verkleinde varianten (-480, -900) van alle foto's in assets/img; bestaande varianten blijven staan."""
import pathlib, re, subprocess

IMG = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img"
WIDTHS = (480, 900)
SKIP = re.compile(r"(-\d{3,4}\.webp|-hero-\d+\.webp|-1200x630)")

def width(p):
    out = subprocess.run(["identify", "-format", "%w", str(p) + "[0]"], capture_output=True, text=True).stdout
    return int(out) if out.strip().isdigit() else 0

def main():
    made = 0
    for p in sorted(IMG.glob("*.webp")):
        if SKIP.search(p.name): continue
        w = None
        for target in WIDTHS:
            v = IMG / f"{p.stem}-{target}.webp"
            if v.exists(): continue
            w = w or width(p)
            if w <= target + 40: continue  # origineel is al klein genoeg
            subprocess.run(["convert", str(p), "-resize", f"{target}x", "-quality", "78", str(v)], check=True)
            made += 1
    print(f"afbeeldingsvarianten: {made} nieuw gemaakt")

if __name__ == "__main__":
    main()
