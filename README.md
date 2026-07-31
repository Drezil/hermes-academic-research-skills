# Hermes Academic Research Skills

A Hermes Agent-compatible adaptation of [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu.

- Upstream suite version: `3.19.0`
- Upstream commit: `2cf3a51e159458b7a8c8784bb874248e79601f7b` (2026-07-30)
- Skills: `hermes-deep-research`, `hermes-academic-paper`, `hermes-academic-paper-reviewer`, `hermes-academic-pipeline`

## Installation

**Primary method — local copy:**

```bash
mkdir -p ~/.hermes/skills/research
cp -R skills/research/* ~/.hermes/skills/research/
```

**Future: Tap-based auto-updates** (requires Hermes scanner support for trusted taps):

```bash
hermes skills tap add Drezil/hermes-academic-research-skills
# Then install each skill from the tap (once scanner allows it):
hermes skills install hermes-academic-paper
hermes skills install hermes-academic-paper-reviewer
hermes skills install hermes-academic-pipeline
hermes skills install hermes-deep-research
# Updates: hermes skills update
```

> **Why not `hermes skills install` today?** The skills.sh registry resolves these skill names
> to the upstream `Imbad0202/academic-research-skills` repo (Claude Code plugin), which is
> blocked by Hermes' security scanner. Our tap (`Drezil/hermes-academic-research-skills`)
> provides the scanner-clean Hermes adaptation but `hermes skills install` always prefers
> skills.sh. Once Hermes supports tap-priority or trusted sources, the tap flow above replaces
> manual copies.

## Cross-Model Verification → Hermes MoA

The upstream cross-model verification feature (sending paper content to external LLM APIs
with separate API keys) is **not included** in this adaptation. In Hermes, use the built-in
**Mixture of Agents (MoA)** model instead:

```bash
hermes config set moa.enabled true
```

See `CONVERT_UPSTREAM.md` for the full reproducible conversion runbook.
