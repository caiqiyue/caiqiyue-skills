---
name: project-ai-dev-init
description: Initialize a real project with an agent-agnostic `.ai-dev` development framework. Use when the user wants to add Codex/Claude shared instructions, external wiki pointers, runtime flow and contract context, full/assisted/quick workflows, gates, MCP notes, and report templates to a target repository without modifying existing skills.
---

# Project AI Dev Init

Use this skill to bootstrap a business repository with the latest AI development framework.

It creates a project-local `.ai-dev/` framework plus `AGENTS.md` and `CLAUDE.md`. It does not copy global skills into the project, does not change existing skills, and does not write secrets.

## Initialize A Project

From this skill directory:

```bash
python3 scripts/init_project_ai_dev.py --project /path/to/project \
  --wiki-root /Users/apple/Desktop/caiqiyue-wiki \
  --apifox-project-id 8445839 \
  --default-mode quick-check \
  --depth standard
```

Use `--project` for the real project being developed. Use `--wiki-root` to point at the external/local knowledge base the project should borrow from.

## Modes

- `feature-delivery`: AI-led full feature delivery.
- `assisted-development`: human-led development with AI review, tests, and reports.
- `quick-check`: small change with minimum scope, runtime, contract, test, and delivery evidence.

## Depth

- `minimal`: generate the framework skeleton.
- `standard`: generate the skeleton and fill project profile, tool bindings, code map, test commands, and knowledge-source pointers.
- `deep`: standard plus broader runtime/contract candidate scanning. This still produces candidates, not truth.

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
- `.ai-dev/runs/init-YYYY-MM-DD/initialization-report.md` with detected facts, gaps, token presence booleans, and next steps.

## After Initialization

Before feature work, inspect and complete:

1. `.ai-dev/runs/init-YYYY-MM-DD/initialization-report.md`
2. `.ai-dev/context/knowledge-sources.md`
3. `.ai-dev/context/tool-bindings.md`
4. `.ai-dev/project-profile.md`
5. `.ai-dev/mcp/env.example`

Secrets belong in local secret files, not committed project files:

- Codex: `~/.codex/mcp-env.sh`
- Project-local private env, if needed: `.ai-dev/mcp/env.local` and add it to `.gitignore`
- Claude Code: local MCP env or secret configuration

Run a small connectivity check when MCP matters. Record results under:

```text
.ai-dev/runs/mcp-connectivity-YYYY-MM-DD/
```

Example outcomes to record:

- Apifox connected and returned an OpenAPI document.
- Codeup/Yunxiao token is present but missing organization-management permission.
- Yuque or DingTalk credentials are missing.

## Development Workflow After Init

For every requirement, create a task run:

```text
.ai-dev/runs/<task-id>/
  requirement-summary.md
  runtime-flow.md
  contract-checklist.md
  design.md
  development-plan.md
  bug-list.md
  test-report.md
  delivery-report.md
  tests/
    scripts/
    evidence/
```

Follow this order:

1. Read `AGENTS.md` or `CLAUDE.md`, then `.ai-dev/instructions/agent-entry.md`.
2. Read project profile, knowledge sources, local rules, code map, and tool bindings.
3. Select `feature-delivery`, `assisted-development`, or `quick-check`.
4. Summarize the requirement and open questions.
5. Map runtime flow and affected contracts before coding when API, data, permissions, or behavior may change.
6. Write design and development plan.
7. Implement scoped code changes.
8. Write or update reproducible test scripts.
9. Run compile/lint/unit/API/feature tests as relevant.
10. Save command outputs under `tests/evidence/`.
11. Update test report, delivery report, and harness state.
12. Prepare Apifox, Codeup, Yuque, or DingTalk handoff notes when relevant.

Testing cannot be claimed complete unless the run includes commands, script paths, inputs or fixtures, assertions, actual results, and any skipped-risk notes.

## Rules

- Do not write tokens or API keys into the target repository.
- If target `AGENTS.md` or `CLAUDE.md` already exists, append the new entry unless `--force` is used.
- Prefer `quick-check` for small manual changes and `feature-delivery` for larger requirements.
- After initialization, ask the user to review `.ai-dev/context/knowledge-sources.md` and `.ai-dev/context/tool-bindings.md`.
- Treat auto-detected runtime/contracts as candidates. Confirm against real code before relying on them during feature work.
- If MCP connectivity fails, record the exact non-secret error and the next required user action.
