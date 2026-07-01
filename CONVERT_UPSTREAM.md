# Converting Upstream Academic Research Skills to Hermes

This file is the maintainer runbook for reproducing this adaptation when upstream changes.

## Current adaptation baseline

- Upstream repository: https://github.com/Imbad0202/academic-research-skills
- Upstream commit: `96e4f98b6e7a8b59be3f062bf854b0499e02b092`
- Upstream date: 2026-07-01
- Upstream suite version: `3.13.0`
- Adaptation output: four Hermes skills under `research/`

## Design intent

The upstream project is Claude Code-native. This repository is a Hermes Agent distribution of the same academic workflows. The adaptation should preserve research/writing/review behavior and academic integrity gates while removing or clearly marking Claude-only runtime assumptions.

The desired result is reproducible, but not a byte-for-byte mirror of upstream.

## Skill set

Always adapt these four upstream skill directories:

| Upstream directory | Hermes skill | Current upstream version |
| --- | --- | --- |
| `deep-research/` | `research/deep-research/` | 2.11.0 |
| `academic-paper/` | `research/academic-paper/` | 3.2.0 |
| `academic-paper-reviewer/` | `research/academic-paper-reviewer/` | 1.10.0 |
| `academic-pipeline/` | `research/academic-pipeline/` | 3.13.0 |

Do not adapt upstream `.claude-plugin/`, `commands/`, `hooks/`, or `skills/` symlink directory as Hermes skills in the default distribution.

## Conversion rules

### 1. Repository layout

Create this shape:

```text
README.md
LICENSE
NOTICE.md
ATTRIBUTION.md
CONVERT_UPSTREAM.md
research/
  deep-research/
    SKILL.md
    references/
    templates/
  academic-paper/
    SKILL.md
    references/
    templates/
  academic-paper-reviewer/
    SKILL.md
    references/
    templates/
  academic-pipeline/
    SKILL.md
    references/
    templates/
    scripts/        # only upstream scripts referenced by that skill tree
scripts/
  convert_upstream.py
```

The old Hermes adaptation used the same `research/<skill>/` installation shape. Keep it unless Hermes standards change.

### 2. Frontmatter normalization

Upstream frontmatter stores version-like fields under `metadata`. Hermes should use top-level fields:

```yaml
---
name: deep-research
title: Deep Research — Universal Academic Research Agent Team
description: Use when ...
version: 2.11.0
author: Hermes Agent adaptation based on Cheng-I Wu's Academic Research Skills
license: CC-BY-NC-4.0
metadata:
  hermes:
    category: research
    tags: [...]
    related_skills: [...]
    requires_toolsets: [file, search, web, browser, todo, delegation]
    homepage: https://github.com/Imbad0202/academic-research-skills
  source_repository: https://github.com/Imbad0202/academic-research-skills
  source_commit: <git-sha>
  source_suite_version: <plugin-version>
  source_skill: <upstream-dir>
  upstream_version: <upstream metadata.version>
  upstream_last_updated: <upstream metadata.last_updated>
  data_access_level: <upstream metadata.data_access_level>
  task_type: <upstream metadata.task_type>
  adaptation_note: Adapted to Hermes skill conventions; Claude Code plugin commands, hooks, and model routing are not installed.
---
```

Description should be concise and start with `Use when ...`. Move long trigger lists into the body.

### 3. Body preamble

Insert a Hermes adaptation section immediately after frontmatter and before upstream content:

- state source repository and commit;
- state that this is not a Claude Code plugin;
- state that Claude commands/hooks/model routing are not installed;
- state that upstream agents are preserved as `references/agents/*.md`;
- state that shared protocols are vendored under `references/shared/`;
- preserve human-in-the-loop source verification and academic integrity gates.

### 4. Agents

Upstream per-skill `agents/` directories are prompt assets, not Hermes runtime agent registrations.

Convert:

```text
<skill>/agents/*.md
```

to:

```text
research/<skill>/references/agents/*.md
```

Then rewrite body links from `agents/...` to `references/agents/...` where needed.

### 5. Shared materials

Vendor upstream `shared/` into every skill:

```text
research/<skill>/references/shared/
```

This duplicates files, but it keeps each skill self-contained after installation into `~/.hermes/skills/research/<skill>/`.

Add:

```text
research/<skill>/references/shared-index.md
```

with a list of vendored shared files.

### 6. Templates and references

Copy upstream per-skill `references/` and `templates/` as-is unless a file is purely Claude plugin maintenance. Prefer retaining academic workflow references over pruning aggressively.

### 7. Scripts

Do not blindly copy all upstream root `scripts/` files. For each skill, scan that skill's Markdown files for references to `scripts/<name>.py`. Copy only existing referenced upstream root scripts into:

```text
research/<skill>/scripts/<name>.py
```

Preserve nested script paths such as `scripts/cross_model_verification/normalize_compat_verdict.py`.

This keeps linked validation helpers available while avoiding a giant unrelated script dump.

### 8. Claude-only surfaces

Do not install these as Hermes features by default:

- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `commands/ars-*.md`
- `hooks/hooks.json`
- PreToolUse guards
- Claude `model: opus/sonnet/inherit` routing
- upstream `skills/` symlinks

If a future adaptation wants `/ars-*` aliases, add them deliberately as separate Hermes skills or a Hermes-native command mechanism, not by copying Claude command files verbatim.

### 9. Link rewriting

Common rewrites:

- `shared/...` -> `references/shared/...`
- `shared/references/...` -> `references/shared/references/...`
- `agents/...` -> `references/agents/...`
- `.claude/CLAUDE.md` routing references -> `references/shared/references/intent_clarification_protocol.md` or a Hermes adaptation note

After rewriting, run a link check or at least grep for stale `.claude`, `.claude-plugin`, `commands/ars`, and `hooks/` references in active `SKILL.md` files.

### 10. License and attribution

Copy upstream `LICENSE` and `NOTICE.md`. Keep `ATTRIBUTION.md` with upstream repository, author, commit, suite version, and license.

Do not relicense as MIT. The upstream material is CC BY-NC 4.0.

## Known issues and decisions

### Issue: Claude slash commands do not map directly to Hermes

Upstream has `/ars-*` command files. Hermes skills are already callable by skill name, but fine-grained command aliases are not automatically created from Markdown command files.

Decision: ship four skills only. Keep mode selection inside the skill bodies. Revisit aliases later if users ask.

### Issue: Claude hooks and write guards are not installed

Upstream includes hook-related safety mechanisms. Hermes has different tool approval and safety systems.

Decision: preserve the safety principles in text, but do not claim hook enforcement.

### Issue: upstream agent prompts are not first-class Hermes agents

Decision: keep them as reference role prompts under `references/agents/`. A Hermes agent may load them and use `delegate_task` manually when useful.

### Issue: duplicated shared files increase repository size

Decision: duplicate shared files per skill for self-contained installation. This matches the obsolete Hermes adaptation style and avoids broken links after users copy only selected skill folders.

### Issue: upstream descriptions are too long

Decision: use concise Hermes descriptions in frontmatter. Keep full trigger detail in body.

## Update checklist

1. Clone or fetch upstream:
   ```bash
   git -C /var/lib/hermes/workspace/git/academic-research-skills fetch --all --prune
   git -C /var/lib/hermes/workspace/git/academic-research-skills pull --ff-only
   ```
2. Record upstream commit and suite version from `.claude-plugin/plugin.json`.
3. Compare upstream skill versions and changed files:
   ```bash
   git -C /path/to/upstream diff --stat <old-commit>..HEAD -- deep-research academic-paper academic-paper-reviewer academic-pipeline shared
   ```
4. Re-run or manually apply the conversion rules above into a temporary directory.
5. Compare temporary output with this repository.
6. Preserve Hermes README/ATTRIBUTION/CONVERT_UPSTREAM decisions unless intentionally changed.
7. Validate SKILL.md files:
   - frontmatter starts at byte 0;
   - YAML parses;
   - `name`, `description`, `version`, `author`, `license`, `metadata.hermes.tags` exist;
   - description is concise;
   - linked files live under `references/`, `templates/`, `scripts/`, or `assets/`;
   - no active instructions imply Claude plugin installation in Hermes.
8. Update this file's baseline commit/version table.
9. Commit with a message like:
   ```text
   chore: port academic-research-skills vX.Y.Z to Hermes
   ```

## Validation commands used for this adaptation

```bash
python - <<'PY'
from pathlib import Path
import yaml
root = Path('research')
for skill in sorted(root.glob('*/SKILL.md')):
    text = skill.read_text()
    assert text.startswith('---'), skill
    end = text.index('
---', 3)
    fm = yaml.safe_load(text[3:end])
    for key in ['name', 'description', 'version', 'author', 'license', 'metadata']:
        assert key in fm, (skill, key)
    assert 'hermes' in fm['metadata'], skill
    assert len(fm['description']) <= 1024, skill
    print(skill, fm['version'])
PY
```
