# Hermes Academic Research Skills

A Hermes Agent-compatible adaptation of [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu.

- Upstream suite version: `3.19.0`
- Upstream commit: `2cf3a51e159458b7a8c8784bb874248e79601f7b` (2026-07-30)
- Skills: `deep-research`, `academic-paper`, `academic-paper-reviewer`, `academic-pipeline`

Install via Hermes tap (recommended — auto-updates with `hermes skills update`):

```bash
hermes skills tap add hermes-academic https://github.com/Drezil/hermes-academic-research-skills
hermes skills install academic-paper academic-paper-reviewer academic-pipeline deep-research
```

Or install manually (legacy):

```bash
mkdir -p ~/.hermes/skills/research
cp -R research/* ~/.hermes/skills/research/
```

See `CONVERT_UPSTREAM.md` in the maintained repository for the full reproducible conversion runbook.
