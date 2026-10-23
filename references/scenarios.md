# Worked examples (Y/A 2025/26) — verify with `scripts/lk_tax_calc.py`

1. **Salaried, Rs. 350,000/month**: annual 4,200,000 − relief 1,800,000 = 2,400,000 → 60,000 + 90,000 + 120,000 + 120,000 (400,000 @30%) = **Rs. 390,000 a year → Rs. 32,500 a month APIT** (`apit --monthly 350000`). No return needed if APIT is the only income.
2. **Salary Rs. 3.6M + FD interest Rs. 400,000 (AIT Rs. 40,000, APIT Rs. 156,000)**: taxable 2,200,000 → tax 330,000 − credits 196,000 = **Rs. 134,000 payable** by 30 Sep; return required (interest exceeds Rs. 5,000).
3. **Freelancer, Rs. 6M foreign-currency income remitted via bank, no other income**: taxable 4.2M; bands capped at 15% → 60,000 + 3 × 75,000 + 255,000 = **Rs. 540,000** (`--foreign 6000000`). Register for TIN, pay quarterly instalments, file by 30 Nov.
4. **Landlord, rent Rs. 150,000/month (tenant withholds 10%)**: gross 1.8M; rent relief 25% (450,000) → 1.35M less personal relief 1.8M ⇒ taxable 0; WHT of Rs. 180,000 is refundable via return.
5. **Mixed**: salary + rent + interest + donation: sum assessable, apply rent relief, personal relief, capped donation, subtract all credits. Use `annual` with each flag.
6. **Selling land**: CGT 15% (sale after 3 Jun 2026) on gain, within 30 days — outside the bands.
