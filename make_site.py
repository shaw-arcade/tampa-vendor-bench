"""Generate site/index.html from the same data that builds the workbook."""
import html, os, runpy

HERE = os.path.dirname(os.path.abspath(__file__))
ns = runpy.run_path(os.path.join(HERE, "build.py"))
triage, sourcing, checks, notes, SAMPLE = ns["triage"], ns["sourcing"], ns["checks"], ns["notes"], ns.get("SAMPLE", [])
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


def sample_rows():
    out = []
    for v in SAMPLE:
        lic = v.get("license","") or "n/a"
        ver = v.get("license_verified","")
        licstr = f"{e(lic)}" + (f"<br><small>verified {e(ver)}</small>" if ver else "")
        rev = v.get("reviews","")
        name = e(v.get("company","") or v.get("name",""))
        web = v.get("web","")
        if web: name = f"<a href='{e(web)}' target='_blank' rel='noopener'>{name}</a>"
        out.append(f"<tr><td><span class='pill'>{e(v.get('trade',''))}</span></td><td class='issue'>{name}<br><small>{e(v.get('phone',''))}</small></td>"
                   f"<td>{licstr}</td><td>{e(v.get('wc',''))}</td><td class='cost'>{e(v.get('rate',''))}<br><small>{e(v.get('trip',''))}</small></td><td>{e(rev)}</td><td class='before'>{e(v.get('notes',''))}</td></tr>")
    return "\n".join(out)

QUESTIONS = [
 "Where are the houses? A list of cities or ZIP codes is enough. An address list is better, because it lets me group houses so one plumber covers a whole cluster.",
 "Which repairs cost you the most or happen the most? AC, plumbing, electrical, roof, handyman work, pest, lawn, turnover cleaning.",
 "Can you send a few recent repair invoices, or last year's total repair spend? Three or four bills is enough to show what you paid versus what the vetted people charge.",
 "Do you want real quotes, or just the vetted list? Quotes mean the vendors get contacted on your behalf. If yes, which email should they reply to?",
 "Any vendors you already like and want to keep? Any you never want to see again?",
 "Anything I should know about specific houses? Very old plumbing or wiring, a roof near the end of its life, a house that always has problems.",
]
def question_items():
    return "\n".join(f"<li>{e(q)}</li>" for q in QUESTIONS)

def note_items():
    return "\n".join(f"<li>{e(n)}</li>" for n in notes)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tampa Vendor Bench</title>
<meta name="description" content="A landlord's system for reliable, fairly priced trades in Tampa: bench, triage guide, sourcing channels, vetting checklist, and the workbook that runs it.">
<meta property="og:title" content="Tampa Vendor Bench">
<meta property="og:description" content="Reliable trades at fair prices for Tampa rentals. Triage guide, sourcing channels, vetting checklist, and the workbook.">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}">
<style>
body{{margin:0;background:#fff;color:#000;font:14px/1.6 Arial,Helvetica,sans-serif}}
.wrap{{max-width:816px;margin:0 auto;padding:0 24px}}
header{{padding:40px 0 8px}}
header .wrap{{padding-top:0}}
h1{{font-size:26px;font-weight:bold;margin:0 0 8px}}
h2{{font-size:18px;font-weight:bold;margin:0 0 8px}}
h3{{font-size:14px;font-weight:bold;margin:0 0 4px}}
a{{color:#1155cc}}
.btn{{display:inline-block;margin:0 14px 0 0}}
.mark{{display:none}}
header p{{margin:0 0 12px}}
nav{{padding:8px 0 16px}}
nav .wrap{{display:block}}
nav a{{display:block;margin:2px 0}}
section{{padding:20px 0;border-top:1px solid #ddd}}
.lede{{margin:0 0 12px;color:#333}}
.answer{{margin:0 0 12px}}
ul.rules{{padding-left:22px}} ul.rules li{{margin:0 0 8px}}
.tablewrap{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border:1px solid #bbb;padding:6px 8px;text-align:left;vertical-align:top}}
th{{background:#f3f3f3;font-weight:bold}}
td.issue{{font-weight:bold}}
td.lic.yes,td.lic.no,td.lic.grey{{color:#000}}
.pill{{white-space:nowrap}}
.cards{{display:block}}
.card{{display:flex;gap:10px;margin:0 0 12px}}
.card .rank{{flex:0 0 22px;font-weight:bold}}
.card p{{margin:0 0 4px}}
.card .how{{color:#333}} .card .cost{{color:#555;font-size:12px}}
ol.checks{{padding-left:22px}} ol.checks li{{margin:0 0 10px}}
ol.checks strong{{display:block}} ol.checks .where,ol.checks .rule{{display:block}}
ol.checks .rule{{color:#333}}
ul.notes{{padding-left:22px}} ul.notes li{{margin:0 0 8px}}
.rates td:first-child{{font-weight:bold}}
footer{{padding:20px 0 40px;color:#555;font-size:12px;border-top:1px solid #ddd}}
small{{color:#555}}
</style>
</head>
<body>
<header><div class="wrap">
<h1>Tampa Vendor Bench</h1>
<p>A landlord's system for keeping reliable, fairly priced plumbers, electricians and handymen on call in Tampa. The workbook runs it. This page explains it.</p>
<p><a class="btn" href="Tampa-Vendor-Bench.xlsx" download>Download the workbook (.xlsx)</a></p>
</div></header>
<nav><div class="wrap"><strong>Contents</strong><a href="#answer">The short answer</a><a href="#rules">Bench rules</a><a href="#triage">Triage guide</a><a href="#sourcing">Where to find people</a><a href="#vetting">Vetting</a><a href="#tampa">Tampa notes</a><a href="#sample">Sample bench</a><a href="#cost">Cost to hand off</a><a href="#questions">Questions for the owner</a><a href="#workbook">The workbook</a></div></nav>

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

<section id="sample"><div class="wrap">
<h2>Sample bench: Tampa</h2>
<p class="lede">What one region looks like once it is done. Every name below was found through the channels above, then checked against the Florida license database and public reviews. Nobody was contacted. This is the vetted list, not quotes. Rates shown are what each shop publishes. Send the list of cities and this gets built for every area.</p>
<div class="tablewrap"><table style="min-width:1000px">
<thead><tr><th>Trade</th><th>Shop</th><th>FL license</th><th>Workers comp</th><th>Published rate</th><th>Reviews</th><th>Notes</th></tr></thead>
<tbody>{sample_rows()}</tbody>
</table></div>
<p class="lede" style="margin-top:12px;font-size:13px">License status and expiry from the Florida DBPR licensee search on the date shown. Workers comp from the Florida DWC proof-of-coverage database where checked. Ratings from Google at time of research. Confirm insurance with a certificate before the first job.</p>
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

<section id="questions"><div class="wrap">
<h2>Questions for the owner</h2>
<p class="lede">Short answers are fine. With these, the sample above gets built for every area.</p>
<ol class="checks">{question_items()}</ol>
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
<p><a href="Tampa-Vendor-Bench.xlsx" download>Download the workbook (.xlsx)</a></p>
</div></section>

<footer><div class="wrap">Built September 2026. Local facts from <a href="https://hcfl.gov/businesses/hillsgovhub/contractor-licensing" target="_blank" rel="noopener">Hillsborough County contractor licensing</a>, <a href="https://www.bellafsm.com/handyman-requirements-in-florida/" target="_blank" rel="noopener">Florida handyman rules</a>, <a href="https://tampareia.com/" target="_blank" rel="noopener">Tampa REIA</a>, <a href="https://lula.life/services" target="_blank" rel="noopener">Lula</a>, <a href="https://www.homeyou.com/fl/handyman-tampa-costs" target="_blank" rel="noopener">Homeyou Tampa</a>, <a href="https://homeguide.com/costs/plumber-cost" target="_blank" rel="noopener">HomeGuide</a>. Not legal advice. Verify every license yourself.</div></footer>
</body>
</html>
"""
out = os.path.join(HERE, "docs", "index.html")
open(out, "w").write(page)
print("wrote", out, len(page), "bytes")
