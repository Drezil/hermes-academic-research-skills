# Hermes Academic Research Skills

A Hermes Agent-compatible adaptation of [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu.

- Upstream suite version: `3.19.0`
- Upstream commit: `2cf3a51e159458b7a8c8784bb874248e79601f7b` (2026-07-30)
- Skills: `hermes-deep-research`, `hermes-academic-paper`, `hermes-academic-paper-reviewer`, `hermes-academic-pipeline`

Skills are prefixed `hermes-` to avoid collision with the upstream Claude Code version on skills.sh.

## Installation

```bash
# Register the tap
hermes skills tap add Drezil/hermes-academic-research-skills

# SAFE — no --force needed
hermes skills install Drezil/hermes-academic-research-skills/skills/research/hermes-academic-paper-reviewer
hermes skills install Drezil/hermes-academic-research-skills/skills/research/hermes-deep-research

# CAUTION — needs --force (false positives on academic reference text, see below)
hermes skills install --force Drezil/hermes-academic-research-skills/skills/research/hermes-academic-paper
hermes skills install --force Drezil/hermes-academic-research-skills/skills/research/hermes-academic-pipeline
```

For updates: `hermes skills update`

## Why `--force` on some skills?

The Hermes security scanner flags false positives on academic reference content:

| Skill | Verdict | Findings | Reason |
|---|---|---|---|
| `hermes-academic-paper` | CAUTION | 2 HIGH | Writing templates describing paper formats and figure guidelines |
| `hermes-academic-pipeline` | CAUTION | 7 MEDIUM | Path references in adapter documentation |

These are academic writing guidelines and cross-reference links — not data exfiltration.
The scanner has no "academic reference" category and defaults to CAUTION.

## Why trust this adaptation?

This fork has been audited to remove all genuinely dangerous upstream content:

- ❌ **Cross-model verification** (sending paper content to external LLM APIs) — **removed**. Use Hermes' built-in MoA instead.
- ❌ **Claude Code hooks** (`ars_write_scope_guard.py`, `ars_mark_read.py`) — **removed**.
- ❌ **CLAUDE.md references** in agent prompts — **rewritten** to model-tiering policy.
- ❌ **External API key setup guides with curl examples** — **removed**.
- ❌ **Prompt injection examples** in agent safeguards — **rewritten** to abstract descriptions.

What remains: academic workflow tools — paper drafting, peer review simulation, research pipelines,
citation verification, and integrity checks. All Python validation scripts operate locally on your files.

The full conversion runbook is in `CONVERT_UPSTREAM.md`. Every upstream sync runs through
`scripts/convert_upstream.py` which automatically strips the above content.

## Cross-Model Verification → Hermes MoA

The upstream cross-model verification feature is **not included**. Use Hermes' built-in
**Mixture of Agents (MoA)** instead:

```bash
hermes config set moa.enabled true
```
