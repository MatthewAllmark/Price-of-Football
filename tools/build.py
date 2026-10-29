#!/usr/bin/env python3
"""Static site builder for Price of Football.
Usage:  python3 tools/build.py
Reads data/clubs.json and writes HTML pages, data/clubs.csv, sitemap.xml and robots.txt.
No dependencies beyond the Python 3 standard library."""
import json, csv, html, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
# TODO: set to the real domain before publishing (used for canonical URLs and sitemap.xml)
SITE_URL = "https://matthewallmark.github.io/Price-of-Football"
SITE = "Price of Football"

data = json.loads((ROOT / "data" / "clubs.json").read_text())
META, CLUBS = data["meta"], sorted(data["clubs"], key=lambda c: c["name"])
SEASON = META["season"]
FIELDS = [  # key, label, short label
    ("season_ticket_min", "Cheapest adult season ticket", "Season ticket from"),
    ("season_ticket_max", "Dearest adult season ticket", "Season ticket to"),
    ("matchday_min", "Cheapest adult matchday ticket", "Matchday from"),
    ("matchday_max", "Dearest adult matchday ticket", "Matchday to"),
    ("away_ticket", "Away ticket (league cap)", "Away ticket"),
    ("pint", "Pint of lager", "Pint"),
    ("pie", "Pie", "Pie"),
    ("programme", "Matchday programme", "Programme"),
]
e = html.escape

def money(v):
    if v is None: return "—"
    return f"£{v:,.0f}" if float(v).is_integer() and v >= 100 else f"£{v:,.2f}"

def fmt_date(s):
    return datetime.date.fromisoformat(s).strftime("%-d %b %Y")

def page(title, desc, path, body, extra_head="", depth=0):
    pre = "../" * depth
    canon = SITE_URL + "/" + path
    nav = [("index.html", "Prices"), ("calculator.html", "Away day calculator"), ("about.html", "About & methodology")]
    navhtml = "".join(f'<a href="{pre}{h}">{t}</a>' for h, t in nav)
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canon)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{e(canon)}">
<meta name="theme-color" content="#0f172a">
<link rel="stylesheet" href="{pre}css/style.css">
{extra_head}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="{pre}index.html"><span class="brand-mark">£</span> {SITE}</a>
<nav aria-label="Main">{navhtml}</nav>
</div></header>
<main id="main" class="wrap">
{body}
</main>
<footer class="site-footer"><div class="wrap">
<p><strong>{SITE}</strong> is an independent project and is not affiliated with, endorsed by or connected to the Premier League, any football club or any ticketing provider. Club names are used for identification only.</p>
<p>Prices are collected by hand from club websites and the press, and every figure links to its source. Prices change, can vary by seat, fixture and kiosk, and may be out of date or wrong — always check with the club before you buy. Where we could not find a figure from a source we trust we show “—”; we never estimate.</p>
<p>Data: {SEASON} {META['league']} season. Last full check {fmt_date(META['generated'])}. <a href="{pre}data/clubs.json">Download JSON</a> · <a href="{pre}data/clubs.csv">CSV</a> · <a href="{pre}about.html#corrections">Report a correction</a></p>
</div></footer>
</body>
</html>
"""

def newsletter(depth=0):
    return """<section class="newsletter" aria-labelledby="nl-h">
<h2 id="nl-h">Get price updates</h2>
<p>One short email when prices change or new clubs are added. No spam.</p>
<div class="nl-embed"><script async src="https://subscribe-forms.beehiiv.com/v3/loader.js" data-beehiiv-form="deb346d0-18cb-4841-9af7-22936ea0b6fc"></script></div>
<noscript><p><a href="https://matthews-newsletter-1fa3a3.beehiiv.com/subscribe">Subscribe on beehiiv</a></p></noscript>
</section>"""

def src_link(f):
    if f["value"] is None or not f["source_url"]: return "—"
    return f'<a href="{e(f["source_url"])}" rel="nofollow noopener" target="_blank">{e(f["source_title"])}</a>'

# ---------- home ----------
def build_home():
    def cell(c, k):
        v = c[k]["value"]
        sv = "" if v is None else v
        return f'<td data-v="{sv}" class="num{" empty" if v is None else ""}" title="{e(c[k]["note"])}">{money(v)}</td>'
    rows = []
    for c in CLUBS:
        cap = c["capacity"]["value"]
        rows.append(f'<tr data-name="{e(c["name"].lower())}">'
                    f'<th scope="row" data-v="{e(c["name"])}"><a href="clubs/{c["slug"]}.html">{e(c["name"])}</a><span class="sub">{e(c["stadium"]["value"])}</span></th>'
                    f'<td data-v="{cap}" class="num hide-sm">{cap:,}</td>'
                    + "".join(cell(c, k) for k, _, _ in FIELDS) + "</tr>")
    def best(k, rev=False):
        vals = [(c[k]["value"], c) for c in CLUBS if c[k]["value"] is not None]
        v, c = (max if rev else min)(vals, key=lambda t: t[0])
        return v, c
    cards = []
    for k, lbl, rev in [("season_ticket_min", "Cheapest season ticket", False), ("season_ticket_min", "Priciest entry-level season ticket", True),
                        ("pint", "Cheapest pint", False), ("pint", "Dearest pint", True)]:
        v, c = best(k, rev)
        cards.append(f'<div class="stat"><span class="stat-label">{lbl}</span><span class="stat-value">{money(v)}</span>'
                     f'<a href="clubs/{c["slug"]}.html">{e(c["name"])}</a></div>')
    filled = {k: sum(1 for c in CLUBS if c[k]["value"] is not None) for k, _, _ in FIELDS}
    heads = "".join(f'<th scope="col" class="num"><button type="button" data-k="{i+2}">{e(s)}</button></th>' for i, (k, l, s) in enumerate(FIELDS))
    body = f"""
<section class="hero">
<h1>What it really costs to watch Premier League football</h1>
<p class="lede">Season tickets, matchday tickets, away tickets, pints, pies and programmes for all 20 {META['league']} clubs in {SEASON} — every figure linked to its source, with the date we checked it.</p>
<div class="stats">{''.join(cards)}</div>
</section>
<section aria-labelledby="t-h">
<div class="table-tools">
<h2 id="t-h">{META['league']} prices {SEASON}</h2>
<div class="filters">
<label for="q" class="sr-only">Filter clubs</label>
<input id="q" type="search" placeholder="Filter clubs or grounds…" autocomplete="off">
<label class="chk"><input type="checkbox" id="complete"> Only clubs with matchday prices</label>
</div>
</div>
<p class="hint">Click a column heading to sort. “—” means we couldn’t find a trustworthy figure (we never guess). Hover a price for its note; click a club for sources and dates.</p>
<div class="table-wrap">
<table id="prices">
<thead><tr><th scope="col"><button type="button" data-k="0">Club</button></th><th scope="col" class="num hide-sm"><button type="button" data-k="1">Capacity</button></th>{heads}</tr></thead>
<tbody>
{''.join(rows)}
</tbody>
</table>
</div>
<p class="coverage">Coverage: {', '.join(f'{s} {filled[k]}/20' for k, l, s in FIELDS)}.</p>
</section>
<section class="seo-copy">
<h2>Cheapest season tickets in the Premier League</h2>
<p>Sort the “Season ticket from” column to rank clubs by their cheapest adult season ticket for {SEASON}. Many clubs sell a handful of restricted or family-area seats below their usual entry price, so read each club’s notes before comparing. Away tickets in the Premier League are capped at £30 for adults until at least the end of 2027/28.</p>
<h2>Price of a pint and a pie at every ground</h2>
<p>Pint and pie prices come from a club-by-club press survey and vary by kiosk and brand. Use the <a href="calculator.html">away day cost calculator</a> to add up a ticket, a pint, a pie, a programme and your train fare.</p>
</section>
{newsletter()}
<script src="js/table.js" defer></script>
"""
    desc = f"Compare {META['league']} {SEASON} ticket prices: cheapest and dearest season tickets, matchday tickets, £30 away tickets, and the price of a pint, pie and programme at all 20 grounds. Sourced and dated."
    (ROOT / "index.html").write_text(page(f"Premier League ticket prices {SEASON}: season tickets, pints & pies | {SITE}", desc, "", body))

# ---------- club pages ----------
def build_club(c):
    rows = []
    for k, lbl, _ in FIELDS:
        f = c[k]
        rows.append(f"""<tr><th scope="row">{e(lbl)}</th><td class="num big">{money(f['value'])}</td>
<td>{e(f['note']) if f['note'] else ''}<div class="src">Source: {src_link(f)}{(' <span class="tag">' + e(f['source_type']) + '</span>') if f['value'] is not None else ''}</div><div class="checked">Checked {fmt_date(f['checked'])}</div></td></tr>""")
    st, cap = c["stadium"], c["capacity"]
    pint, pie = c["pint"]["value"], c["pie"]["value"]
    name, ground = c["name"], st["value"]
    def q(k): return money(c[k]["value"])
    summary = []
    if c["season_ticket_min"]["value"] is not None:
        summary.append(f"The cheapest adult {name} season ticket for {SEASON} is {q('season_ticket_min')}" +
                       (f" and the dearest we found is {q('season_ticket_max')}" if c['season_ticket_max']['value'] is not None else "") + ".")
    if c["matchday_min"]["value"] is not None:
        summary.append(f"Adult matchday tickets range from {q('matchday_min')} to {q('matchday_max')}.")
    else:
        summary.append("We have not yet found a reliable adult matchday ticket price range.")
    if pint is not None:
        summary.append(f"A pint at {ground} costs {money(pint)}" + (f" and a pie {money(pie)}" if pie is not None else "") + ".")
    summary.append(f"Away fans pay no more than £30 under the Premier League cap.")
    others = "".join(f'<li><a href="{o["slug"]}.html">{e(o["name"])}</a></li>' for o in CLUBS if o["slug"] != c["slug"])
    ld = {"@context": "https://schema.org", "@type": "StadiumOrArena", "name": ground,
          "maximumAttendeeCapacity": cap["value"], "url": f"{SITE_URL}/clubs/{c['slug']}.html"}
    body = f"""
<nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Premier League prices</a> › {e(name)}</nav>
<h1>{e(name)} ticket prices {SEASON}</h1>
<p class="lede">{' '.join(e(s) for s in summary)}</p>
<dl class="facts">
<div><dt>Ground</dt><dd>{e(ground)}</dd></div>
<div><dt>Capacity</dt><dd>{cap['value']:,}</dd></div>
<div><dt>League</dt><dd>{e(c['league'])}</dd></div>
<div><dt>Season</dt><dd>{e(c['season'])}</dd></div>
</dl>
<p class="small">Ground and capacity source: {src_link(cap)} · checked {fmt_date(cap['checked'])}{(' · ' + e(cap['note'])) if cap['note'] else ''}</p>
<h2>{e(name)} prices, sources and dates</h2>
<div class="table-wrap"><table class="club-table">
<thead><tr><th scope="col">Item</th><th scope="col" class="num">Price</th><th scope="col">Details, source and date checked</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
{('<p class="note">' + e(c['notes']) + '</p>') if c['notes'] else ''}
<p><a class="btn" href="../calculator.html?club={c['slug']}">Work out an away day at {e(ground)} →</a></p>
<h2>Price of a pint at {e(ground)}</h2>
<p>{('A pint of lager at ' + e(ground) + ' costs ' + money(pint) + ' in ' + SEASON + ', according to the source above. Prices vary by kiosk, brand and promotion.') if pint is not None else 'We have not found a reliable pint price for ' + e(ground) + ' yet.'}</p>
<p>Spotted a wrong or outdated price? See <a href="../about.html#corrections">how to report a correction</a>.</p>
{newsletter(1)}
<section class="others"><h2>Other clubs</h2><ul class="club-list">{others}</ul></section>
"""
    desc = (f"{name} ticket prices {SEASON}: season tickets from {q('season_ticket_min')}, matchday tickets, £30 away tickets and the price of a pint and pie at {ground}. Every price sourced and dated.")
    head = f'<script type="application/ld+json">{json.dumps(ld)}</script>'
    (ROOT / "clubs" / f"{c['slug']}.html").write_text(
        page(f"{name} ticket prices {SEASON} – season tickets, pint & pie at {ground} | {SITE}", desc, f"clubs/{c['slug']}.html", body, head, depth=1))

# ---------- calculator ----------
def build_calc():
    opts = "".join(f'<option value="{c["slug"]}">{e(c["name"])} – {e(c["stadium"]["value"])}</option>' for c in CLUBS)
    body = f"""
<h1>Away day cost calculator</h1>
<p class="lede">Pick the ground you’re visiting. We fill in the £30 away ticket cap and that ground’s pint, pie and programme prices from our database — change any figure, add your train fare, and see the total.</p>
<form id="calc" class="calc" onsubmit="return false">
<div class="field full"><label for="club">Ground you’re visiting</label>
<select id="club"><option value="">Choose a club…</option>{opts}</select></div>
<div class="field"><label for="ticket">Away ticket (£)</label><input id="ticket" type="number" min="0" step="0.01" inputmode="decimal" value="30"></div>
<div class="field"><label for="pint">Pint (£)</label><input id="pint" type="number" min="0" step="0.01" inputmode="decimal"></div>
<div class="field"><label for="pints">Number of pints</label><input id="pints" type="number" min="0" step="1" value="1"></div>
<div class="field"><label for="pie">Pie (£)</label><input id="pie" type="number" min="0" step="0.01" inputmode="decimal"></div>
<div class="field"><label for="prog">Programme (£)</label><input id="prog" type="number" min="0" step="0.01" inputmode="decimal"></div>
<div class="field"><label for="rail">Rail fare, return (£) <span class="opt">optional</span></label><input id="rail" type="number" min="0" step="0.01" inputmode="decimal" placeholder="e.g. 45.60"></div>
</form>
<div class="result" aria-live="polite">
<p class="total-label">Your away day</p>
<p class="total" id="total">£30.00</p>
<ul id="breakdown"></ul>
<p class="small" id="missing"></p>
</div>
<p class="small">Away ticket: Premier League adult away tickets are capped at £30 (<a href="https://www.premierleague.com/en/news/4617247/premier-league-statement-on-30-pounds-cap-on-away-tickets" target="_blank" rel="noopener">Premier League statement, 19 Mar 2026</a>); some clubs charge less and concessions are cheaper. Food and drink prices are for the home ground and come from the sources on each club page. Blank fields mean we have no reliable figure — type your own.</p>
{newsletter()}
<script>window.POF_CLUBS = {json.dumps({c['slug']: {k: c[k]['value'] for k in ('away_ticket','pint','pie','programme')} | {'name': c['name'], 'ground': c['stadium']['value']} for c in CLUBS})};</script>
<script src="js/calculator.js" defer></script>
"""
    desc = "Work out what a Premier League away day costs: £30 away ticket, pint, pie, programme and your rail fare, using sourced prices for every ground."
    (ROOT / "calculator.html").write_text(page(f"Away day cost calculator – ticket, pint, pie & train | {SITE}", desc, "calculator.html", body))

# ---------- about ----------
def build_about():
    srcs = {}
    for c in CLUBS:
        for k in ["stadium", "capacity"] + [f[0] for f in FIELDS]:
            f = c[k]
            if f["source_url"]: srcs.setdefault(f["source_url"], (f["source_title"], f["source_type"], set()))[2].add(c["name"])
    order = {"official": 0, "press": 1, "reference": 2, "guide": 3, "fan site": 4, "enthusiast": 5}
    li = "".join(f'<li><span class="tag">{e(t)}</span> <a href="{e(u)}" target="_blank" rel="nofollow noopener">{e(ti)}</a> <span class="small">({len(cl)} club{"s" if len(cl)!=1 else ""})</span></li>'
                 for u, (ti, t, cl) in sorted(srcs.items(), key=lambda kv: (order.get(kv[1][1], 9), kv[1][0])))
    d = META["definitions"]
    defs = "".join(f"<li><strong>{e(l)}</strong>: {e(d[k])}</li>" for k, l, _ in FIELDS)
    body = f"""
<h1>About Price of Football &amp; our methodology</h1>
<p class="lede">Price of Football is an independent, unaffiliated database of what it costs to watch UK football. Version 1 covers the 20 {META['league']} clubs for the {SEASON} season.</p>
<h2>Independent and unaffiliated</h2>
<p>We are not connected to, sponsored by or endorsed by the Premier League, the EFL, any club, any ticket seller or any brewer. Club and competition names are used only to identify them. We deliberately don’t use club badges, crests or logos.</p>
<h2>Where the numbers come from</h2>
<ol>
<li><strong>Club websites first</strong> — official ticketing pages, price lists and announcements.</li>
<li><strong>Reputable press second</strong> — national and local newspapers (e.g. BBC Sport, The Mirror, Manchester Evening News, Liverpool Echo, Birmingham Mail, local titles) and GiveMeSport, where the club’s own figures couldn’t be read.</li>
<li><strong>Other sources only when labelled</strong> — a small number of figures come from fan sites, a ticket-guide site or a programme-collector site. These are tagged on each club page so you can judge them.</li>
</ol>
<p>Stadium names and capacities are taken from the Wikipedia 2026–27 Premier League article (which cites club sources). Pint and pie prices come from a single press survey in which the newspaper contacted every club, so they’re comparable but are not club-published price lists.</p>
<h2>Rules we follow</h2>
<ul>
<li>Every figure has a source link and the date we last checked it.</li>
<li>If we can’t find a figure from a source we trust, we show “—”. <strong>We never estimate, interpolate or guess.</strong></li>
<li>Where sources disagree we use the club’s own figure if we can read it, otherwise the most specific press report, and we say so in the note.</li>
<li>Prices are adult, general admission and exclude hospitality unless the note says otherwise.</li>
</ul>
<h2>What each column means</h2>
<ul>{defs}</ul>
<h2>Known limitations</h2>
<ul>
<li>Several clubs publish prices only as images, behind log-ins, or individually to season ticket holders (e.g. Sunderland, Fulham), so some figures rely on press reports.</li>
<li>Clubs often sell a few restricted or family-area seats below their usual entry price; compare notes, not just numbers.</li>
<li>Matchday prices depend on the fixture category, which clubs set match by match.</li>
</ul>
<h2 id="corrections">Corrections</h2>
<p>If a price is wrong or out of date, please send the correct figure with a link to the club’s page. <!-- TODO: add a contact email or form before publishing. --> Contact details will be added before launch.</p>
<h2>Every source used</h2>
<ul class="sources">{li}</ul>
{newsletter()}
"""
    desc = "How Price of Football collects ticket, pint and pie prices: club websites first, reputable press second, every figure sourced and dated. Independent and unaffiliated."
    (ROOT / "about.html").write_text(page(f"About & methodology | {SITE}", desc, "about.html", body))

def build_csv():
    with open(ROOT / "data" / "clubs.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        hdr = ["slug", "name", "league", "season", "stadium", "capacity"]
        for k, _, _ in FIELDS: hdr += [k, k + "_source_url", k + "_checked", k + "_note"]
        w.writerow(hdr)
        for c in CLUBS:
            r = [c["slug"], c["name"], c["league"], c["season"], c["stadium"]["value"], c["capacity"]["value"]]
            for k, _, _ in FIELDS:
                f = c[k]; r += ["" if f["value"] is None else f["value"], f["source_url"], f["checked"], f["note"]]
            w.writerow(r)

def build_seo():
    today = META["generated"]
    urls = ["", "calculator.html", "about.html"] + [f"clubs/{c['slug']}.html" for c in CLUBS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "".join(f"  <url><loc>{SITE_URL}/{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sm)
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")

build_home(); build_calc(); build_about(); build_csv(); build_seo()
for c in CLUBS: build_club(c)
print("built", len(CLUBS), "club pages")
