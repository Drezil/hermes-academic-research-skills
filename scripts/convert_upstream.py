#!/usr/bin/env python3
"""Convert Imbad0202/academic-research-skills into a Hermes skill repository.

Usage:
    python scripts/convert_upstream.py /path/to/academic-research-skills /path/to/output

The output directory must not already exist. The script creates the same basic
shape as this repository: repository docs plus four skills under research/.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import json
import re
import shutil
import subprocess

SKILLS = {
    "hermes-deep-research": {
        "title": "Deep Research — Universal Academic Research Agent Team",
        "description": "Use when exploring research questions, building literature reviews, fact-checking claims, or running systematic/PRISMA-style academic research workflows.",
        "tags": ["research", "academic", "literature-review", "systematic-review", "prisma", "fact-checking", "socratic"],
        "related": ["academic-paper", "academic-paper-reviewer", "academic-pipeline", "arxiv"],
    },
    "hermes-academic-paper": {
        "title": "Academic Paper — Academic Paper Writing Agent Team",
        "description": "Use when planning, outlining, drafting, revising, formatting, citation-checking, or preparing disclosure/rebuttal material for academic papers.",
        "tags": ["academic", "writing", "paper", "citations", "latex", "pandoc", "revision"],
        "related": ["deep-research", "academic-paper-reviewer", "academic-pipeline"],
    },
    "hermes-academic-paper-reviewer": {
        "title": "Academic Paper Reviewer — Multi-Perspective Review Team",
        "description": "Use when reviewing manuscripts, simulating peer review, checking revisions, focusing on methodology, or calibrating reviewer-style critique.",
        "tags": ["academic", "peer-review", "manuscript", "methodology", "reviewer", "critique"],
        "related": ["academic-paper", "academic-pipeline", "deep-research"],
    },
    "hermes-academic-pipeline": {
        "title": "Academic Pipeline — Research-to-Publication Orchestrator",
        "description": "Use when coordinating the full research-to-publication workflow from research through drafting, integrity checks, review, revision, and finalization.",
        "tags": ["academic", "pipeline", "orchestration", "research", "writing", "review", "integrity"],
        "related": ["deep-research", "academic-paper", "academic-paper-reviewer"],
    },
}
REQUIRES = ["file", "search", "web", "browser", "todo", "delegation"]


def git_out(cwd: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(cwd), *args], text=True).strip()


def split_frontmatter(text: str):
    """Parse just the upstream frontmatter fields this converter needs.

This intentionally avoids a PyYAML dependency so the converter works on a plain
Python installation. It is not a general YAML parser.
    """
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end]
    body = text[text.find("\n", end + 4) + 1:]
    fm = {}
    meta = {}
    for key in ["name", "version", "description"]:
        m = re.search(rf"(?m)^{key}:\s*(.+?)\s*$", raw)
        if m:
            fm[key] = m.group(1).strip().strip('"')
    for key in ["version", "last_updated", "data_access_level", "task_type"]:
        m = re.search(rf"(?m)^\s+{key}:\s*(.+?)\s*$", raw)
        if m:
            meta[key] = m.group(1).strip().strip('"')
    if meta:
        fm["metadata"] = meta
    return fm, body


def clean(obj):
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, list):
        return [clean(v) for v in obj]
    return obj


def _yaml_scalar(value) -> str:
    if isinstance(value, str):
        if value == "" or any(ch in value for ch in [":", "#", "{", "}", "[", "]", "\n", "'", '"']):
            return repr(value)
        return value
    return str(value).lower() if isinstance(value, bool) else str(value)


def _yaml_lines(obj, indent: int = 0):
    sp = " " * indent
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                yield f"{sp}{k}:"
                yield from _yaml_lines(v, indent + 2)
            else:
                yield f"{sp}{k}: {_yaml_scalar(v)}"
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                yield f"{sp}-"
                yield from _yaml_lines(item, indent + 2)
            else:
                yield f"{sp}- {_yaml_scalar(item)}"


def dump_frontmatter(fm: dict) -> str:
    return "---\n" + "\n".join(_yaml_lines(fm)) + "\n---\n\n"


def rewrite_body(body: str, skill_name: str, title: str, short_commit: str, commit_date: str) -> str:
    body = re.sub(r"\n?> \*\*Routing discipline.*?\n", "\n", body)
    body = body.replace("shared/references/", "references/shared/references/")
    body = body.replace("`shared/", "`references/shared/")
    body = body.replace("](shared/", "](references/shared/")
    body = body.replace("agents/", "references/agents/")
    body = body.replace("Invoke in a *fresh* Claude Code session.", "Invoke in a *fresh* Hermes session.")
    body = body.replace("runs the full reviewer panel standalone via `/ars-review` equivalent.", "runs the full reviewer panel standalone via `academic-paper-reviewer` full mode.")
    body = re.sub(
        r"Routing into Mode B requires explicit user signal — `/ars-<mode>` slash command or `\[direct-mode\]` prefix\. Ambiguous cross-phase input defaults to clarification per `\.claude/CLAUDE\.md` Routing Discipline \+ `references/shared/references/intent_clarification_protocol\.md`\.?",
        "Routing into Mode B requires an explicit user signal, such as naming the desired mode or using a `[direct-mode]` prefix. Ambiguous cross-phase input defaults to clarification using `references/shared/references/intent_clarification_protocol.md`.",
        body,
    )
    body = re.sub(
        r"\*\*Enforcement \(v3\.9\.2\):\*\* prompt-level via Phase Boundary blocks on (?:downstream )?Bucket A agents \+ advisory verifier \(`scripts/check_pipeline_integrity\.py`\)\. Deterministic PreToolUse hook \+ multi-phase envelope(?: \+ orchestrator structured intake)? deferred to v3\.10 active conductor \(#134\)\.",
        "**Enforcement (v3.9.2):** prompt-level via Phase Boundary blocks on upstream Bucket A agents. The Claude Code PreToolUse hook mentioned upstream is not installed in this Hermes adaptation; treat the phase boundary as a workflow rule and verify manually or with referenced scripts when available.",
        body,
    )
    body = re.sub(r"^# .+?\n\n", "", body, count=1)
    preamble = f"""# {title}

## Hermes Adaptation Notes

This is a Hermes Agent adaptation of upstream `{skill_name}` from
`Imbad0202/academic-research-skills` at commit `{short_commit}` ({commit_date}).

- Use this as a Hermes skill, not as a Claude Code plugin.
- Claude Code plugin commands, hooks, and model-routing frontmatter are not installed by this adaptation.
- Shared upstream protocols are vendored under `references/shared/`.
- Keep human-in-the-loop academic integrity gates: verify sources, cite evidence, and ask for confirmation at workflow boundaries.
- **Cross-model verification is NOT supported.** The upstream cross-model feature (`ARS_CROSS_MODEL`, `cross_model_verification.md`) sends paper content to external LLM APIs with separate API keys — a Claude Code workaround replaced in Hermes by the built-in **Mixture of Agents (MoA)** model (`hermes config set moa.enabled true`). References to cross-model features in the body describe upstream-only functionality.

## Safety in Hermes

This adaptation removes upstream Claude Code safety hooks. Use Hermes' built-in equivalents:

- **Write protection** (replaces upstream file protection hooks): Before modifying any file outside the current working directory, ask the user via `clarify()`. Respect `AGENTS.md` rules in the project root.
- **Human acknowledgement** (replaces upstream mark-read hooks): When you produce findings or decisions that need user sign-off, present them via `clarify()` and WAIT for the user response. Do not auto-advance past integrity checkpoints.
- **Integrity verification**: Run relevant `scripts/check_*.py` validators before presenting findings as confirmed. On failure, report to the user and ask whether to proceed.

## When to Use

See the trigger and mode-selection sections below. Prefer this skill when the user's task matches its academic workflow; use the linked references only when needed to avoid loading unnecessary context.

"""
    return preamble + body.lstrip()


def copy_referenced_scripts(upstream: Path, skilldir: Path) -> list[str]:
    refs: set[str] = set()
    for md in skilldir.rglob("*.md"):
        txt = md.read_text(errors="replace")
        refs.update(re.findall(r"`scripts/([^`]+?\.py)`", txt))
        refs.update(re.findall(r"\(scripts/([^\)]+?\.py)\)", txt))
        refs.update(re.findall(r"scripts/([A-Za-z0-9_./-]+?\.py)", txt))
    copied = []
    for rel in sorted(refs):
        source = upstream / "scripts" / rel
        if source.exists() and source.is_file():
            target = skilldir / "scripts" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            copied.append(rel)
    return copied


def strip_cross_model(skilldir: Path) -> None:
    """Remove cross-model verification scripts incompatible with Hermes."""
    for pattern in ["cross_model_handoff.py", "check_benchmark_report.py",
                   "test_cross_model_handoff.py", "test_normalize_compat_verdict.py"]:
        p = skilldir / "scripts" / pattern
        if p.exists():
            p.unlink()
    cm_dir = skilldir / "scripts" / "cross_model_verification"
    if cm_dir.exists() and cm_dir.is_dir():
        shutil.rmtree(cm_dir)
    # Catch any future cross-model scripts added by upstream
    for script in list((skilldir / "scripts").glob("cross_model*")):
        if script.is_file():
            script.unlink()
        elif script.is_dir():
            shutil.rmtree(script)


def strip_claude_only(skilldir: Path) -> None:
    """Remove Claude Code-specific content with no Hermes equivalent."""
    for name in ["ars_write_scope_guard.py", "ars_mark_read.py"]:
        p = skilldir / "scripts" / name
        if p.exists():
            p.unlink()
    # Rewrite CLAUDE.md references in vendored shared files
    ca = skilldir / "references" / "shared" / "agents" / "compliance_agent.md"
    if ca.exists():
        text = ca.read_text(encoding="utf-8")
        text = text.replace(
            "(per user CLAUDE.md: never haiku)",
            "(per model tiering policy)"
        )
        ca.write_text(text, encoding="utf-8")


def convert(upstream: Path, out: Path):
    if out.exists():
        raise SystemExit(f"Output already exists: {out}")
    out.mkdir(parents=True)
    commit = git_out(upstream, "rev-parse", "HEAD")
    short = commit[:7]
    date = git_out(upstream, "log", "-1", "--format=%cs")
    plugin_path = upstream / ".claude-plugin" / "plugin.json"
    suite_version = json.loads(plugin_path.read_text()).get("version", "unknown") if plugin_path.exists() else "unknown"

    shutil.copy2(upstream / "LICENSE", out / "LICENSE")
    if (upstream / "NOTICE.md").exists():
        shutil.copy2(upstream / "NOTICE.md", out / "NOTICE.md")
    (out / "ATTRIBUTION.md").write_text(f"""# Attribution

This repository is a Hermes Agent adaptation of Academic Research Skills by Cheng-I Wu / Imbad0202.

- Upstream repository: https://github.com/Imbad0202/academic-research-skills
- Upstream version at adaptation time: {suite_version}
- Upstream commit: `{commit}` ({date})
- Upstream license: CC BY-NC 4.0

See `LICENSE` and `NOTICE.md`.
""", encoding="utf-8")

    skills_out = out / "skills" / "research"
    skills_out.mkdir(parents=True)
    for name, spec in SKILLS.items():
        src_skill = upstream / name
        dst = skills_out / name
        dst.mkdir()
        for item in src_skill.iterdir():
            if item.name == "SKILL.md":
                continue
            if item.name == "agents" and item.is_dir():
                shutil.copytree(item, dst / "references" / "agents", dirs_exist_ok=True)
            elif item.is_dir():
                shutil.copytree(item, dst / item.name, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dst / item.name)
        if (upstream / "shared").exists():
            shutil.copytree(upstream / "shared", dst / "references" / "shared", dirs_exist_ok=True)
            # Filter out cross-model content incompatible with Hermes
            cross_model_doc = dst / "references" / "shared" / "cross_model_verification.md"
            if cross_model_doc.exists():
                cross_model_doc.unlink()
            shared_files = sorted(
                str(p.relative_to(dst / "references" / "shared"))
                for p in (dst / "references" / "shared").rglob("*")
                if p.is_file() and "cross_model" not in p.name
            )
            (dst / "references" / "shared-index.md").write_text(
                "# Shared Upstream Materials\n\n"
                + "\n".join(f"- `references/shared/{p}`" for p in shared_files)
                + "\n", encoding="utf-8"
            )
        fm, body = split_frontmatter((src_skill / "SKILL.md").read_text(encoding="utf-8"))
        meta = fm.get("metadata") or {}
        version = str(meta.get("version") or fm.get("version") or "unknown")
        out_fm = clean({
            "name": name,
            "title": spec["title"],
            "description": spec["description"],
            "version": version,
            "author": "Hermes Agent adaptation based on Cheng-I Wu's Academic Research Skills",
            "license": "CC-BY-NC-4.0",
            "metadata": {
                "hermes": {"category": "research", "tags": spec["tags"], "related_skills": spec["related"], "requires_toolsets": REQUIRES, "homepage": "https://github.com/Imbad0202/academic-research-skills"},
                "source_repository": "https://github.com/Imbad0202/academic-research-skills",
                "source_commit": commit,
                "source_suite_version": suite_version,
                "source_skill": name,
                "upstream_version": version,
                "upstream_last_updated": meta.get("last_updated"),
                "data_access_level": meta.get("data_access_level"),
                "task_type": meta.get("task_type"),
                "adaptation_note": "Adapted to Hermes skill conventions; Claude Code plugin commands, hooks, and model routing are not installed.",
            },
        })
        (dst / "SKILL.md").write_text(dump_frontmatter(out_fm) + rewrite_body(body, name, spec["title"], short, date), encoding="utf-8")
        copy_referenced_scripts(upstream, dst)
        strip_cross_model(dst)
        strip_claude_only(dst)

    (out / "README.md").write_text(f"""# Hermes Academic Research Skills

A Hermes Agent-compatible adaptation of [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu.

- Upstream suite version: `{suite_version}`
- Upstream commit: `{commit}` ({date})
- Skills: `deep-research`, `academic-paper`, `academic-paper-reviewer`, `academic-pipeline`

Install manually with:

```bash
mkdir -p ~/.hermes/skills/research
cp -R skills/research/* ~/.hermes/skills/research/
```

See `CONVERT_UPSTREAM.md` in the maintained repository for the full reproducible conversion runbook.
""", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("upstream", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    convert(args.upstream.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
