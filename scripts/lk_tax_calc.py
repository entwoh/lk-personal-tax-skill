#!/usr/bin/env python3
"""Sri Lanka personal income tax calculator (pure Python, no dependencies).

Usage:
  lk_tax_calc.py annual --ya 2025/26 --employment 3600000 --apit-paid 222000
  lk_tax_calc.py apit --monthly 350000 --ya 2025/26
Rules snapshot: October 2026. Verify at ird.gov.lk before relying on results.
"""
import argparse
import json
import sys

# (relief, [(band_width or None for balance, rate), ...])
YA_TABLES = {
    "2023/24": (1_200_000, [(500_000, .06), (500_000, .12), (500_000, .18), (500_000, .24), (500_000, .30), (None, .36)]),
    "2024/25": (1_200_000, [(500_000, .06), (500_000, .12), (500_000, .18), (500_000, .24), (500_000, .30), (None, .36)]),
    "2025/26": (1_800_000, [(1_000_000, .06), (500_000, .18), (500_000, .24), (500_000, .30), (None, .36)]),
    "2026/27": (1_800_000, [(1_000_000, .06), (500_000, .18), (500_000, .24), (500_000, .30), (None, .36)]),
}
FOREIGN_CAP = 0.15
RENT_RELIEF = 0.25
SOLAR_MAX = 600_000
DONATION_MAX = 75_000

L = {
    "en": {
        "title": "Sri Lanka income tax - Y/A {ya}", "assess": "Assessable income", "rentrel": "Rent relief (25%)",
        "pers": "Personal relief", "solar": "Solar relief", "don": "Donations (qualifying)", "taxable": "Taxable income",
        "band": "Band", "tax": "Tax before credits", "credits": "Credits (APIT/AIT/WHT/instalments)",
        "pay": "BALANCE PAYABLE (by 30 Sep)", "refund": "REFUND / OVERPAID", "eff": "Effective rate on assessable income",
        "apit": "Monthly APIT", "gross": "Monthly gross", "foreign": "foreign income, max 15%", "note": "General guidance only - confirm with ird.gov.lk or a registered tax advisor.",
    },
    "si": {
        "title": "ශ්‍රී ලංකා ආදායම් බද්ද - Y/A {ya}", "assess": "තක්සේරු කළ හැකි ආදායම (Assessable income)",
        "rentrel": "කුලී සහනය (Rent relief 25%)", "pers": "පුද්ගලික සහන (Personal relief)", "solar": "සූර්ය පැනල සහනය (Solar relief)",
        "don": "පරිත්‍යාග (Donations)", "taxable": "බදු ගෙවිය යුතු ආදායම (Taxable income)", "band": "පරාසය",
        "tax": "බද්ද (credits පෙර)", "credits": "ගෙවූ බදු (APIT/AIT/WHT/instalments)",
        "pay": "ගෙවිය යුතු ශේෂය (සැප්තැම්බර් 30 ට පෙර)", "refund": "ආපසු ලැබිය යුතු මුදල (Refund)",
        "eff": "සඵල බදු අනුපාතය", "apit": "මාසික APIT", "gross": "මාසික දළ ආදායම",
        "foreign": "විදේශ ආදායම, උපරිම 15%",
        "note": "මෙය සාමාන්‍ය මඟපෙන්වීමක් පමණි; ird.gov.lk හෝ ලියාපදිංචි බදු උපදේශකයෙකු සමඟ තහවුරු කරගන්න.",
    },
}


def rs(x):
    x = round(x) + 0  # avoid "-0"
    return f"Rs. {x:,.0f}"


def compute_bands(taxable, bands, foreign_top=0.0):
    """Apply bands to `taxable`; the top `foreign_top` rupees are taxed at min(rate, 15%)."""
    rows, remaining, start, total = [], taxable, 0.0, 0.0
    for width, rate in bands:
        if remaining <= 0:
            break
        amt = remaining if width is None else min(remaining, width)
        end = start + amt
        # portion of this slice that lies in the foreign (top) layer
        f_start = taxable - foreign_top
        f_amt = max(0.0, end - max(start, f_start))
        o_amt = amt - f_amt
        f_rate = min(rate, FOREIGN_CAP)
        t = o_amt * rate + f_amt * f_rate
        rows.append((start, end, rate, amt, t, o_amt, f_amt, f_rate))
        total += t
        remaining -= amt
        start = end
    return rows, total


def annual(a):
    if a.ya not in YA_TABLES:
        sys.exit(f"Unsupported Y/A {a.ya}. Supported: {', '.join(YA_TABLES)}")
    relief, bands = YA_TABLES[a.ya]
    rent_rel = a.rent * RENT_RELIEF
    ordinary = a.employment + a.business + a.interest + a.other + (a.rent - rent_rel)
    foreign = a.foreign
    assessable = a.employment + a.business + a.interest + a.other + a.rent + foreign
    solar = min(a.solar, SOLAR_MAX)
    pre_don = max(0.0, ordinary + foreign - relief - solar)
    don = min(a.donations, DONATION_MAX, pre_don / 3)
    taxable = max(0.0, pre_don - don)
    # relief and deductions reduce ordinary income first, so foreign stays the top layer
    foreign_top = min(foreign, taxable)
    rows, tax = compute_bands(taxable, bands, foreign_top)
    credits = a.apit_paid + a.ait_paid + a.rent_wht + a.wht_paid + a.instalments
    bal = tax - credits
    res = dict(ya=a.ya, assessable=assessable, rent_relief=rent_rel, personal_relief=relief, solar_relief=solar,
               donations=don, taxable=taxable, tax=tax, credits=credits, balance=bal,
               effective_rate=(tax / assessable if assessable else 0.0),
               bands=[dict(from_=r[0], to=r[1], rate=r[2], amount=r[3], tax=r[4],
                          ordinary_amount=r[5], foreign_amount=r[6], foreign_rate=r[7]) for r in rows])
    return res


def print_annual(r, lang):
    t = L[lang]
    print(t["title"].format(ya=r["ya"]))
    print("-" * 60)
    for k, v in [("assess", r["assessable"]), ("rentrel", -r["rent_relief"] or 0), ("pers", -r["personal_relief"]),
                 ("solar", -r["solar_relief"]), ("don", -r["donations"])]:
        print(f"{t[k]:<48}{('-' + rs(-v)) if round(v) < 0 else rs(v):>14}")
    print(f"{t['taxable']:<48}{rs(r['taxable']):>14}")
    for b in r["bands"]:
        rng = f"  {t['band']} {b['from_']:>10,.0f}-{b['to']:>10,.0f}"
        parts = []
        if b["ordinary_amount"] > 0:
            parts.append((b["rate"], b["ordinary_amount"], ""))
        if b["foreign_amount"] > 0:
            parts.append((b["foreign_rate"], b["foreign_amount"], f" ({t['foreign']})"))
        for i, (rate, amt, tag) in enumerate(parts):
            label = rng if i == 0 else " " * len(rng)
            print(f"{label} @ {rate*100:>4.0f}% on {rs(amt):>14} = {rs(amt * rate)}{tag}")
    print(f"{t['tax']:<48}{rs(r['tax']):>14}")
    print(f"{t['credits']:<48}{('-' + rs(r['credits'])) if round(r['credits']) > 0 else rs(0):>14}")
    key = "pay" if r["balance"] >= 0 else "refund"
    print(f"{t[key]:<48}{rs(abs(r['balance'])):>14}")
    print(f"{t['eff']}: {r['effective_rate']*100:.2f}%")
    print(t["note"])


def apit(a):
    r = annual(argparse.Namespace(ya=a.ya, employment=a.monthly * 12, business=0, rent=0, interest=0, other=0,
                                  foreign=0, solar=0, donations=0, apit_paid=0, ait_paid=0, rent_wht=0,
                                  wht_paid=0, instalments=0))
    return dict(ya=a.ya, monthly_gross=a.monthly, annual_tax=r["tax"], monthly_apit=r["tax"] / 12)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("annual", help="annual tax computation (all amounts annual, in Rs.)")
    pa.add_argument("--ya", default="2025/26")
    for f in ("employment", "business", "rent", "interest", "other", "foreign", "solar", "donations",
              "apit-paid", "ait-paid", "rent-wht", "wht-paid", "instalments"):
        pa.add_argument("--" + f, type=float, default=0.0,
                        help={"foreign": "foreign-currency service/foreign-source income remitted via bank (rate capped at 15%%)",
                              "business": "net profit", "rent": "gross rent (25%% relief applied)",
                              "solar": "solar panel cost/loan repayments (max 600,000)"}.get(f))
    pa.add_argument("--lang", choices=["en", "si"], default="en")
    pa.add_argument("--json", action="store_true")
    pp = sub.add_parser("apit", help="monthly APIT on a salary")
    pp.add_argument("--monthly", type=float, required=True, help="monthly gross taxable employment income")
    pp.add_argument("--ya", default="2025/26")
    pp.add_argument("--lang", choices=["en", "si"], default="en")
    pp.add_argument("--json", action="store_true")
    a = p.parse_args()
    for k in list(vars(a)):
        if "-" in k:
            setattr(a, k.replace("-", "_"), getattr(a, k))
    if a.cmd == "annual":
        r = annual(a)
        print(json.dumps(r, indent=2)) if a.json else print_annual(r, a.lang)
    else:
        r = apit(a)
        if a.json:
            print(json.dumps(r, indent=2))
        else:
            t = L[a.lang]
            print(f"Y/A {r['ya']} | {t['gross']}: {rs(r['monthly_gross'])} | {t['apit']}: {rs(r['monthly_apit'])} (annual {rs(r['annual_tax'])})")
            print(t["note"])


if __name__ == "__main__":
    main()
