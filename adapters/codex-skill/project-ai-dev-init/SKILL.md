---
name: project-ai-dev-init
description: Initialize a real project with an agent-agnostic `.ai-dev` development framework. Use when the user wants to add Codex/Claude shared instructions, external wiki pointers, runtime flow and contract context, full/assisted/quick workflows, gates, MCP notes, and report templates to a target repository without modifying existing skills.
---

# Project AI Dev Init

Use this skill to bootstrap a business repository with the latest AI development framework.

It creates a project-local `.ai-dev/` framework plus `AGENTS.md` and `CLAUDE.md`. It does not change existing skills and does not write secrets.

## Run

From this skill directory:

```bash
python3 scripts/init_project_ai_dev.py --project /path/to/project \
  --wiki-root /Users/apple/Desktop/caiqiyue-wiki \
  --apifox-project-id 8445839 \
  --default-mode quick-check
```

Modes:

- `feature-delivery`: AI-led full feature delivery.
- `assisted-development`: human-led development with AI review, tests, and reports.
- `quick-check`: small change with minimum scope, runtime, contract, test, and delivery evidence.

## What It Generates

- `AGENTS.md` for Codex.
- `CLAUDE.md` for Claude Code.
- `.ai-dev/instructions/agent-entry.md` as the shared entrypoint.
- `.ai-dev/context/` for knowledge pointers and project rules.
- `.ai-dev/context/runtime/` for runtime flow knowledge.
- `.ai-dev/context/contracts/` for API, data, business, error, permission, and compatibility contracts.
- `.ai-dev/harness/workflows/` for full, assisted, and quick modes.
- `.ai-dev/harness/gates/` for requirement, runtime, contract, review, test, delivery, and state gates.
- `.ai-dev/mcp/` with Codex and Claude examples, without secrets.
- `.ai-dev/templates/` and `.ai-dev/runs/`.

## Rules

- Do not write tokens or API keys into the target repository.
- If target `AGENTS.md` or `CLAUDE.md` already exists, append the new entry unless `--force` is used.
- Prefer `quick-check` for small manual changes and `feature-delivery` for larger requirements.
- After initialization, ask the user to review `.ai-dev/context/knowledge-sources.md` and `.ai-dev/context/tool-bindings.md`.
