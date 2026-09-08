"""Generate site/index.html from the same data that builds the workbook."""
import html, os, runpy

HERE = os.path.dirname(os.path.abspath(__file__))
ns = runpy.run_path(os.path.join(HERE, "build.py"))
triage, sourcing, checks, notes = ns["triage"], ns["sourcing"], ns["checks"], ns["notes"]
e = html.escape

SITE_URL = "https://shaw-arcade.github.io/tampa-vendor-bench/"

def triage_rows():
    out = []
    for issue, trade, lic, urg, cost, before in triage:
        cls = "yes" if lic.startswith("Yes") else ("no" if lic.startswith("No") else "grey")
        out.append(f"<tr><td class='issue'>{e(issue)}</td><td><span class='pill'>{e(trade)}</span></td>"
                   f"<td class='lic {cls}'>{e(lic)}</td><td>{e(urg)}</td><td class='cost'>{e(cost)}</td><td class='before'>{e(before)}</td></tr>")
    return "\n".join(out)

def sourcing_cards():
    out = []
    for rank, ch, best, cost, link, how in sourcing:
        title = f"<a href='{e(link)}' target='_blank' rel='noopener'>{e(ch)}</a>" if link else e(ch)
        out.append(f"<div class='card'><div class='rank'>{rank}</div><div class='body'><h3>{title}</h3>"
                   f"<p class='best'>{e(best)}</p><p class='how'>{e(how)}</p><p class='cost'>{e(cost)}</p></div></div>")
    return "\n".join(out)

def check_items():
    out = []
    for step, check, where, link, rule in checks:
        w = f"<a href='{e(link)}' target='_blank' rel='noopener'>{e(where)}</a>" if link else e(where)
        out.append(f"<li><strong>{e(check)}</strong><span class='where'>{w}</span><span class='rule'>{e(rule)}</span></li>")
    return "\n".join(out)

def note_items():
    return "\n".join(f"<li>{e(n)}</li>" for n in notes)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tampa Vendor Bench</title>
<meta name="description" content="A landlord's system for reliable, fairly priced trades in Tampa: bench, triage guide, sourcing channels, vetting checklist, and the workbook that runs it.">
<link rel="icon" type="image/png" sizes="32x32" href="brand/favicon-32.png">
<link rel="icon" type="image/png" sizes="64x64" href="brand/favicon-64.png">
<link rel="apple-touch-icon" href="brand/apple-touch-icon.png">
<meta property="og:title" content="Tampa Vendor Bench">
<meta property="og:description" content="Reliable trades at fair prices for Tampa rentals. Triage guide, sourcing channels, vetting checklist, and the workbook.">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}brand/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<style>
:root{{--ink:#26241f;--gold:#b49a5a;--ivory:#f7f4ee;--paper:#fffdf9;--mute:#6b665c;--line:#e6e0d3;--red:#b3402e;--green:#3d6b3f}}
*{{box-sizing:border-box}}
body{{margin:0;font:16px/1.55 Georgia,'Times New Roman',serif;color:var(--ink);background:var(--ivory)}}
a{{color:var(--ink);text-decoration:underline;text-decoration-color:var(--gold);text-underline-offset:3px}}
header{{background:var(--ink);color:var(--ivory);padding:56px 20px 44px}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 20px}}
.mark{{display:inline-block;width:44px;height:44px;border:1.5px solid var(--gold);color:var(--gold);text-align:center;line-height:42px;font-size:26px;margin-bottom:18px}}
h1{{font-size:clamp(30px,5vw,46px);margin:0 0 10px;font-weight:normal;letter-spacing:.5px}}
header p{{max-width:640px;margin:0 0 22px;color:#d8d2c4;font-size:18px}}
.btn{{display:inline-block;background:var(--gold);color:var(--ink);padding:12px 22px;text-decoration:none;font-weight:bold;letter-spacing:.3px;border-radius:2px}}
.btn.ghost{{background:transparent;color:var(--gold);border:1px solid var(--gold);margin-left:8px}}
nav{{background:var(--paper);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}}
nav .wrap{{display:flex;gap:18px;overflow-x:auto;padding:12px 20px;font-size:14px;white-space:nowrap}}
nav a{{text-decoration:none;color:var(--mute)}} nav a:hover{{color:var(--ink)}}
section{{padding:44px 0;border-bottom:1px solid var(--line)}}
h2{{font-size:26px;font-weight:normal;margin:0 0 6px}}
.lede{{color:var(--mute);margin:0 0 22px;max-width:700px}}
.answer{{background:var(--paper);border-left:4px solid var(--gold);padding:18px 22px;margin:0 0 18px;font-size:17px}}
ul.rules{{padding-left:20px}} ul.rules li{{margin:0 0 10px}}
.tablewrap{{overflow-x:auto;border:1px solid var(--line);background:var(--paper)}}
table{{border-collapse:collapse;width:100%;min-width:900px;font-size:14px}}
th{{background:var(--ink);color:var(--ivory);text-align:left;padding:10px 12px;font-weight:normal;letter-spacing:.3px}}
td{{padding:10px 12px;border-top:1px solid var(--line);vertical-align:top}}
td.issue{{font-weight:bold;min-width:180px}} td.cost{{white-space:nowrap}} td.before{{color:var(--mute);min-width:260px}}
td.lic.yes{{color:var(--red)}} td.lic.no{{color:var(--green)}} td.lic.grey{{color:var(--mute)}}
.pill{{display:inline-block;border:1px solid var(--gold);padding:2px 8px;border-radius:12px;font-size:13px;white-space:nowrap}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}}
.card{{display:flex;gap:14px;background:var(--paper);border:1px solid var(--line);padding:16px}}
.card .rank{{flex:0 0 34px;height:34px;border:1.5px solid var(--gold);color:var(--gold);text-align:center;line-height:32px;font-size:16px}}
.card h3{{margin:0 0 6px;font-size:16px;font-weight:bold}} .card p{{margin:0 0 6px;font-size:14px}}
.card .best{{color:var(--ink)}} .card .how{{color:var(--mute)}} .card .cost{{font-size:12px;color:var(--gold)}}
ol.checks{{padding-left:22px}} ol.checks li{{margin:0 0 14px;background:var(--paper);border:1px solid var(--line);padding:12px 14px 12px 8px;list-style-position:inside}}
ol.checks strong{{display:block}} ol.checks .where{{display:block;font-size:14px;margin:4px 0}} ol.checks .rule{{display:block;font-size:14px;color:var(--mute)}}
ul.notes{{padding-left:20px}} ul.notes li{{margin:0 0 10px}}
.rates td:first-child{{font-weight:bold}}
footer{{padding:30px 0 50px;color:var(--mute);font-size:13px}}
footer a{{color:var(--mute)}}
@media (max-width:600px){{header{{padding:40px 0 32px}} .btn.ghost{{margin:10px 0 0}}}}
</style>
</head>
<body>
<header><div class="wrap">
<div class="mark">T</div>
<h1>Tampa Vendor Bench</h1>
<p>A landlord's system for keeping reliable, fairly priced plumbers, electricians and handymen on call in Tampa. The workbook runs it. This page explains it.</p>
<a class="btn" href="Tampa-Vendor-Bench.xlsx" download>Download the workbook (.xlsx)</a><a class="btn ghost" href="#triage">Jump to the triage guide</a>
</div></header>
<nav><div class="wrap"><a href="#answer">The short answer</a><a href="#rules">Bench rules</a><a href="#triage">Triage guide</a><a href="#sourcing">Where to find people</a><a href="#vetting">Vetting</a><a href="#tampa">Tampa notes</a><a href="#cost">Cost to hand off</a><a href="#workbook">The workbook</a></div></nav>

<section id="answer"><div class="wrap">
<h2>Are you overthinking it?</h2>
<p class="answer">Mostly, yes. What you want is a vendor bench: two or three vetted people per trade, a rule for which one to call, and a log that tells you who is actually cheap and reliable. Property managers have run this on a spreadsheet for decades. Software is not the hard part. Finding and filtering the people is.</p>
<p>The cheapest quote is rarely the win. Facebook and word of mouth produce lower rates, but in Florida the low rate often means no license or insurance. Anything over a thousand dollars total, or touching plumbing, electrical, HVAC, roofing or pest control, legally needs a licensed trade. An uninsured worker hurt on your property becomes your problem. The savings that stick come from repeat-business rates, triage before dispatch, and never paying emergency pricing out of desperation.</p>
</div></section>

<section id="rules"><div class="wrap">
<h2>Bench rules that keep prices low</h2>
<ul class="rules">
<li><strong>Two or three per trade.</strong> One primary, one backup. A vendor who knows he is your default gets every small job and prices them lower.</li>
<li><strong>Handyman first.</strong> Route every small job through the handyman. Escalate to a licensed plumber or electrician only when the triage guide says the law requires it.</li>
<li><strong>Not-To-Exceed on every call.</strong> Name the number when you dispatch. Anything above it needs a call back before work continues.</li>
<li><strong>Batch the cosmetic stuff.</strong> One handyman visit per property per month, not one visit per drywall hole.</li>
<li><strong>Insurance expiry is a hard stop.</strong> The bench turns red 30 days out. Ask for a new certificate before the next job.</li>
<li><strong>Spring is for roofs and AC.</strong> Tampa trades are booked solid June through October and prices rise with demand.</li>
<li><strong>One trial job before a key.</strong> Showed up on time, sent a photo when done, invoice matched the quote. Pass all three or they are off the bench.</li>
</ul>
</div></section>

<section id="triage"><div class="wrap">
<h2>Triage guide</h2>
<p class="lede">Find the complaint, send the right trade, know whether the law requires a license, and know what a fair Tampa price looks like before you get the quote.</p>
<div class="tablewrap"><table>
<thead><tr><th>Tenant reports</th><th>Send first</th><th>FL license required?</th><th>Urgency</th><th>Typical Tampa cost (2026)</th><th>Before you dispatch</th></tr></thead>
<tbody>{triage_rows()}</tbody>
</table></div>
<p class="lede" style="margin-top:12px;font-size:13px">Cost ranges are published 2026 Tampa and national figures (HomeGuide, Angi, Homeyou), not quotes. Your own job log replaces them within a few months. License rules are Florida Statute 489.</p>
</div></section>

<section id="sourcing"><div class="wrap">
<h2>Where to find people</h2>
<p class="lede">Ranked by how well the channel filters for quality. Investor referrals beat homeowner referrals, and both beat a cold platform search. Facebook is the best channel for the sub-$1,000 handyman tier and the worst for licensed trades.</p>
<div class="cards">{sourcing_cards()}</div>
</div></section>

<section id="vetting"><div class="wrap">
<h2>Vetting checklist</h2>
<p class="lede">Eight checks before anyone gets a key. Every lookup is free and takes about a minute.</p>
<ol class="checks">{check_items()}</ol>
</div></section>

<section id="tampa"><div class="wrap">
<h2>Tampa notes</h2>
<ul class="notes">{note_items()}</ul>
</div></section>

<section id="cost"><div class="wrap">
<h2>What it costs to hand this off</h2>
<p class="lede">Running the bench is a few hours a week for a handful of doors, more at turnover. Here is what each level of help costs in 2026.</p>
<div class="tablewrap"><table class="rates" style="min-width:700px">
<thead><tr><th>Option</th><th>Rate</th><th>What you get</th><th>What stays on you</th></tr></thead>
<tbody>
<tr><td>You plus the workbook</td><td>Your time</td><td>Full control, lowest cost, the log builds your own price benchmarks</td><td>Everything: calls, sourcing, vetting, dispatch, follow-up</td></tr>
<tr><td>Offshore VA (Philippines)</td><td>$8 to $13 per hour</td><td>Tenant intake, vendor calls and texts, license lookups, scheduling, log upkeep</td><td>Approvals over your NTE, payment, anything on site</td></tr>
<tr><td>US-based VA</td><td>$18 to $28 per hour</td><td>Same as above with US hours and easier phone rapport with local trades</td><td>Same as above</td></tr>
<tr><td>Latchel or Lula</td><td>About $25 per unit per month (Latchel); Lula is per job plus fee</td><td>24/7 tenant line, triage, vetted vendor dispatch, invoice handling</td><td>Approvals over NTE, paying the invoice, deciding when to replace instead of repair</td></tr>
<tr><td>Full property manager</td><td>8 to 10 percent of rent, plus 10 percent maintenance markup and leasing fees</td><td>Everything, including tenants and rent</td><td>Reviewing their markups. Their vendors are rarely the cheapest.</td></tr>
</tbody></table></div>
<p style="font-size:14px;color:var(--mute)">Sources: <a href="https://shoreagents.com/resources/property-maintenance-coordinator-va" target="_blank" rel="noopener">ShoreAgents</a>, <a href="https://www.ziprecruiter.com/Salaries/Virtual-Assistant-Philippines-Salary" target="_blank" rel="noopener">ZipRecruiter</a>, <a href="https://sfailabs.com/guides/best-ai-maintenance-triage-tools-small-property-managers" target="_blank" rel="noopener">SFAI Labs on Latchel pricing</a>.</p>
</div></section>

<section id="workbook"><div class="wrap">
<h2>The workbook</h2>
<p class="lede">Six tabs. Drag it into Google Drive and it opens as a Sheet with the dropdowns and formulas intact.</p>
<ul class="rules">
<li><strong>Start Here.</strong> How to use it and the bench rules above.</li>
<li><strong>Properties.</strong> One row per house, feeds the Job Log dropdown.</li>
<li><strong>Vendor Bench.</strong> Name, trade, license, insurance expiry, workers comp, rate, trip charge. Insurance cells turn red 30 days out. Jobs done, total paid, average rating and last used fill themselves from the Job Log.</li>
<li><strong>Job Log.</strong> One row per job with property and vendor dropdowns, quote versus paid, a 1 to 5 rating, and a 90-day spend summary.</li>
<li><strong>Triage Guide, Tampa Sourcing, Vetting Checklist.</strong> The three tables on this page, with links.</li>
</ul>
<a class="btn" href="Tampa-Vendor-Bench.xlsx" download>Download the workbook (.xlsx)</a>
</div></section>

<footer><div class="wrap">Built September 2026. Local facts from <a href="https://hcfl.gov/businesses/hillsgovhub/contractor-licensing" target="_blank" rel="noopener">Hillsborough County contractor licensing</a>, <a href="https://www.bellafsm.com/handyman-requirements-in-florida/" target="_blank" rel="noopener">Florida handyman rules</a>, <a href="https://tampareia.com/" target="_blank" rel="noopener">Tampa REIA</a>, <a href="https://lula.life/services" target="_blank" rel="noopener">Lula</a>, <a href="https://www.homeyou.com/fl/handyman-tampa-costs" target="_blank" rel="noopener">Homeyou Tampa</a>, <a href="https://homeguide.com/costs/plumber-cost" target="_blank" rel="noopener">HomeGuide</a>. Not legal advice. Verify every license yourself.</div></footer>
</body>
</html>
"""
out = os.path.join(HERE, "docs", "index.html")
open(out, "w").write(page)
print("wrote", out, len(page), "bytes")
