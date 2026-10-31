# Price of Festivals (festivals/ subfolder of Price of Football)

A static, sourced comparison of UK festival ticket prices for 2027. Drop this whole folder into the
Price-of-Football repo root as `festivals/`. It will be served at
https://matthewallmark.github.io/Price-of-Football/festivals/

- Self-contained: every internal link and asset path is relative, so nothing in the main site changes.
  The only optional change to the main site is one link to `festivals/`, which Matthew handles himself.
- No robots.txt (robots.txt only works at the domain root). The sitemap is `festivals/sitemap.xml`; it can be
  submitted in Search Console or referenced from the main site's robots.txt if wanted.
- No 404.html (GitHub Pages only uses a root 404; the main site's 404 applies).
- Data: `data/festivals.json`. Every figure has `source_url`, `source_title`, `source_type` and `checked`.
  `null` means not found and is never estimated. `adult.days` is set only where the ticket label names fewer days than the festival dates.
- Rebuild: `python3 tools/build.py` (stdlib only). This writes `index.html`, `calendar.html`, `calculator.html`, `about.html`,
  one `<id>.html` per festival, `data/festivals.csv` and `sitemap.xml`.
- `tools/seed_data_2026-10-31.py` regenerates `data/festivals.json` from the hand-checked figures (checked 31 Oct 2026).
- TODO placeholders: the newsletter block (`newsletter()`), affiliate and sponsor slots (`affiliate_slot()`; **no affiliate IDs**),
  and the corrections email (`CORRECTIONS` in tools/build.py).
