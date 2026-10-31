#!/usr/bin/env python3
"""Static site builder for Price of Festivals.
Usage:  python3 tools/build.py
Reads data/festivals.json and writes all HTML pages, data/festivals.csv and sitemap.xml.
This folder is published as the festivals/ subfolder of the Price-of-Football GitHub Pages repo.
All internal links are relative, so the folder works under any base path.
Standard library only."""
import json, csv, html, pathlib, datetime, statistics

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Public base URL of this folder (used only for canonical URLs, og:url and sitemap.xml)
SITE_URL = "https://matthewallmark.github.io/Price-of-Football/festivals"
POF_URL = "https://matthewallmark.github.io/Price-of-Football/"
SITE = "Price of Festivals"
CORRECTIONS = "corrections@example.com"  # TODO: replace with a real corrections address before launch

data = json.loads((ROOT / "data" / "festivals.json").read_text())
META = data["meta"]
FESTS = sorted(data["festivals"], key=lambda f: (f["start"], f["name"]))
ED = META["edition"]
e = html.escape
STATUS = {"on_sale": "On sale", "sold_out": "Sold out", "coming_soon": "Coming soon", "sale_held": "Sale held", "unknown": "Check site"}
CAMP = {"included": "Camping included", "optional": "Camping or non-camping", "available": "Camping available", "none": "No camping", "unknown": "—"}
FEES = {"included": "incl. booking fee", "extra": "+ booking fee", "unknown": "fees not stated", None: ""}
STYPE = {"official": "Official", "agent": "Ticket agent", "press": "Press", "other": "Guide"}

def d(s): return datetime.date.fromisoformat(s)
def fmt_date(s): return d(s).strftime("%-d %b %Y")
def date_range(f):
    a, b = d(f["start"]), d(f["end"])
    if a.month == b.month: return f"{a.day}–{b.day} {b.strftime('%b %Y')}"
    return f"{a.strftime('%-d %b')} – {b.strftime('%-d %b %Y')}"
def ndays(f): return (d(f["end"]) - d(f["start"])).days + 1
def money(v):
    if v is None: return "—"
    if v == 0: return "Free"
    return f"£{v:,.0f}" if float(v).is_integer() else f"£{v:,.2f}"
def ticket_days(f):
    a = f.get("adult") or {}
    return a.get("days") or ndays(f)
def per_day(f):
    a = f.get("adult")
    if not a or a["value"] in (None, 0): return None
    if f.get("dates_basis") != "festival" and not a.get("days"): return None
    return round(a["value"] / ticket_days(f), 2)
NATIONS = ["England", "Scotland", "Wales", "Northern Ireland"]
def nation_line():
    parts = []
    for n in NATIONS:
        c = sum(1 for f in FESTS if f.get("nation") == n)
        if c: parts.append(f"{c} in {n}")
    return ", ".join(parts)
def place(f): return ", ".join(x for x in (f.get("venue"), f.get("county")) if x)

def page(title, desc, path, body, depth=0, extra_head=""):
    pre = "../" * depth
    canon = SITE_URL + "/" + ("" if path == "index.html" else path)
    nav = [("index.html", "Prices"), ("calendar.html", "On-sale calendar"), ("calculator.html", "Budget calculator"), ("about.html", "About & methodology")]
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
<div class="xlink"><div class="wrap">Also from Price of Football: <a href="{POF_URL}">what it costs to watch football in the UK</a></div></div>
<main id="main" class="wrap">
{body}
</main>
<footer class="site-footer"><div class="wrap">
<p><strong>{SITE}</strong> is an independent project. It is not affiliated with, endorsed by or connected to any festival, promoter or ticket agent. Festival names are used for identification only.</p>
<p>Prices are collected by hand from festival websites and official ticket pages, and every figure links to its source with the date we checked it. Prices change by tier and sell out. Where we could not find a figure from a source we trust we show “—”; we never estimate. Always check the official seller before you buy, and never buy from unofficial resellers.</p>
<p>Also from <a href="{POF_URL}">Price of Football</a>, the cost of watching UK football.</p>
<p>Data: {ED} festival season, {len(FESTS)} festivals. Last full check {fmt_date(META['generated'])}. <a href="{pre}data/festivals.json">Download JSON</a> · <a href="{pre}data/festivals.csv">CSV</a> · <a href="{pre}about.html#corrections">Report a correction</a></p>
</div></footer>
</body>
</html>
"""

def newsletter():
    # TODO(newsletter): no provider is wired up. Replace this block with the embed from the chosen free
    # newsletter provider (e.g. the existing beehiiv account) once Matthew has approved it.
    return """<section class="newsletter" aria-labelledby="nl-h">
<h2 id="nl-h">Get on-sale alerts</h2>
<p>One short email when early birds drop, tiers go up or festivals sell out. No spam.</p>
<div class="todo" style="background:#1e293b;color:#e2e8f0;border-color:#7c3aed"><strong>TODO: newsletter signup</strong>No newsletter provider is connected yet. This box gets replaced by the signup form.</div>
</section>"""

def affiliate_slot(kind, f=None):
    # TODO(affiliate): placeholder only. No affiliate IDs are inserted anywhere on this site.
    what = {"tickets": "Ticket link slot: an approved official ticket-agent affiliate link (e.g. See Tickets or Skiddle via their programmes) can go here once approved. Until then, use the official seller linked above.",
            "gear": "Camping gear slot: e.g. Go Outdoors / Blacks (Awin) or Amazon UK Associates. No IDs are inserted yet.",
            "stay": "Places to stay slot: e.g. Booking.com affiliate (for non-camping festivals). No IDs are inserted yet.",
            "sponsor": "Sponsor slot: a featured listing or sponsor message, clearly labelled as advertising."}[kind]
    return f'<aside class="todo" data-slot="{kind}"><strong>TODO: affiliate/sponsor placeholder</strong>{e(what)}</aside>'

def src_link(p, pre=""):
    if not p or not p.get("source_url"): return ""
    return (f'<span class="tag">{e(STYPE.get(p.get("source_type"), "Source"))}</span> '
            f'<a href="{e(p["source_url"])}" rel="nofollow noopener" target="_blank">{e(p["source_title"])}</a> '
            f'<span class="checked">checked {fmt_date(p["checked"])}</span>')

# ---------- index ----------
def build_index():
    priced = [f for f in FESTS if f.get("adult") and f["adult"]["value"]]
    pdays = [(per_day(f), f) for f in priced if per_day(f)]
    cheapest_pd = min(pdays, key=lambda x: x[0]) if pdays else None
    med = statistics.median([f["adult"]["value"] for f in priced]) if priced else None
    lo = min(priced, key=lambda f: f["adult"]["value"]); hi = max(priced, key=lambda f: f["adult"]["value"])
    regions = sorted({f["region"] for f in FESTS if f.get("region")})
    months = sorted({f["start"][:7] for f in FESTS})
    rows = []
    for f in FESTS:
        a = f.get("adult"); pd = per_day(f)
        av = "" if not a else a["value"]
        rows.append(f"""<tr data-name="{e(f['name'].lower())} {e(place(f).lower())}" data-region="{e(f.get('region',''))}" data-nation="{e(f.get('nation',''))}" data-camp="{e(f['camping'])}" data-status="{e(f['status'])}" data-month="{f['start'][:7]}">
<th scope="row" data-v="{e(f['name'])}"><a href="{f['id']}.html">{e(f['name'])}</a><span class="sub">{e(place(f) or 'Location not confirmed')}</span></th>
<td data-v="{d(f['start']).toordinal()}">{date_range(f)}</td>
<td class="hide-sm" data-v="">{e(f.get('region') or '—')}</td>
<td class="hide-sm" data-v="">{e(CAMP[f['camping']])}</td>
<td class="num{' empty' if not a else ''}" data-v="{av}">{money(a['value']) if a else '—'}{f'<span class="sub">{e(FEES[a.get("fees")])}</span>' if a else ''}</td>
<td class="num{' empty' if pd is None else ''}" data-v="{'' if pd is None else pd}">{money(pd) if pd is not None else '—'}</td>
<td data-v=""><span class="status st-{f['status']}">{STATUS[f['status']]}</span></td>
</tr>""")
    nations = [n for n in NATIONS if any(f.get("nation") == n for f in FESTS)]
    nopts = "".join(f'<option value="{e(n)}">{e(n)}</option>' for n in nations)
    ropts = "".join(f'<option value="{e(r)}">{e(r)}</option>' for r in regions)
    mopts = "".join(f'<option value="{m}">{datetime.date.fromisoformat(m + "-01").strftime("%B %Y")}</option>' for m in months)
    stats = f"""<div class="stats">
<div class="stat"><span class="stat-label">Festivals tracked</span><span class="stat-value">{len(FESTS)}</span><span class="small">{len(priced)} with a sourced {ED} adult price</span></div>
<div class="stat"><span class="stat-label">Median adult ticket</span><span class="stat-value">{money(med)}</span><span class="small">across the {len(priced)} priced festivals</span></div>
<div class="stat"><span class="stat-label">Cheapest per day</span><span class="stat-value">{money(cheapest_pd[0]) if cheapest_pd else '—'}</span><span class="small">{e(cheapest_pd[1]['name']) if cheapest_pd else ''}</span></div>
<div class="stat"><span class="stat-label">On sale now</span><span class="stat-value">{sum(1 for f in FESTS if f['status']=='on_sale')}</span><span class="small">festivals with {ED} tickets on sale</span></div>
</div>"""
    body = f"""<h1>UK festival ticket prices {ED}, compared</h1>
<p class="lede">Compare the cheapest adult ticket, price per day, camping, parking and on-sale status for {len(FESTS)} UK festivals in {ED}: {nation_line()}. Every price links to the festival's own page or official ticket agent, and we show the date we checked it.</p>
{stats}
<p class="notice">Prices go up tier by tier and sell out. The figure shown is the cheapest adult full-festival ticket we found on sale (or last on sale) when we checked. Always confirm with the official seller.</p>
<div class="table-tools"><h2 id="t-h">All festivals</h2>
<div class="filters">
<label class="sr-only" for="q">Search</label><input type="search" id="q" placeholder="Search festival or place">
<label class="sr-only" for="nation">Nation</label><select id="nation"><option value="">All nations</option>{nopts}</select>
<label class="sr-only" for="region">Region</label><select id="region"><option value="">All regions</option>{ropts}</select>
<label class="sr-only" for="month">Month</label><select id="month"><option value="">Any month</option>{mopts}</select>
<label class="sr-only" for="camp">Camping</label><select id="camp"><option value="">Any camping</option><option value="included">Camping included</option><option value="optional">Camping or non-camping</option><option value="none">No camping</option></select>
<label class="chk"><input type="checkbox" id="onsale"> On sale only</label>
<label class="chk"><input type="checkbox" id="priced"> Priced only</label>
<button type="button" id="reset">Reset</button>
</div></div>
<p class="small" id="count" aria-live="polite"></p>
<div class="table-wrap"><table id="prices">
<thead><tr>
<th scope="col"><button data-k="0">Festival</button></th>
<th scope="col"><button data-k="1">Dates</button></th>
<th scope="col" class="hide-sm">Region</th>
<th scope="col" class="hide-sm">Camping</th>
<th scope="col" class="num"><button data-k="4">Adult ticket</button></th>
<th scope="col" class="num"><button data-k="5">Per day</button></th>
<th scope="col">Status</th>
</tr></thead>
<tbody>
{''.join(rows)}
</tbody></table></div>
<p id="empty" class="small" hidden>No festivals match those filters.</p>
<p class="small">“Per day” is the adult ticket divided by the number of days it covers (the festival's published dates, or the days named on the ticket where it covers fewer). It is our calculation, not a festival figure. “—” means we have not found a {ED} figure from a source we trust yet.</p>
{affiliate_slot('sponsor')}
{newsletter()}
<section class="seo-copy"><h2>How much does a UK festival cost in {ED}?</h2>
<p>Among the {len(priced)} festivals where we found a sourced {ED} price, the median cheapest adult full-festival ticket is {money(med)}. The cheapest is {e(lo['name'])} at {money(lo['adult']['value'])} and the dearest is {e(hi['name'])} at {money(hi['adult']['value'])}. Booking fees, parking, campervan passes and refundable litter bonds can add a lot, so each festival page lists them where the festival publishes them.</p>
<p>Use the <a href="calendar.html">on-sale calendar</a> to see which festivals are on sale, sold out or coming soon, and the <a href="calculator.html">budget calculator</a> to add travel, food and drink to the ticket price.</p></section>
<script src="js/table.js"></script>"""
    desc = f"Compare {ED} UK festival ticket prices: cheapest adult ticket, price per day, camping, parking and on-sale status for {len(FESTS)} festivals, with sources."
    (ROOT / "index.html").write_text(page(f"UK Festival Ticket Prices {ED} Compared | {SITE}", desc, "index.html", body))

# ---------- detail pages ----------
ROWS = [("adult", "Cheapest adult full-festival ticket"), ("noncamp", "Adult, no camping"), ("day", "Adult day ticket"),
        ("parking", "Car parking"), ("campervan", "Campervan / live-in vehicle")]
def build_detail(f):
    pd = per_day(f)
    trs = []
    for k, label in ROWS:
        p = f.get(k)
        if p:
            note = " ".join(x for x in (p.get("label", ""), "·" if p.get("note") else "", p.get("note", "")) if x)
            trs.append(f'<tr><th scope="row">{label}</th><td class="big">{money(p["value"])}<span class="sub">{e(FEES[p.get("fees")])}</span></td><td>{e(note)}<div class="src">{src_link(p)}</div></td></tr>')
        else:
            trs.append(f'<tr><th scope="row">{label}</th><td class="big empty">—</td><td class="small">Not found from a source we trust yet.</td></tr>')
    days_txt = str(ndays(f)) + (f" (adult ticket covers {f['adult']['days']})" if f.get("adult") and f["adult"].get("days") and f["adult"]["days"] != ndays(f) else "")
    facts = [("Dates", date_range(f) + (" (camping dates)" if f.get("dates_basis") == "camping" else "")), ("Days", days_txt),
             ("Where", place(f) or "Not confirmed"), ("Nation", f.get("nation") or "—"), ("Region", f.get("region") or "—"), ("Camping", CAMP[f["camping"]]),
             ("Status", STATUS[f["status"]]), ("Per day", money(pd) if pd is not None else "—")]
    if f.get("seller"): facts.append(("Official seller", f["seller"]))
    factshtml = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts)
    extras = [x for x in (f.get("extras") or [])]
    more = ""
    if f.get("kids"): more += f"<p><strong>Children and teens:</strong> {e(f['kids'])}</p>"
    if f.get("deposit"): more += f"<p><strong>Deposits and payment plans:</strong> {e(f['deposit'])}</p>"
    if extras: more += "<ul>" + "".join(f"<li>{e(x)}</li>" for x in extras) + "</ul>"
    if more:
        srcp = f.get("adult") or f.get("dates_src")
        more = f"<h2>Other ticket details</h2>{more}<p class='small'>From the same source as the main price: {src_link(srcp)}</p>"
    srcs = f"<ul class='sources'><li>Dates: {src_link(f['dates_src'])}</li>" + (f"<li>Location: {src_link(f['loc_src'])}</li>" if f.get("loc_src") else "") + "</ul>"
    same = [g for g in FESTS if g["id"] != f["id"] and g.get("region") and g.get("region") == f.get("region")][:6]
    rel = ("<h2>Other festivals in " + e(f["region"]) + "</h2><ul>" + "".join(f'<li><a href="{g["id"]}.html">{e(g["name"])}</a>, {date_range(g)}</li>' for g in same) + "</ul>") if same else ""
    buy = f.get("adult") or f.get("dates_src")
    a = f.get("adult")
    body = f"""<p class="crumbs"><a href="index.html">All festivals</a> › {e(f['name'])}</p>
<h1>{e(f['name'])} {ED} ticket prices</h1>
<p class="lede">{e(f['name'])} {ED} runs {date_range(f)}{(' at ' + e(place(f))) if place(f) else ''}. {('The cheapest adult full-festival ticket we found is ' + money(a['value']) + ' (' + e(a['label']) + ').') if a else 'We have not found a sourced ' + ED + ' adult price yet.'}</p>
<p><span class="status st-{f['status']}">{STATUS[f['status']]}</span> {e(f.get('status_note',''))}</p>
<dl class="facts">{factshtml}</dl>
<h2>Prices</h2>
<div class="table-wrap"><table class="club-table"><tbody>{''.join(trs)}</tbody></table></div>
<p class="small">Buy only from the official seller: <a href="{e(buy['source_url'])}" rel="nofollow noopener" target="_blank">{e(buy['source_title'])}</a>.</p>
{affiliate_slot('tickets', f)}
{more}
<h2>Sources</h2>{srcs}
{affiliate_slot('stay' if f['camping'] in ('none', 'unknown') else 'gear', f)}
{rel}
{newsletter()}
<p class="small">Spotted a wrong or out-of-date price? <a href="about.html#corrections">Send a correction</a>.</p>"""
    desc = (f"{f['name']} {ED} ticket prices: " + (f"from {money(a['value'])}, " if a else "") + f"{date_range(f)}. Camping, parking and on-sale status, with sources.")[:300]
    (ROOT / f"{f['id']}.html").write_text(page(f"{f['name']} {ED} Ticket Prices | {SITE}", desc, f"{f['id']}.html", body))

# ---------- calendar ----------
def build_calendar():
    by = {}
    for f in FESTS: by.setdefault(f["start"][:7], []).append(f)
    parts = []
    for m in sorted(by):
        items = "".join(f'<li><span><a href="{f["id"]}.html"><strong>{e(f["name"])}</strong></a> · {date_range(f)}{(" · " + e(place(f))) if place(f) else ""}</span>'
                        f'<span>{money(f["adult"]["value"]) if f.get("adult") else "—"} <span class="status st-{f["status"]}">{STATUS[f["status"]]}</span></span></li>' for f in by[m])
        parts.append(f'<section class="month"><h2>{datetime.date.fromisoformat(m + "-01").strftime("%B %Y")}</h2><ul>{items}</ul></section>')
    soon = [f for f in FESTS if f["status"] == "coming_soon"]
    soonhtml = "".join(f"<li><a href='{f['id']}.html'>{e(f['name'])}</a>: {e(f.get('status_note',''))}</li>" for f in soon)
    body = f"""<h1>UK festival {ED} on-sale calendar</h1>
<p class="lede">Every festival we track, month by month, with its cheapest adult ticket and whether tickets are on sale, sold out or coming soon.</p>
{('<h2>Going on sale soon</h2><ul>' + soonhtml + '</ul>') if soon else ''}
{''.join(parts)}
{newsletter()}"""
    (ROOT / "calendar.html").write_text(page(f"UK Festival {ED} Calendar and On-Sale Dates | {SITE}",
        f"UK festivals {ED} by month: dates, cheapest adult ticket and on-sale status for {len(FESTS)} festivals.", "calendar.html", body))

# ---------- calculator ----------
def build_calculator():
    opts = []
    for f in FESTS:
        a = f.get("adult")
        if not a: continue
        opts.append({"id": f["id"], "name": f["name"], "days": ticket_days(f), "ticket": a["value"], "fees": a.get("fees"),
                     "parking": (f.get("parking") or {}).get("value"), "campervan": (f.get("campervan") or {}).get("value")})
    body = f"""<h1>Festival budget calculator</h1>
<p class="lede">Pick a festival to fill in the ticket and parking prices we have sourced, then add your own travel, food and drink to see the full cost per person.</p>
<form class="calc" id="calc" onsubmit="return false">
<div class="field full"><label for="fest">Festival</label><select id="fest"></select></div>
<div class="field"><label for="people">People in your group</label><input type="number" id="people" min="1" value="2"></div>
<div class="field"><label for="ticket">Ticket each (£)</label><input type="number" id="ticket" min="0" step="0.01"></div>
<div class="field"><label for="fee">Booking fee each (£) <span class="opt">if not included</span></label><input type="number" id="fee" min="0" step="0.01" value="0"></div>
<div class="field"><label for="parking">Parking for the group (£)</label><input type="number" id="parking" min="0" step="0.01" value="0"></div>
<div class="field"><label for="travel">Travel each (£) <span class="opt">train, coach, fuel</span></label><input type="number" id="travel" min="0" step="0.01" value="0"></div>
<div class="field"><label for="food">Food and drink each per day (£)</label><input type="number" id="food" min="0" step="0.01" value="0"></div>
<div class="field"><label for="days">Days</label><input type="number" id="days" min="1" value="3"></div>
<div class="field"><label for="other">Other each (£) <span class="opt">tent, kit, extras</span></label><input type="number" id="other" min="0" step="0.01" value="0"></div>
</form>
<div class="result" aria-live="polite"><p class="total-label">Cost per person</p><p class="total" id="total">£0</p><ul id="breakdown"></ul><p class="small" id="feenote"></p></div>
<p class="small">The festival prices come from our sourced data. Your travel, food and drink figures are your own estimates, and we do not supply any. Nothing you type is sent anywhere.</p>
{affiliate_slot('gear')}
{newsletter()}
<script>window.FESTS={json.dumps(opts)};</script>
<script src="js/calculator.js"></script>"""
    (ROOT / "calculator.html").write_text(page(f"Festival Budget Calculator {ED} | {SITE}",
        "Work out the real cost of a UK festival per person: sourced ticket and parking prices plus your own travel, food and drink.", "calculator.html", body))

# ---------- about ----------
def build_about():
    defs = "".join(f"<li><strong>{e(k)}</strong>: {e(v)}</li>" for k, v in META["definitions"].items())
    st = "".join(f"<li><strong>{e(STYPE[k])}</strong>: {e(v)}</li>" for k, v in META["source_types"].items())
    body = f"""<h1>About and methodology</h1>
<p class="lede">{SITE} is a free, independent comparison of UK festival ticket prices. It is part of <a href="{POF_URL}">Price of Football</a>, which tracks what it costs to watch football in the UK.</p>
<h2>How prices are collected</h2>
<p>Each figure is read by hand from the festival's own website, its official ticket page or an official ticket agent. Where only the press has published a price, we label it “Press”. Every figure shows its source link and the date we checked it. If we cannot find a {ED} price from a source we trust, we show “—”. We never estimate, carry over last year's price or fill gaps with averages.</p>
<h2>Definitions</h2><ul>{defs}</ul>
<h2>Source types</h2><ul>{st}</ul>
<h2>Known limits</h2>
<ul><li>Festivals sell in tiers, so the cheapest tier may already have gone up or sold out by the time you read this.</li>
<li>Ticket agents add booking fees in different ways. We record whether the shown price includes them (“incl. booking fee”), says they are extra (“+ booking fee”) or does not say (“fees not stated”).</li>
<li>Some festivals show prices only inside a booking widget we could not read. These are listed with a blank price until we can confirm one.</li></ul>
<h2 id="corrections">Corrections</h2>
<p>Spotted a wrong, missing or out-of-date price? Email <strong>{e(CORRECTIONS)}</strong> <!-- TODO: replace placeholder address --> with the festival, the correct figure and a link to where it is published. We fix sourced corrections quickly.</p>
<h2>How the site is funded</h2>
<p>The site is free. It may in future carry clearly labelled sponsor slots, or affiliate links to official ticket agents and camping retailers, which would pay us a small commission at no extra cost to you. Affiliate links will never change which festivals appear or how they are ranked. <!-- TODO: add affiliate disclosure wording once any programme is approved --></p>
<h2>Data</h2>
<p>The full dataset is free to download as <a href="data/festivals.json">JSON</a> or <a href="data/festivals.csv">CSV</a>.</p>
{newsletter()}"""
    (ROOT / "about.html").write_text(page(f"About and Methodology | {SITE}", "How Price of Festivals collects and checks UK festival ticket prices, and how to send a correction.", "about.html", body))

def build_csv():
    with open(ROOT / "data" / "festivals.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "name", "start", "end", "venue", "county", "nation", "region", "camping", "status", "adult_price", "adult_label", "adult_fees", "adult_source_url", "adult_checked",
                    "adult_ticket_days", "noncamp_price", "day_price", "parking_price", "campervan_price", "per_day_calc", "dates_source_url"])
        for f in FESTS:
            g = lambda k: (f.get(k) or {}).get("value")
            a = f.get("adult") or {}
            w.writerow([f["id"], f["name"], f["start"], f["end"], f.get("venue", ""), f.get("county", ""), f.get("nation", ""), f.get("region", ""), f["camping"], f["status"],
                        a.get("value", ""), a.get("label", ""), a.get("fees", ""), a.get("source_url", ""), a.get("checked", ""), a.get("days", ""),
                        g("noncamp") if g("noncamp") is not None else "", g("day") if g("day") is not None else "", g("parking") if g("parking") is not None else "",
                        g("campervan") if g("campervan") is not None else "", per_day(f) or "", f["dates_src"]["source_url"]])

def build_seo():
    urls = ["index.html", "calendar.html", "calculator.html", "about.html"] + [f"{f['id']}.html" for f in FESTS]
    today = META["generated"]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"<url><loc>{SITE_URL}/{'' if u == 'index.html' else u}</loc><lastmod>{today}</lastmod></url>" for u in urls]
    xml.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(xml) + "\n")
    # No robots.txt here: robots.txt only works at the domain root, which this folder is not.

if __name__ == "__main__":
    reserved = {"index", "calendar", "calculator", "about"}
    assert not reserved & {f["id"] for f in FESTS}, "festival id clashes with a site page"
    build_index(); build_calendar(); build_calculator(); build_about()
    for f in FESTS: build_detail(f)
    build_csv(); build_seo()
    print(f"Built {len(FESTS)} festival pages + 4 site pages.")
