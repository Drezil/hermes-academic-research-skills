# Hermes Academic Research Skills

A Hermes Agent-compatible adaptation of [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu.

- Upstream suite version: `3.19.0`
- Upstream commit: `2cf3a51e159458b7a8c8784bb874248e79601f7b` (2026-07-30)
- Skills: `hermes-deep-research`, `hermes-academic-paper`, `hermes-academic-paper-reviewer`, `hermes-academic-pipeline`

Skills are prefixed `hermes-` to avoid collision with the upstream Claude Code version on skills.sh.

## Installation

```bash
# Clone and install
git clone https://github.com/Drezil/hermes-academic-research-skills.git /tmp/hermes-academic-skills
cp -r /tmp/hermes-academic-skills/skills/research/* ~/.hermes/skills/research/

# Register tap for future updates
hermes skills tap add Drezil/hermes-academic-research-skills
```

## Cross-Model Verification → Hermes MoA

The upstream cross-model verification feature (sending paper content to external LLM APIs
with separate API keys) is **not included**. In Hermes, use the built-in
**Mixture of Agents (MoA)** model:

```bash
hermes config set moa.enabled true
```

See `CONVERT_UPSTREAM.md` for the full reproducible conversion runbook.
