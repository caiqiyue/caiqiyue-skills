#!/usr/bin/env python3
"""Create and inspect external-feature-flow run archives."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


PHASE_FILES = {
    "00-input": {
        "requirement.md": "# Requirement\n\n## Source\n\n## Raw Requirement\n\n## Notes\n",
        "source-links.md": "# Source Links\n\n- Requirement source:\n- Yuque:\n- Codeup work item:\n- Local files:\n",
    },
    "01-requirement-review": {
        "requirement-summary.md": "# Requirement Summary\n\n## Goal\n\n## Scope\n\n## Non-Goals\n",
        "acceptance-criteria.md": "# Acceptance Criteria\n\n- [ ] \n",
        "open-questions.md": "# Open Questions\n\n## Blocking\n\n## Non-Blocking\n",
        "spec-flow-analysis.md": "# Spec Flow Analysis\n\n## User Flows\n\n## Gaps\n\n## Questions\n",
        "openspec-change.md": "# OpenSpec Change\n\n## Change ID\n\n## Files\n\n## Validation\n",
    },
    "02-context": {
        "code-map.md": "# Code Map\n\n## Related Files\n\n## Existing Patterns\n\n## Evidence\n",
        "graphify-notes.md": "# Graphify Notes\n\n## Commands\n\n## Findings\n\n## Graph Freshness\n",
        "affected-nodes.md": "# Affected Nodes\n\n## Nodes\n\n## Paths\n\n## Impact\n",
        "apifox-contract.md": "# Apifox Contract\n\n## Project\n\n## Endpoints\n\n## Request/Response\n\n## Sync Need\n",
        "codeup-context.md": "# Codeup Context\n\n## Repository\n\n## Branch/MR/Work Item\n\n## Pipeline\n\n## Permission Notes\n",
        "docs-references.md": "# Documentation References\n\n## Context7\n\n## Official Docs\n\n## Local Docs\n",
    },
    "03-design": {
        "design.md": "# Design\n\n## Approach\n\n## Runtime Behavior\n\n## Static Links\n\n## Data/API Impact\n",
        "risks.md": "# Risks\n\n## Technical\n\n## Product\n\n## Operational\n",
        "compatibility.md": "# Compatibility\n\n## API\n\n## Data\n\n## Permissions\n\n## Rollback\n",
    },
    "04-plan": {
        "plan.md": "# Implementation Plan\n\n## Tasks\n\n- [ ] \n",
        "atomic-tasks.md": "# Atomic Tasks\n\n| ID | Goal | Files | Test | Status |\n|---|---|---|---|---|\n",
        "skill-routing.md": "# Skill Routing\n\n| Phase | Skill/CLI | Output | Archive |\n|---|---|---|---|\n",
    },
    "05-implementation": {
        "changed-files.md": "# Changed Files\n\n## Files\n\n## Reason\n",
        "debug.md": "# Debug Notes\n\n## Observations\n\n## Hypotheses\n\n## Experiments\n\n## Conclusion\n",
        "task-progress.md": "# Task Progress\n\n| Task | Status | Evidence |\n|---|---|---|\n",
    },
    "06-tests": {
        "test-plan.md": "# Test Plan\n\n## Unit\n\n## Integration\n\n## API\n\n## E2E\n\n## Manual\n",
        "verification-report.md": "# Verification Report\n\n## Commands\n\n## Results\n\n## Failures Fixed\n\n## Skipped/Risk\n",
    },
    "07-review": {
        "ocr-review.md": "# Open Code Review\n\n## Command\n\n## Findings\n\n## Fixes\n",
        "gsd-code-review.md": "# GSD Code Review\n\n## Command\n\n## Findings\n",
        "gstack-review.md": "# GStack Review\n\n## Command\n\n## Findings\n",
        "fixes.md": "# Review Fixes\n\n## Fixed\n\n## Accepted Risk\n",
    },
    "08-delivery": {
        "git-summary.md": "# Git Summary\n\n## Branch\n\n## Status\n\n## Diff\n",
        "commit-message.md": "# Commit Message\n\n```text\n\n```\n",
        "mr-description.md": "# MR Description\n\n## Summary\n\n## Test Evidence\n\n## Risk\n",
        "release-note.md": "# Release Note\n\n## User Impact\n\n## Operator Notes\n",
    },
    "09-knowledge": {
        "graphify-update.md": "# Graphify Update\n\n## Command\n\n## Result\n",
        "learnings.md": "# Learnings\n\n## Reusable Knowledge\n\n## Project Pattern\n",
        "wiki-follow-up.md": "# Wiki Follow-Up\n\n## Should Update\n\n## Suggested Content\n",
    },
}

EXTRA_DIRS = [
    "06-tests/test-scripts",
    "06-tests/test-evidence",
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug[:48] or "feature"


def run_command(args: list[str], cwd: Path) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd),
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return completed.returncode, completed.stdout.strip()
    except FileNotFoundError:
        return 127, f"{args[0]} not found"


def detect_tools(project: Path) -> dict[str, object]:
    tools = {}
    for name in [
        "openspec",
        "gsd-tools",
        "graphify",
        "ocr",
        "git",
        "node",
        "npm",
        "pnpm",
        "python3",
    ]:
        tools[name] = bool(shutil.which(name))

    git_code, git_out = run_command(["git", "rev-parse", "--is-inside-work-tree"], project)
    branch_code, branch_out = run_command(["git", "branch", "--show-current"], project)
    tools["gitRepository"] = git_code == 0 and git_out == "true"
    tools["gitBranch"] = branch_out if branch_code == 0 else ""

    env_keys = [
        "APIFOX_ACCESS_TOKEN",
        "APIFOX_PROJECT_ID",
        "YUNXIAO_ACCESS_TOKEN",
        "YUNXIAO_API_BASE_URL",
    ]
    tools["env"] = {key: bool(os.environ.get(key)) for key in env_keys}
    return tools


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def init_run(args: argparse.Namespace) -> Path:
    project = Path(args.project).expanduser().resolve()
    if not project.exists():
        raise SystemExit(f"Project path does not exist: {project}")

    title = args.title.strip() if args.title else "Feature"
    task_id = args.task_id.strip() if args.task_id else f"{datetime.now():%Y-%m-%d}-{slugify(title)}"
    task_id = slugify(task_id)

    run_dir = project / ".external-feature" / "runs" / task_id
    run_dir.mkdir(parents=True, exist_ok=True)

    for phase, files in PHASE_FILES.items():
        phase_dir = run_dir / phase
        phase_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            write_if_missing(phase_dir / filename, content)

    for rel_dir in EXTRA_DIRS:
        (run_dir / rel_dir).mkdir(parents=True, exist_ok=True)

    if args.requirement_file:
        requirement_path = Path(args.requirement_file).expanduser().resolve()
        if not requirement_path.exists():
            raise SystemExit(f"Requirement file does not exist: {requirement_path}")
        raw = requirement_path.read_text(encoding="utf-8")
        (run_dir / "00-input" / "requirement.md").write_text(
            "# Requirement\n\n"
            f"## Source\n\n{requirement_path}\n\n"
            "## Raw Requirement\n\n"
            f"{raw}\n",
            encoding="utf-8",
        )

    tools = detect_tools(project)
    metadata = {
        "taskId": task_id,
        "title": title,
        "project": str(project),
        "createdAt": datetime.now().isoformat(timespec="seconds"),
        "toolAvailability": tools,
    }
    (run_dir / "run.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    index = f"""# External Feature Run

## Metadata

- Task id: `{task_id}`
- Title: {title}
- Project: `{project}`
- Created at: {metadata["createdAt"]}

## Current Phase

- [ ] 00 Input
- [ ] 01 Requirement Review
- [ ] 02 Context
- [ ] 03 Design
- [ ] 04 Plan
- [ ] 05 Implementation
- [ ] 06 Tests
- [ ] 07 Review
- [ ] 08 Delivery
- [ ] 09 Knowledge
- [ ] Final Report

## Tool Availability

```json
{json.dumps(tools, indent=2, ensure_ascii=False)}
```
"""
    write_if_missing(run_dir / "index.md", index)

    final_report = """# Final Report

## Summary

## Requirement

## Design

## Changed Files

## Test Evidence

## Review Evidence

## Git / Codeup Delivery

## Apifox Sync

## Knowledge Follow-Up

## Residual Risk
"""
    write_if_missing(run_dir / "final-report.md", final_report)

    return run_dir


def show_run(args: argparse.Namespace) -> None:
    project = Path(args.project).expanduser().resolve()
    run_root = project / ".external-feature" / "runs"
    if not run_root.exists():
        print(f"No runs found under {run_root}")
        return
    for path in sorted(run_root.iterdir()):
        if path.is_dir():
            print(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage external-feature-flow run archives.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a feature run archive.")
    init.add_argument("--project", default=".", help="Existing project path.")
    init.add_argument("--task-id", default="", help="Run id. Defaults to date plus title slug.")
    init.add_argument("--title", default="Feature", help="Human-readable feature title.")
    init.add_argument("--requirement-file", default="", help="Optional PRD or requirement file.")
    init.set_defaults(func=lambda parsed: print(init_run(parsed)))

    runs = sub.add_parser("list", help="List existing feature runs.")
    runs.add_argument("--project", default=".", help="Existing project path.")
    runs.set_defaults(func=show_run)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
