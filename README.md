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

## Leagues and adding or updating data
The site already covers 116 clubs in five leagues: Premier League, Championship, League One, League Two and National League. `meta.leagues` in `data/clubs.json` sets the order. build.py groups, filters (`index.html?league=championship` etc.) and builds the coverage summary from that list, so adding a league means adding it to `meta.leagues` and adding club objects with that `league` value.

Every price field is `{value, source_title, source_url, source_type, checked, note}`:
- `source_type` is one of official, press, reference, guide, fan site, enthusiast or other. Fan guides such as Football Ground Guide are "other" and are only used when the page is dated.
- `value: null` renders as "—". **Never estimate, interpolate or derive a figure.** That includes filling a price from a tied rank, computing an advance price from a matchday one, or copying one listed price into both min and max unless the source says it's the only adult price. Put any context (stand, category, advance or matchday) in `note`.
- The £30 away cap applies only to the Premier League. For EFL and National League grounds, source the home club's away price: the club, the visiting club's published ticket details, or press.
- No ticket-resale or betting sites as sources (press articles reporting betting-firm research are fine), and no club badges or logos.

Then run `python3 tools/build.py`. It regenerates every HTML page, `data/clubs.csv` (including `_source_title` and `_source_type` columns), `sitemap.xml` and `robots.txt`.
