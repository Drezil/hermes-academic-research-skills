# Hermes Academic Research Skills

A Hermes Agent-compatible adaptation of [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu.

This repository is intended to be shared as a reproducible Hermes adaptation, not as a Claude Code plugin fork. It tracks how upstream Claude Code skills were converted into Hermes `SKILL.md` folders.

## Included skills

- `deep-research` — rigorous academic research, literature review, fact-checking, PRISMA/systematic review workflows.
- `academic-paper` — paper planning, outlining, drafting, revision, citation checking, formatting, disclosure, and rebuttal support.
- `academic-paper-reviewer` — simulated peer review, methodology-focused review, re-review, guided review, and calibration modes.
- `academic-pipeline` — full research-to-publication orchestration across research, writing, integrity checks, review, revision, and finalization.

## Source and version

- Upstream repository: https://github.com/Imbad0202/academic-research-skills
- Upstream suite version: `3.13.0`
- Upstream commit used here: `96e4f98b6e7a8b59be3f062bf854b0499e02b092` (2026-07-01)
- License: CC BY-NC 4.0. See `LICENSE`, `NOTICE.md`, and `ATTRIBUTION.md`.

## What was adapted

- Converted upstream Claude Code skill frontmatter into Hermes-style top-level metadata.
- Preserved the four-skill suite layout under `research/`.
- Re-homed upstream per-skill `agents/` into `references/agents/` because Hermes skills expose reference files, not Claude Code agent registrations.
- Vendored upstream `shared/` materials into each skill under `references/shared/` so each skill is self-contained.
- Added `references/shared-index.md` files for discoverability.
- Copied only upstream root `scripts/*.py` files referenced from each skill tree into that skill's `scripts/` directory.
- Removed or reframed Claude Code plugin assumptions: plugin marketplace install, slash command registration, PreToolUse hooks, and Claude model routing are not installed by this Hermes adaptation.

## Hermes metadata policy

The active `SKILL.md` files are intentionally not 1:1 copies of the Claude Code originals. Their frontmatter is normalized for Hermes discovery and loading:

- `version` is promoted to a top-level field instead of living under upstream `metadata.version`.
- `description` is shortened to a concise `Use when ...` trigger sentence; upstream's long trigger/mode lists remain in the body.
- Hermes-specific fields live under `metadata.hermes`, including `category`, `tags`, `related_skills`, `requires_toolsets`, and `homepage`.
- Upstream provenance is preserved separately with `source_repository`, `source_commit`, `source_suite_version`, `source_skill`, `upstream_version`, and `upstream_last_updated`.
- Claude Code-only frontmatter and runtime surfaces (`allowed-tools`, `argument-hint`, `model: opus/sonnet/inherit`, plugin commands, hooks) are not carried over as Hermes metadata.

## Claude Code compatibility caveat

The four active `SKILL.md` entrypoints are Hermes-facing. Vendored `references/`, `examples/`, `templates/`, and `scripts/` preserve upstream material and may still mention Claude Code, `/ars-*`, or PreToolUse hooks as historical/upstream context. Those references do not mean this repository installs Claude plugin behavior in Hermes.

## Install into Hermes

From this repository root:

```bash
mkdir -p ~/.hermes/skills/research
cp -R research/* ~/.hermes/skills/research/
```

Then start a fresh Hermes session or run `/reload-skills`, and verify:

```bash
hermes skills list | grep -E 'deep-research|academic-paper|academic-paper-reviewer|academic-pipeline'
```

No skill is installed automatically by this repository.

## Updating from upstream

Read `CONVERT_UPSTREAM.md` first. The goal is not a blind copy: upstream is Claude Code-native, so updates must be ported through the documented conversion rules.

Short version:

1. Fetch upstream.
2. Compare upstream versions and changed files.
3. Reapply the frontmatter/layout conversion.
4. Preserve Hermes-only README/license/attribution/update notes.
5. Validate all `SKILL.md` files before release.

## Non-goals

- This repository does not implement Claude Code plugin installation.
- This repository does not register `/ars-*` slash command aliases in Hermes.
- This repository does not install Claude hooks or PreToolUse guards.
- This repository does not claim automatic first-class Hermes subagent registration for upstream agent prompt files.

Those features can be designed later, but the first adaptation keeps the surface simple and reliable: four Hermes skills plus linked references/templates.
