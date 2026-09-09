from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

import os

# ---------------- Sample bench data (filled by research, see sample_bench.json) ----------------
import json as _json
_sb = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_bench.json")
SAMPLE = _json.load(open(_sb)) if os.path.exists(_sb) else []

wb = Workbook()
F = "Arial"
HDR_FILL = PatternFill("solid", fgColor="1F3A5F")
HDR_FONT = Font(name=F, bold=True, color="FFFFFF", size=10)
BODY = Font(name=F, size=10)
BOLD = Font(name=F, size=10, bold=True)
TITLE = Font(name=F, size=14, bold=True)
NOTE = Font(name=F, size=9, italic=True, color="555555")
INPUT_FILL = PatternFill("solid", fgColor="FFF9C4")
EX_FILL = PatternFill("solid", fgColor="EEEEEE")
thin = Side(style="thin", color="BBBBBB")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
LINK = Font(name=F, size=10, color="0563C1", underline="single")

def header(ws, row, headers, widths=None):
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = HDR_FONT; c.fill = HDR_FILL; c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical="center")
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 30

def body(ws, row, values, fill=None, wrap=True):
    for i, v in enumerate(values, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = BODY; c.border = BORDER
        c.alignment = Alignment(wrap_text=wrap, vertical="top")
        if fill: c.fill = fill

# ---------------- README ----------------
ws = wb.active; ws.title = "Start Here"
ws.column_dimensions["A"].width = 110
lines = [
 ("Tampa Vendor Bench", TITLE),
 ("A one-workbook system for keeping reliable, fairly priced trades on call for Tampa rentals.", BODY),
 ("", BODY),
 ("How to use it", BOLD),
 ("1. Properties tab: list each rental once. The Job Log dropdown reads from it.", BODY),
 ("2. Vendor Bench tab: add every person you have vetted. Yellow cells are yours to fill. Jobs, spend and last-used update themselves from the Job Log.", BODY),
 ("3. Job Log tab: one row per job. Pick the property and vendor from the dropdowns, enter quote and paid, rate the job 1 to 5.", BODY),
 ("4. Triage Guide tab: before you call anyone, find the issue here. It tells you which trade, whether a license is legally required, how urgent it is, and a typical Tampa price so you know when a quote is high.", BODY),
 ("5. Tampa Sourcing tab: where to find new people when a bench slot is empty. Ranked by how well they filter for quality.", BODY),
 ("6. Vetting Checklist tab: the six checks to run before anyone gets a key. Every check is a free online lookup.", BODY),
 ("", BODY),
 ("Bench rules that keep prices low", BOLD),
 ("Keep 2 to 3 people per trade. One primary, one backup. A vendor who knows he is your default gets all the small jobs and prices them lower.", BODY),
 ("Route every small job through the handyman first. Only escalate to a licensed plumber or electrician when the Triage Guide says the law requires it.", BODY),
 ("Set a Not-To-Exceed amount per job when you call. Anything above it needs a call back before work continues.", BODY),
 ("Insurance expiry cells turn red 30 days out. Ask for a new certificate before sending the next job.", BODY),
 ("Book AC and roof work in spring. Tampa trades are booked solid June through October and prices rise with demand.", BODY),
 ("", BODY),
 ("Legend", BOLD),
 ("Yellow cells: you fill these in.  Grey row: example, delete it once you add a real entry.  Black text: formulas, leave alone.", BODY),
 ("", BODY),
 ("Prices in the Triage Guide are 2026 published national and Tampa ranges (HomeGuide, Angi, Homeyou), not quotes. Your Job Log will replace them with real numbers within a few months.", NOTE),
 ("Built 2026-09-08.", NOTE),
]
for i, (t, f) in enumerate(lines, 1):
    c = ws.cell(row=i, column=1, value=t); c.font = f
    c.alignment = Alignment(wrap_text=True, vertical="top")

# ---------------- Properties ----------------
wp = wb.create_sheet("Properties")
header(wp, 1, ["Property nickname", "Street address", "City / ZIP", "Type", "Tenant name", "Tenant phone", "Lockbox / access note", "Water heater / AC age", "Notes"],
       [18, 28, 14, 12, 18, 14, 24, 18, 30])
body(wp, 2, ["Example: Seminole Hts", "123 N Example St", "Tampa 33603", "SFH 3/2", "Jane Tenant", "813-555-0100", "Lockbox 4821 on side gate", "AC 2019, WH 2016", "Older cast-iron drain lines"], EX_FILL)
for r in range(3, 33):
    body(wp, r, [""]*9, INPUT_FILL)
wp.freeze_panes = "A2"

# ---------------- Vendor Bench ----------------
wv = wb.create_sheet("Vendor Bench")
vh = ["Vendor name", "Company", "Trade", "Phone", "Email / text", "Role", "Status",
      "FL license #", "License type", "License verified (date)", "GL insurance expiry", "Days to expiry",
      "Workers comp (Y / Exempt / None)", "Rate", "Trip / min charge", "Response time", "Found via",
      "Jobs done", "Total paid", "Avg rating", "Last used", "Notes"]
vw = [18, 18, 14, 13, 20, 10, 10, 14, 16, 14, 14, 10, 14, 12, 12, 12, 16, 9, 11, 9, 11, 34]
header(wv, 1, vh, vw)
ex = ["Example: Mike R.", "Mike's Home Repair LLC", "Handyman", "813-555-0101", "mike@example.com", "Primary", "Active",
      "n/a (under $1k jobs)", "None (handyman)", "2026-09-01", None, None, "Exempt", "$65/hr", "$85 first hour", "Same day", "Tampa REIA",
      None, None, None, None, "Does drywall, paint, fixtures, fences. Will not touch panel or pipe cuts."]
body(wv, 2, ex, EX_FILL)
from datetime import date
wv["K2"] = date(2027, 3, 15); wv["K2"].number_format = "yyyy-mm-dd"; wv["K2"].font = BODY; wv["K2"].border = BORDER
LOG = "'Job Log'"
SAMPLE_FILL = PatternFill("solid", fgColor="EAF2E3")
for r in range(2, 42):
    if r > 2:
        body(wv, r, [""]*22, INPUT_FILL)
    si = r - 3
    if 0 <= si < len(SAMPLE):
        v = SAMPLE[si]
        vals = [v.get("name",""), v.get("company",""), v.get("trade",""), v.get("phone",""), v.get("web",""),
                v.get("role","Candidate"), "Active", v.get("license",""), v.get("license_type",""), v.get("license_verified",""),
                None, None, v.get("wc",""), v.get("rate",""), v.get("trip",""), v.get("response",""), v.get("found_via",""),
                None, None, None, None, v.get("notes","")]
        body(wv, r, vals, SAMPLE_FILL)
        if v.get("gl_expiry"):
            wv[f"K{r}"] = v["gl_expiry"]
    # formula columns stay black on white
    for col, formula in [
        ("L", f'=IF(K{r}="","",K{r}-TODAY())'),
        ("R", f'=IF(A{r}="","",COUNTIF({LOG}!$E:$E,A{r}))'),
        ("S", f'=IF(A{r}="","",SUMIFS({LOG}!$H:$H,{LOG}!$E:$E,A{r}))'),
        ("T", f'=IF(OR(A{r}="",COUNTIFS({LOG}!$E:$E,A{r},{LOG}!$I:$I,">0")=0),"",AVERAGEIFS({LOG}!$I:$I,{LOG}!$E:$E,A{r},{LOG}!$I:$I,">0"))'),
        ("U", f'=IF(OR(A{r}="",COUNTIF({LOG}!$E:$E,A{r})=0),"",SUMPRODUCT(MAX(({LOG}!$E$2:$E$500=A{r})*{LOG}!$A$2:$A$500)))'),
    ]:
        c = wv[f"{col}{r}"]; c.value = formula; c.fill = PatternFill(fill_type=None); c.font = BODY; c.border = BORDER
    wv[f"K{r}"].number_format = "yyyy-mm-dd"
    wv[f"J{r}"].number_format = "yyyy-mm-dd"
    wv[f"S{r}"].number_format = '$#,##0;($#,##0);-'
    wv[f"T{r}"].number_format = "0.0"
    wv[f"U{r}"].number_format = "yyyy-mm-dd"
wv.freeze_panes = "D2"

# dropdowns
dv_trade = DataValidation(type="list", formula1='"Handyman,Plumber,Electrician,HVAC,Roofer,Appliance,Pest,Lawn / Tree,Cleaner / Turnover,Locksmith,Painter,Drywall / Stucco,Pool,Fence / Gate,GC"', allow_blank=True)
dv_role = DataValidation(type="list", formula1='"Primary,Backup,Trial,Candidate,Retired"', allow_blank=True)
dv_status = DataValidation(type="list", formula1='"Active,On hold,Do not use"', allow_blank=True)
dv_wc = DataValidation(type="list", formula1='"Y,Exempt,None,Unknown"', allow_blank=True)
for dv, rng in [(dv_trade, "C2:C41"), (dv_role, "F2:F41"), (dv_status, "G2:G41"), (dv_wc, "M2:M41")]:
    wv.add_data_validation(dv); dv.add(rng)

# conditional: insurance within 30 days or expired -> red
red = PatternFill("solid", fgColor="F8CBAD")
wv.conditional_formatting.add("K2:L41", FormulaRule(formula=['AND($K2<>"",$K2-TODAY()<30)'], fill=red))
grey = PatternFill("solid", fgColor="D9D9D9")
wv.conditional_formatting.add("A2:V41", FormulaRule(formula=['$G2="Do not use"'], fill=grey))

# ---------------- Job Log ----------------
wl = wb.create_sheet("Job Log")
lh = ["Date", "Property", "Issue (short)", "Trade", "Vendor", "Urgency", "Quote / NTE", "Paid", "Rating 1-5", "Permit needed?", "Tenant caused?", "Notes / what was done"]
lw = [11, 18, 30, 13, 18, 11, 12, 11, 9, 11, 11, 40]
header(wl, 1, lh, lw)
body(wl, 2, [date(2026, 9, 1), "Example: Seminole Hts", "Kitchen faucet dripping", "Handyman", "Example: Mike R.", "Routine", 120, 110, 5, "No", "No", "Replaced cartridge. 45 min."], EX_FILL)
wl["A2"].number_format = "yyyy-mm-dd"
for r in range(3, 501):
    if r <= 40:
        body(wl, r, [""]*12, INPUT_FILL)
    wl[f"A{r}"].number_format = "yyyy-mm-dd"
    wl[f"G{r}"].number_format = '$#,##0'; wl[f"H{r}"].number_format = '$#,##0'
wl["G2"].number_format = '$#,##0'; wl["H2"].number_format = '$#,##0'
dv_prop = DataValidation(type="list", formula1="=Properties!$A$2:$A$32", allow_blank=True)
dv_vendor = DataValidation(type="list", formula1="='Vendor Bench'!$A$2:$A$41", allow_blank=True)
dv_urg = DataValidation(type="list", formula1='"Emergency,24 hr,This week,Routine,Turnover"', allow_blank=True)
dv_yn = DataValidation(type="list", formula1='"Yes,No,Unsure"', allow_blank=True)
dv_rate = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True)
dv_trade2 = DataValidation(type="list", formula1='"Handyman,Plumber,Electrician,HVAC,Roofer,Appliance,Pest,Lawn / Tree,Cleaner / Turnover,Locksmith,Painter,Drywall / Stucco,Pool,Fence / Gate,GC"', allow_blank=True)
for dv, rng in [(dv_prop, "B2:B500"), (dv_vendor, "E2:E500"), (dv_urg, "F2:F500"), (dv_yn, "J2:K500"), (dv_rate, "I2:I500"), (dv_trade2, "D2:D500")]:
    wl.add_data_validation(dv); dv.add(rng)
wl.freeze_panes = "A2"
# summary block
wl["N1"] = "Spend summary"; wl["N1"].font = BOLD
wl["N2"] = "Total paid, all time"; wl["O2"] = "=SUM(H2:H500)"
wl["N3"] = "Total paid, last 90 days"; wl["O3"] = '=SUMIFS(H2:H500,A2:A500,">="&(TODAY()-90))'
wl["N4"] = "Jobs, last 90 days"; wl["O4"] = '=COUNTIFS(A2:A500,">="&(TODAY()-90),H2:H500,"<>")'
wl["N5"] = "Avg cost per job, last 90 days"; wl["O5"] = '=IF(O4=0,0,O3/O4)'
wl["N6"] = "Emergency jobs, last 90 days"; wl["O6"] = '=COUNTIFS(A2:A500,">="&(TODAY()-90),F2:F500,"Emergency")'
for r in range(2, 7):
    wl[f"N{r}"].font = BODY; wl[f"O{r}"].font = BODY
    wl[f"O{r}"].number_format = '$#,##0' if r in (2, 3, 5) else '0'
wl.column_dimensions["N"].width = 28; wl.column_dimensions["O"].width = 12

# ---------------- Triage Guide ----------------
wt = wb.create_sheet("Triage Guide")
th = ["Issue tenant reports", "Send this trade first", "FL license legally required?", "Urgency", "Typical Tampa cost (2026)", "Before you dispatch"]
tw = [30, 16, 26, 11, 20, 46]
header(wt, 1, th, tw)
triage = [
 ("No water / major leak / burst pipe", "Plumber", "Yes. Any pipe cutting or drain alteration.", "Emergency", "$150-400 service + repair", "Have tenant shut main valve. Show them where it is on move-in."),
 ("Clogged sink / tub drain", "Handyman", "No, if snaking only. Yes if pipe is opened.", "This week", "$75-250", "Ask tenant to try a plunger first. Recurring clogs on cast iron = plumber camera."),
 ("Running or leaking toilet", "Handyman", "No. Flapper, fill valve, wax ring are all handyman.", "This week", "$100-200", "Photo of tank interior. Usually a $15 part."),
 ("Dripping faucet / bad cartridge", "Handyman", "No. Fixture replacement is exempt.", "Routine", "$90-180", "Confirm brand from photo so he brings the cartridge."),
 ("Water heater dead", "Plumber", "Yes. Permit required for replacement in Tampa.", "24 hr", "$1,200-2,200 installed (40 gal)", "Check age on the label. Over 12 years, replace, do not repair."),
 ("Garbage disposal jammed / dead", "Handyman", "No. Like-for-like swap is exempt.", "Routine", "$150-300 installed", "Reset button and allen key first, tenant can try."),
 ("No power to whole unit", "Electrician", "Yes.", "Emergency", "$100-200 diagnostic", "Have tenant check main breaker and call TECO first. Half of these are utility side."),
 ("One outlet / switch dead, breaker trips", "Electrician", "Yes. Anything inside the box or panel.", "24 hr", "$150-350", "GFCI reset first. Tenant can try every GFCI in kitchen, baths, garage."),
 ("Light fixture / ceiling fan swap", "Handyman", "Grey area. Like-for-like swap is commonly done by handymen. New circuit = electrician.", "Routine", "$75-150 labor", "Only if replacing an existing fixture on existing wiring."),
 ("AC not cooling", "HVAC", "Yes. Refrigerant and electrical work need a license.", "Emergency (Jun-Oct)", "$100-150 diagnostic, $300-800 common repairs", "Tenant: change filter, check thermostat batteries, check breaker, check drain line float switch. Solves 30% of calls."),
 ("AC drain line clogged / water at air handler", "Handyman", "No. Clearing the condensate line is maintenance.", "24 hr", "$75-150", "Put a $10 float switch on every unit. Vinegar in drain line quarterly."),
 ("Roof leak", "Roofer", "Yes.", "24 hr", "$300-900 repair", "Tarp first if storm season. Take photos of ceiling stain for insurance."),
 ("Fridge / range / washer dead", "Appliance", "No.", "24 hr (fridge)", "$100-150 diagnostic", "Under 8 years old, repair. Over, replace and skip the diagnostic fee."),
 ("Lockout / rekey at turnover", "Locksmith", "No.", "Routine", "$100-200 rekey", "Rekey every turnover, do not replace. Keep 2 keys."),
 ("Drywall hole / paint / caulk", "Handyman", "No.", "Routine", "$50-80/hr", "Batch these. Send one visit per property per month, not one per issue."),
 ("Fence down / gate broken", "Handyman or Fence", "No under $1,000 total. Yes above.", "Routine", "$200-600 per section", "Post-storm, expect 2-3 week waits."),
 ("Pests (ants, roaches, rodents)", "Pest", "Yes. Pest control is state licensed.", "This week", "$100-200 one-time, $40-60/mo plan", "Quarterly plan across all units beats one-off calls."),
 ("Mold / musty smell", "Handyman first", "Depends. Over 10 sq ft of mold remediation needs a licensed remediator in FL.", "24 hr", "$150 inspect", "Find the water source first. Mold is a symptom."),
 ("Stucco cracks / exterior", "Drywall / Stucco", "No if cosmetic under $1,000.", "Routine", "$300-800", "Spring only. Seal before rainy season."),
 ("Anything over $1,000 or needing a permit", "GC or licensed trade", "Yes. FL law, no exceptions.", "Varies", "Get 3 quotes", "Verify license and insurance again even for a bench vendor. Pull permit in owner or contractor name, never tenant."),
]
for i, row in enumerate(triage, 2):
    body(wt, i, list(row))
wt.freeze_panes = "A2"
wt.cell(row=len(triage)+3, column=1, value="Sources: Florida Statute 489 ($1,000 handyman threshold; licensed trades for plumbing, electrical, HVAC, roofing, pest). Cost ranges from HomeGuide, Angi, Homeyou 2026 Tampa and national data. Ranges are estimates, replace with your Job Log averages.").font = NOTE
wt.merge_cells(start_row=len(triage)+3, start_column=1, end_row=len(triage)+3, end_column=6)
wt.row_dimensions[len(triage)+3].height = 30
wt.cell(row=len(triage)+3, column=1).alignment = Alignment(wrap_text=True)

# ---------------- Tampa Sourcing ----------------
wsrc = wb.create_sheet("Tampa Sourcing")
sh = ["Rank", "Channel", "Best for", "Cost", "Link", "How to work it"]
sw = [6, 30, 24, 14, 40, 60]
header(wsrc, 1, sh, sw)
sourcing = [
 (1, "Tampa REIA (Tampa Real Estate Investors Alliance)", "Every trade. Vendors here already work for landlords, so they know the volume-rate game.", "Meetup free, membership ~$100/yr", "https://tampareia.com/", "Go to one monthly meeting. Ask three investors with 10+ doors who they use for plumbing, electric, and handyman. Write down every name that comes up twice."),
 (2, "Tampa Bay REIA (TBREIA)", "Same as above, different crowd. Sub-groups across the Bay.", "Meetup free", "https://www.meetup.com/tampabayreia/", "Post in the group: 'Looking for a licensed plumber who works with investors in [neighborhood].' Investor referrals beat homeowner referrals."),
 (3, "Other landlords in your ZIP", "The cheapest reliable people. Nobody advertises them.", "Free", "", "Knock on the door of the other rental on your street, or ask your property's previous owner. One good handyman referral is worth the whole list."),
 (4, "Facebook groups: search 'Tampa landlord', 'Tampa Bay real estate investors', 'Hillsborough County homeowners'", "Handyman, lawn, cleaner, appliance", "Free", "https://www.facebook.com/groups/search/groups/?q=tampa%20landlord", "Search the group history before posting; the same 5 names get recommended every month. Ignore anyone who replies 'DM me' with no company name."),
 (5, "Nextdoor (set to your rental's neighborhood)", "Handyman, lawn, pressure wash, cleaner", "Free", "https://nextdoor.com/", "Neighbors recommend people who show up. Good for the sub-$1,000 handyman tier only."),
 (6, "Thumbtack", "Handyman, cleaner, appliance, junk removal", "Free to browse, pros pay per lead", "https://www.thumbtack.com/fl/tampa/", "Fast quotes, good for filling a backup slot. Sort by reviews with 50+, then verify license yourself. Do not rely on Thumbtack's badge."),
 (7, "Angi / HomeAdvisor", "Licensed trades (plumber, electrician, HVAC, roofer)", "Free", "https://www.angi.com/companylist/tampa/", "Pricier tier. Use it for the licensed backup, not the primary. Angi-listed shops rarely negotiate."),
 (8, "Home Depot Pro Referral", "Licensed trades for permitted work", "Free", "https://www.homedepot.com/services/", "Pre-screened for license and insurance. Prices are mid-market. Useful when you need a permit pulled fast."),
 (9, "Google Maps, search '[trade] near [rental ZIP]' and sort by rating", "Any", "Free", "https://www.google.com/maps", "Filter for 4.7+ with 100+ reviews AND a real address. Read the 1-star reviews for the pattern (no-shows vs pricing)."),
 (10, "TaskRabbit", "Furniture assembly, mounting, moving help, minor handyman", "Taskers set hourly rate", "https://www.taskrabbit.com/locations/tampa", "Fine for turnover odd jobs. Not for plumbing, electric, or anything on a ladder over 6 ft."),
 (11, "Lula (maintenance coordination, covers Tampa)", "The 'always have someone' backstop. They take the tenant call, triage, dispatch a vetted pro, bill you.", "Per-job pricing plus service fee; ask for current terms", "https://lula.life/services", "Best once you are past ~10 doors or living out of state. Set a Not-To-Exceed and they call before exceeding it. Also available through TurboTenant as Maintenance Plus."),
 (12, "Latchel", "Same idea as Lula: 24/7 tenant maintenance line and dispatch", "Monthly per unit, ask for a quote", "https://latchel.com/", "Compare against Lula. Ask both which Tampa vendors they actually dispatch and whether you can add your own bench."),
 (13, "Hillsborough County licensed contractor list", "Confirms a name is legit, also a way to find licensed locals", "Free", "https://hcfl.gov/businesses/hillsgovhub/contractor-licensing", "Search by trade to find registered locals in your area. Cross-check with reviews."),
]
for i, row in enumerate(sourcing, 2):
    body(wsrc, i, list(row))
    if row[4]:
        c = wsrc.cell(row=i, column=5); c.hyperlink = row[4]; c.font = LINK
wsrc.freeze_panes = "A2"

# ---------------- Vetting Checklist ----------------
wc = wb.create_sheet("Vetting Checklist")
ch = ["Step", "Check", "Where (free lookup)", "Link", "Pass / fail rule"]
cw = [6, 34, 40, 44, 50]
header(wc, 1, ch, cw)
checks = [
 (1, "State license active (plumber, electrician, HVAC, roofer, GC, pest)", "Florida DBPR license search. Search by name or license number.", "https://www.myfloridalicense.com/wl11.asp", "Status must read Current, Active. Note the expiry date and any discipline. Null and Void or Inactive = fail."),
 (2, "County registration (for county-registered, not state-certified, contractors)", "HillsGovHub record search, Contractor Licensing.", "https://hcfl.gov/businesses/hillsgovhub/contractor-licensing", "If they hold a Hillsborough registration rather than a state certification, it must be active here. Registered contractors can only work inside the county."),
 (3, "General liability insurance", "Ask for a Certificate of Insurance (COI) with you named as certificate holder.", "", "Minimum $300k GL for handyman, $1M for licensed trades. Enter the expiry on the Bench so the cell turns red 30 days out."),
 (4, "Workers comp coverage or exemption", "Florida DWC Proof of Coverage database. Search by business name.", "https://dwcdataportal.fldfs.com/ProofOfCoverage.aspx", "Either an active policy or a current exemption on file. A solo handyman with an exemption is fine. A crew with no policy is your liability if someone gets hurt."),
 (5, "Business is real", "Sunbiz (Florida Division of Corporations).", "https://search.sunbiz.org/Inquiry/CorporationSearch/ByName", "Active LLC or Inc matching the name on the COI. Not required for a solo handyman, but a plus."),
 (6, "Reputation", "Google reviews, BBB, and the REIA group history.", "https://www.bbb.org/local-bbb/bbb-of-west-florida", "Read the 1-star reviews. No-shows and surprise charges are the deal-breakers. Bad grammar in a reply is not."),
 (7, "Trial job", "Give them one small, non-urgent job at one property.", "", "Judge on: showed up when they said, sent a photo when done, invoice matched quote. Pass all three = Primary or Backup. Fail any = Retired."),
 (8, "Rate agreement", "Text or email, kept in the Notes column.", "", "Agree hourly or flat rate, trip charge, and that you are called before any job exceeds the NTE. Ask for a volume rate: 'I have X doors, what is your rate for a landlord who sends you everything?'"),
]
for i, row in enumerate(checks, 2):
    body(wc, i, list(row))
    if row[3]:
        c = wc.cell(row=i, column=4); c.hyperlink = row[3]; c.font = LINK
wc.freeze_panes = "A2"
r = len(checks) + 3
wc.cell(row=r, column=1, value="Tampa-specific notes").font = BOLD
notes = [
 "City of Tampa proper permits through the City of Tampa Accela portal, not HillsGovHub. Unincorporated Hillsborough (Brandon, Riverview, Town 'n' Country, Carrollwood) uses HillsGovHub. Check which one your address falls under before a permitted job.",
 "Hurricane season is June 1 to Nov 30. Roofers, fence crews and tree services book out weeks after any named storm. Get roof and tree work done in March-May.",
 "AC failures spike June-September. A backup HVAC vendor is not optional in Tampa. Float switches on every air handler prevent the most common ceiling-water call.",
 "Older Tampa housing (Seminole Heights, Ybor, South Tampa bungalows) has cast-iron drain lines and sometimes knob-and-tube or aluminum wiring. Ask the vendor if they have worked on it before you send them.",
 "Florida has no handyman license. The $1,000 total-job threshold and the trade rules are state law (Ch. 489). An unlicensed person doing licensed work voids your ability to enforce the contract and can affect insurance claims.",
]
for i, n in enumerate(notes, 1):
    c = wc.cell(row=r+i, column=1, value=n); c.font = BODY; c.alignment = Alignment(wrap_text=True, vertical="top")
    wc.merge_cells(start_row=r+i, start_column=1, end_row=r+i, end_column=5)
    wc.row_dimensions[r+i].height = 32

import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Tampa Vendor Bench.xlsx")
wb.save(out)
print("saved", out)
