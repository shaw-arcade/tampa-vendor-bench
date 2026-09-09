"""Generate docs/index.html: a plain, owner-facing page built from sample_bench.json."""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = json.load(open(os.path.join(HERE, "sample_bench.json")))
e = html.escape

TRADES = ["Handyman", "Plumber", "Electrician", "HVAC"]
TRADE_NOTE = {
    "Handyman": "Small repairs under $1,000: drywall, paint, doors, fixtures, fences, faucet and toilet parts. Florida does not license handymen, so the check here is insurance and reviews.",
    "Plumber": "Leaks, drains, water heaters. Florida requires a licensed plumbing contractor for this work.",
    "Electrician": "Outlets, breakers, panels, troubleshooting. Florida requires a licensed electrical contractor.",
    "HVAC": "AC repair, tune-ups, replacement. Florida requires a licensed air conditioning or mechanical contractor.",
}

QUESTIONS = [
    "Where are the houses? A list of cities or ZIP codes is enough. An address list is better, because it lets me group houses so one plumber covers a whole cluster.",
    "Which repairs cost you the most or happen the most? AC, plumbing, electrical, roof, handyman work, pest, lawn, turnover cleaning.",
    "Can you send a few recent repair invoices, or last year's total repair spend? Three or four bills is enough to show what you paid versus what these people charge.",
    "Do you want real quotes, or just the vetted list? Quotes mean the vendors get contacted on your behalf. If yes, which email should they reply to?",
    "Any vendors you already like and want to keep? Any you never want to see again?",
    "Anything I should know about specific houses? Very old plumbing or wiring, a roof near the end of its life, a house that always has problems.",
]

def trade_table(trade):
    out = []
    for v in [v for v in SAMPLE if v["trade"] == trade]:
        pick = v.get("role", "")
        is_ref = pick.startswith("Reference")
        name = e(v["company"])
        if v.get("web"):
            name = f"<a href='{e(v['web'])}' target='_blank' rel='noopener'>{name}</a>"
        if pick.startswith("Primary"):
            name = f"<strong>{name}</strong>"
        lic = v.get("license", "") or ""
        ver = v.get("license_verified", "")
        if lic.startswith("n/a"):
            licstr = "Not required (handyman)"
        elif ver.startswith("2026"):
            licstr = f"{e(lic)}<br><small>Active, expires 8/31/2028</small>"
        else:
            licstr = e(lic)
        role = "Price reference only" if is_ref else e(pick)
        out.append(
            f"<tr><td>{name}<br><small>{e(v.get('phone',''))}</small></td>"
            f"<td>{role}</td><td>{licstr}</td>"
            f"<td>{e(v.get('rate',''))}</td>"
            f"<td>{e(v.get('reviews',''))}</td>"
            f"<td>{e(v.get('notes',''))}</td></tr>"
        )
    return "\n".join(out)

def trade_sections():
    parts = []
    for t in TRADES:
        parts.append(f"""
<h3>{e(t)}</h3>
<p>{e(TRADE_NOTE[t])}</p>
<div class="tablewrap"><table>
<thead><tr><th>Shop</th><th>Role</th><th>Florida license</th><th>Published pricing</th><th>Reviews</th><th>Notes</th></tr></thead>
<tbody>{trade_table(t)}</tbody>
</table></div>""")
    return "\n".join(parts)

def question_items():
    return "\n".join(f"<li>{e(q)}</li>" for q in QUESTIONS)

n_total = len(SAMPLE)
n_lic = sum(1 for v in SAMPLE if v.get("license_verified", "").startswith("2026"))

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tampa Vendor Bench</title>
<meta name="description" content="Vetted, fairly priced repair vendors for Florida rental houses. Tampa sample.">
<style>
body{{margin:0;background:#fff;color:#000;font:14px/1.6 Arial,Helvetica,sans-serif}}
.wrap{{max-width:900px;margin:0 auto;padding:32px 24px 48px}}
h1{{font-size:24px;margin:0 0 12px}}
h2{{font-size:18px;margin:28px 0 8px;padding-top:16px;border-top:1px solid #ddd}}
h3{{font-size:15px;margin:20px 0 4px}}
p{{margin:0 0 10px}}
a{{color:#1155cc}}
ul,ol{{padding-left:22px}} li{{margin:0 0 8px}}
.tablewrap{{overflow-x:auto;margin:6px 0 12px}}
table{{border-collapse:collapse;width:100%;min-width:820px;font-size:13px}}
th,td{{border:1px solid #bbb;padding:6px 8px;text-align:left;vertical-align:top}}
th{{background:#f3f3f3}}
small{{color:#555}}
.muted{{color:#555;font-size:12px}}
</style>
</head>
<body><div class="wrap">

<h1>Repair vendors for your Florida houses</h1>
<p>This is a list of repair people who have been checked and are priced fairly, built for one area first so you can see what it looks like. Tampa was used as the sample. Once you send the list of cities where your houses are, the same list gets built for every area.</p>
<p><strong>{n_total} vendors below. {n_lic} hold a Florida trade license, and every one of those was checked against the state license database on September 9, 2026 and came back active.</strong> Nobody has been contacted. These are not quotes yet.</p>

<h2>How to read the list</h2>
<ul>
<li><strong>Bold</strong> is the recommended first call for that trade.</li>
<li>"Backup" is who to call when the first one is booked. "Candidate" passed the checks but has a thinner track record or a smaller service area.</li>
<li>"Price reference only" is the big franchise or large shop, included so you can see what the expensive option charges. Not recommended.</li>
<li>Pricing is what each shop publishes on its own site. Real quotes come after you say which houses.</li>
</ul>

<h2>Tampa sample</h2>
{trade_sections()}

<h2>What was checked on every name</h2>
<ul>
<li>Florida state license lookup for every plumber, electrician and AC company. All active through August 2028.</li>
<li>Florida workers comp database for the handymen. None of the four has a policy or exemption on file under their business name, which is common for small crews. Ask each for proof before the first job.</li>
<li>Google, Yelp, Angi and Better Business Bureau reviews.</li>
<li>Years in business and whether they work with landlords or property managers.</li>
</ul>
<p class="muted">Still to do before anyone gets a key: a certificate of insurance from each shop, and one small trial job.</p>

<h2>What I need from you</h2>
<p>Short answers are fine. Number 1 is the only one that blocks the rest.</p>
<ol>
{question_items()}
</ol>

<h2>The workbook</h2>
<p>The same vendors in a spreadsheet, plus a job log and a guide for which trade to send for which problem. <a href="Tampa-Vendor-Bench.xlsx" download>Download the workbook (.xlsx)</a>. It opens in Excel or Google Sheets.</p>

<p class="muted">Built September 2026. License status from the Florida DBPR licensee search. Not legal advice.</p>
</div></body>
</html>
"""
out = os.path.join(HERE, "docs", "index.html")
open(out, "w").write(page)
print("wrote", out, len(page), "bytes")
