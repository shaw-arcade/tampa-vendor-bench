#!/usr/bin/env python3
"""Merge the three Pasco painter research files into one ranked list of 50.

Reads research/pasco-{west,central,east}-painters.json, dedupes by phone and by
normalized company name, scores each vendor, and writes:
  - pasco_painters_50.json   (the working list)
  - PAINTER-LIST.md          (owner-facing table)
"""
import json, re, os, sys
from collections import OrderedDict

BASE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(BASE), "research")
REGIONS = [("west", "West Pasco"), ("central", "Central Pasco"), ("east", "East Pasco")]

def all_phones(p):
    """A record can carry two numbers in one string; return every 10-digit one."""
    s = str(p or "")
    out = set()
    for m in re.findall(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", s):
        d = re.sub(r"\D", "", m)
        if len(d) == 10:
            out.add(d)
    return out

def cname(v):
    return v.get("company") or v.get("name") or "?"

def norm_name(n):
    n = (n or "").lower()
    n = re.sub(r"\b(llc|inc|incorporated|corp|corporation|co|company|the|and|&|of|services|service|painting|painters|painter|paint)\b", " ", n)
    return re.sub(r"[^a-z0-9]", "", n)

def num(v, default=0.0):
    try:
        return float(str(v).strip())
    except Exception:
        return default

def score(v):
    """Higher is better. Built to favor small, reviewed, corroborated shops."""
    s = 0.0
    gr, gc = num(v.get("google_rating")), num(v.get("google_reviews"))
    yr, yc = num(v.get("yelp_rating")), num(v.get("yelp_reviews"))
    # rating quality, weighted by how much evidence backs it
    if gr and gc:
        s += (gr - 3.5) * 10 * min(gc / 40.0, 1.5)
    if yr and yc:
        s += (yr - 3.5) * 5 * min(yc / 20.0, 1.0)
    # review volume, with diminishing returns
    s += min(gc, 300) ** 0.5
    # contactability: email or a form beats phone-only for a 50-vendor send
    ch = str(v.get("contact_channel", "")).lower()
    if "email" in ch: s += 12
    elif "form" in ch or "http" in ch: s += 8
    elif "facebook" in ch: s += 3
    if str(v.get("email", "")).strip() not in ("", "unknown", "none"): s += 6
    # corroboration and legitimacy
    if str(v.get("sunbiz_status", "")).lower().startswith("active"): s += 10
    if str(v.get("insured_claim", "")).lower() == "yes": s += 6
    if len(v.get("source_urls") or []) >= 2: s += 4
    yib = num(v.get("years_in_business"))
    if yib: s += min(yib, 20) * 0.5
    # franchises stay in as price references but should not crowd out locals
    if v.get("franchise") is True: s -= 15
    # red flags
    notes = str(v.get("notes", "")).lower()
    for flag in ("no-show", "no show", "unlicensed", "complaint", "lawsuit", "scam"):
        if flag in notes: s -= 12
    if not gc and not yc: s -= 10
    return round(s, 1)

def load():
    rows, missing = [], []
    for key, label in REGIONS:
        p = os.path.join(RES, f"pasco-{key}-painters.json")
        if not os.path.exists(p):
            missing.append(p); continue
        with open(p) as f:
            data = json.load(f)
        for v in data:
            v["region"] = label
            rows.append(v)
    return rows, missing

def dedupe(rows):
    """Two records are the same vendor if they share ANY phone number or a
    normalized company name. Records often carry two numbers, so match on sets."""
    kept = []          # list of (phoneset, namekey, record)
    for v in rows:
        ph, nk = all_phones(v.get("phone")), norm_name(cname(v))
        match = None
        for slot in kept:
            if (ph and slot[0] & ph) or (nk and nk == slot[1]):
                match = slot
                break
        if match:
            old = match[2]
            richer, thinner = (v, old) if len(json.dumps(v)) > len(json.dumps(old)) else (old, v)
            if thinner.get("region") != richer.get("region"):
                richer["also_listed_in"] = thinner.get("region")
            match[0].update(ph)
            kept[kept.index(match)] = (match[0], match[1] or nk, richer)
        else:
            kept.append((set(ph), nk, v))
    return [k[2] for k in kept]

def main():
    rows, missing = load()
    if missing:
        print("MISSING research files, cannot build final list:")
        for m in missing: print("  ", m)
    if not rows:
        print("No vendor rows loaded. Nothing written."); sys.exit(1)
    rows = dedupe(rows)
    for v in rows:
        v["score"] = score(v)
    rows.sort(key=lambda v: -v["score"])
    final = rows[:50]
    with open(os.path.join(BASE, "pasco_painters_50.json"), "w") as f:
        json.dump(final, f, indent=1)
    # owner-facing table
    lines = ["# Pasco County interior painters, quote list", "",
             f"Sourced 2026-09-09 by web research only. No one has been contacted.",
             f"Loaded {len(rows)} unique vendors, listing top {len(final)}.", "",
             "| # | Company | City | Region | Phone | Best contact | Google | Yelp | Sunbiz | Notes |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for i, v in enumerate(final, 1):
        g = f"{v.get('google_rating','?')} ({v.get('google_reviews','?')})"
        y = f"{v.get('yelp_rating','?')} ({v.get('yelp_reviews','?')})"
        tag = " [franchise]" if v.get("franchise") is True else ""
        note = str(v.get("notes", ""))[:120].replace("|", "/")
        lines.append(f"| {i} | {cname(v)}{tag} | {v.get('city','?')} | {v.get('region','?')} | "
                     f"{v.get('phone','?')} | {v.get('contact_channel','?')} | {g} | {y} | "
                     f"{v.get('sunbiz_status','?')} | {note} |")
    with open(os.path.join(BASE, "PAINTER-LIST.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    # contactability breakdown, decides how the send actually happens
    ch = {}
    for v in final:
        c = str(v.get("contact_channel", "unknown")).split()[0].lower()
        ch[c] = ch.get(c, 0) + 1
    print(f"Wrote {len(final)} vendors.")
    print("By region:", {r[1]: sum(1 for v in final if v.get('region') == r[1]) for r in REGIONS})
    print("By contact channel:", ch)
    print("Franchises included:", sum(1 for v in final if v.get('franchise') is True))

if __name__ == "__main__":
    main()
