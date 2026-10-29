# Price of Football — v1 (local build only)

Static site: sortable, source-linked database of what it costs to watch Premier League clubs, **2026/27 season**.
No backend, no dependencies beyond Python 3 standard library to build. Not deployed anywhere.

## Structure
- `data/clubs.json` — the source of truth. Each price field is `{value, source_title, source_url, source_type, checked, note}`; `value: null` = not found (shown as "—", never estimated).
- `data/clubs.csv` — generated flat export.
- `tools/build.py` — regenerates all HTML, CSV, `sitemap.xml`, `robots.txt` from the JSON. Run `python3 tools/build.py`.
- `tools/seed_data.py` — the script that wrote the v1 JSON (kept for provenance; edit the JSON directly going forward).
- `tools/screenshots.py` — Playwright screenshots (`/tmp/pwvenv/bin/python tools/screenshots.py`).
- `index.html`, `clubs/*.html`, `calculator.html`, `about.html`, `css/`, `js/`.

## Preview
`python3 -m http.server -d /workspace/price-of-football 8000` then open http://localhost:8000

## Before publishing (TODOs)
- Set `SITE_URL` in `tools/build.py` (currently `https://www.example.com`) and rebuild — used in canonical tags and sitemap.
- Wire the newsletter form (`newsletter()` in build.py) to a provider.
- Add a corrections contact on the About page.

## Extending to the Championship
Add club objects with `"league": "Championship"` to `data/clubs.json` (same schema); for the away ticket field the
PL £30 cap does not apply, so source each club's away price. Then extend build.py to group/filter by league.
