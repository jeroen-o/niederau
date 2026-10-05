# Niederau.nl

Persoonlijke gids over Niederau in de Wildschönau (Tirol), in het Nederlands, Engels en Duits.

- `index.html`: Nederlands, `en/index.html`: Engels, `de/index.html`: Duits
- `assets/style.css` en `assets/main.js`: gedeeld, zonder externe afhankelijkheden of build-stap
- **Seizoensversie:** van 1 oktober tot 1 april toont de site automatisch de winterversie, van 1 april tot 1 oktober de zomerversie. Bezoekers kunnen ook zelf wisselen met de knop in het menu.
- `CNAME` staat op `niederau.nl` (voor GitHub Pages)
- **Bouwen:** pas `index.html` aan en draai `./tools/build.sh`. Dat maakt de Engelse en Duitse versie (`tools/translate.py`) en werkt SEO/GEO bij (`tools/seo.py`: geo-tags, Open Graph, JSON-LD met FAQ, `sitemap.xml`, `llms.txt`).
- Werkafspraken staan in `CLAUDE.md`.

## Publiceren via GitHub Pages
Settings → Pages → Deploy from branch → kies de branch en `/ (root)`. Laat daarna bij je domeinregistrar de DNS van `niederau.nl` naar GitHub Pages wijzen.
