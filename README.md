# lk-personal-tax

Sri Lanka personal income tax assistant as an agent skill (Claude) and a Custom GPT (ChatGPT). Rules snapshot: **October 2026**.

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
