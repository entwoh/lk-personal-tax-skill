# lk-personal-tax

Sri Lanka personal income tax assistant as an agent skill (Claude) and a Custom GPT (ChatGPT). Rules snapshot: **October 2026**.

## For everyone (no technical knowledge needed)

### What can it do?
Ask it about Sri Lankan personal income tax in **Sinhala, English or Singlish**, for example:
- "My salary is Rs. 350,000 a month. How much APIT is deducted?"
- "Do I need to file a tax return for 2025/26?"
- "I get paid in USD by foreign clients. How is that taxed?"
- "When are my quarterly instalments due?"
- "tax file එක දාන්නේ කොහොමද?" (how do I file on RAMIS?)

It can tell you:
- whether you must pay or file a return
- how much tax you owe, with the working shown step by step
- how much tax is taken from your salary each month (APIT)
- the due dates for instalments, final payment and the return
- tax on interest, rent, service fees, dividends, and on selling land or shares
- which documents to collect, and how to register for a TIN, file on RAMIS and pay

### What it will NOT do
- It does not log in to RAMIS or file or pay for you. It explains the steps and you do them.
- It never needs your NIC, TIN, bank details or passwords. Don't share them.
- It is not a licensed tax advisor. For complicated cases (partnerships, mid-year change of residency, gratuity, foreign tax credits), it points you to the IRD or a registered tax advisor.
- The rules are as at **October 2026**. Sri Lankan tax law changes often, usually in the November Budget, so confirm important figures at ird.gov.lk.

### How to start using it
Pick the one that matches the app you already use:

**A. ChatGPT (easiest to share with family and friends)**
1. Open ChatGPT, then **Explore GPTs → Create** (a paid plan is needed to create a GPT).
2. Open `chatgpt/custom-gpt-instructions.md` and copy the text under "Instructions" into the Instructions box.
3. Upload the files from the `references/` folder and `scripts/lk_tax_calc.py` as Knowledge. Turn on Web Search and Code Interpreter.
4. Save, then ask your question.

**B. Claude (claude.ai)**
1. Compress this whole folder into a `.zip` file.
2. Go to **Settings → Capabilities → Skills** and upload the zip. This needs a plan that supports Skills.
3. Start a new chat and ask your tax question.

**C. Claude Code (for developers)**: see "Install" below.

### Tips for good answers
- Say which year you mean (for example "2025/26"). The tax year runs from 1 April to 31 March.
- Give amounts per month or per year and say which. Have your salary slip, T-10 certificate or bank interest certificate nearby.
- Read the "assumptions" part of the answer, then check the final numbers with the IRD or a tax advisor before you file.

---

## For developers

## Layout
- `SKILL.md` — skill entry point (YAML frontmatter + workflow)
- `references/` — rates, WHT, deadlines, filing, changes, scenarios, glossary (loaded on demand)
- `scripts/lk_tax_calc.py` — annual tax & monthly APIT calculator (Python 3, no dependencies)
- `chatgpt/custom-gpt-instructions.md` — setup for a Custom GPT

## Install
- **Claude Code:** copy this folder to `~/.claude/skills/lk-personal-tax/` (or `.claude/skills/` in a project).
- **Claude.ai:** zip the folder (SKILL.md at the zip root folder) and upload under Settings → Capabilities → Skills.
- **ChatGPT:** follow `chatgpt/custom-gpt-instructions.md`.

## Calculator
```bash
python3 scripts/lk_tax_calc.py annual --ya 2025/26 --employment 3600000 --apit-paid 156000 --interest 400000 --ait-paid 40000
python3 scripts/lk_tax_calc.py apit --monthly 350000
```

## Maintenance
Update `YA_TABLES` in the script and `references/` after each November Budget / Amendment Act, then bump the snapshot date in `SKILL.md`. Items marked "confirm" (penalty amounts, 2023/24 slabs, WHT thresholds) were not verified against the gazette.
