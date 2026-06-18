#!/usr/bin/env python3
"""Initialize a project-local .ai-dev framework.

This script is intentionally self-contained so the skill does not need to
modify or depend on existing skills in this repository.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
from pathlib import Path


TOKEN_KEYS = [
    "YUQUE_TOKEN",
    "DINGTALK_Client_ID",
    "DINGTALK_Client_Secret",
    "YUNXIAO_ACCESS_TOKEN",
    "APIFOX_ACCESS_TOKEN",
    "APIFOX_PROJECT_ID",
]


FILES: dict[str, str] = {
    "AGENTS.md": """# Project AI Development Entry

Before task work, read:

1. `.ai-dev/instructions/agent-entry.md`
2. `.ai-dev/project-profile.md`
3. `.ai-dev/context/constitution.md`
4. `.ai-dev/context/knowledge-sources.md`
5. `.ai-dev/context/local-rules.md`
6. The selected workflow under `.ai-dev/harness/workflows/`
7. The relevant gates under `.ai-dev/harness/gates/`

Hard rules:

- Do not claim completion before verification evidence exists.
- Design before implementation when runtime flow, contracts, data, or API behavior may change.
- Tests must include reproducible scripts or commands, inputs, assertions, and actual results.
- Do not print or commit secrets.
""",
    "CLAUDE.md": """# Project AI Development Entry

Claude Code follows the same project harness as Codex.

Before task work, read:

1. `.ai-dev/instructions/agent-entry.md`
2. `.ai-dev/project-profile.md`
3. `.ai-dev/context/constitution.md`
4. `.ai-dev/context/knowledge-sources.md`
5. `.ai-dev/context/local-rules.md`
6. The selected workflow under `.ai-dev/harness/workflows/`
7. The relevant gates under `.ai-dev/harness/gates/`

Hard rules:

- Do not claim completion before verification evidence exists.
- Design before implementation when runtime flow, contracts, data, or API behavior may change.
- Tests must include reproducible scripts or commands, inputs, assertions, and actual results.
- Do not print or commit secrets.
""",
    ".ai-dev/README.md": """# Project AI Development Harness

This directory is the project-local adapter for external wiki knowledge, harness workflows, skills, and MCP tools.

It stores constitution rules, context pointers, candidate runtime/static/contract maps, workflows, gates, run artifacts, templates, adapters, and MCP usage notes.

Initialization prepares containers and candidate maps only. Requirement-specific dynamic runtime flow and static code/contract links are analyzed inside `.ai-dev/runs/<task-id>/`.

It does not store secrets.
""",
    ".ai-dev/project-profile.md": """# Project Profile

- Project name: `{{PROJECT_NAME}}`
- Project root: `{{PROJECT_ROOT}}`
- Initialized at: `{{INIT_DATE}}`
- Default mode: `{{DEFAULT_MODE}}`
- Detected stack: `{{DETECTED_STACK}}`

## Expected Code Roots

- Backend:
- Frontend:
- Tests:
- Docs:

## Default Verification Commands

```text
{{DEFAULT_VERIFY_COMMANDS}}
```
""",
    ".ai-dev/instructions/agent-entry.md": """# Shared Agent Entry

This is the shared entrypoint for Codex, Claude Code, and other coding agents.

## Startup

1. Confirm repository root.
2. Read `.ai-dev/project-profile.md`.
3. Read `.ai-dev/context/constitution.md`.
4. Read `.ai-dev/context/knowledge-sources.md`.
5. Read `.ai-dev/context/local-rules.md`.
6. Select one workflow:
   - `feature-delivery`
   - `assisted-development`
   - `quick-check`
7. Read the selected workflow and required gates.
8. For feature work, create or update a task run under `.ai-dev/runs/<task-id>/`.

## Runtime / Static Analysis Boundary

- During project startup, treat `.ai-dev/context/runtime/`, `.ai-dev/context/static/`, and `.ai-dev/context/contracts/` as reusable maps and candidates.
- During a concrete feature or fix, analyze the requirement-specific dynamic flow in `runtime-flow.md`, static code links in `static-links.md`, and contract impact in `contract-checklist.md`.
- For an empty or greenfield project, mark existing-flow sections as `N/A` and design the target flow instead.

## Evidence Order

1. Real code and tests in this repository.
2. `.ai-dev/context` files.
3. External wiki or Yuque documents listed in `knowledge-sources.md`.
4. MCP sources such as Apifox and Codeup.
5. Chat history.

If sources conflict, trust real code for implementation facts and record the knowledge follow-up.
""",
    ".ai-dev/instructions/codex-notes.md": """# Codex Notes

- Use `AGENTS.md` as the project entrypoint.
- Use configured Codex MCP servers when available.
- Keep secrets in local environment files such as `~/.codex/mcp-env.sh`.
""",
    ".ai-dev/instructions/claude-notes.md": """# Claude Code Notes

- Use `CLAUDE.md` as the project entrypoint.
- Use `.mcp.json` or `claude mcp add` when configuring MCP.
- Keep secrets in local environment variables or secret stores.
""",
    ".ai-dev/context/knowledge-sources.md": """# Knowledge Sources

## Local / External Wiki

- Global wiki root: `{{GLOBAL_WIKI_ROOT}}`
- Standards:
- Runtime flows:
- Static architecture / dependency maps:
- Contracts:
- Team methods:

## Yuque

- Enabled: `{{YUQUE_ENABLED}}`
- PRD space:
- Standards space:
- Delivery docs space:

## Apifox

- Enabled: `{{APIFOX_ENABLED}}`
- Project ID: `{{APIFOX_PROJECT_ID}}`

## Codeup / Yunxiao

- Enabled: `{{CODEUP_ENABLED}}`
- Repository:
- Work item project:

## DingTalk

- Enabled: `{{DINGTALK_ENABLED}}`
- Notify mode: `draft`
""",
    ".ai-dev/context/local-rules.md": """# Local Rules

- Keep changes scoped to the active task.
- Match existing project style before introducing new abstractions.
- Do not change API, data, permission, or compatibility contracts without recording the impact.
- Do not claim tests passed without reproducible evidence.
""",
    ".ai-dev/context/constitution.md": """# Constitution

These rules are the project-local contract for AI-assisted development.

1. Real code and reproducible tests outrank chat history and stale documentation.
2. External wiki knowledge should shape understanding, but implementation claims must be checked against the repository.
3. Do not claim completion without command output, script paths, assertions, and actual results.
4. Runtime flow and contracts must be checked before behavior, API, data, permission, or compatibility changes.
5. Small tasks may use `quick-check`, but still need a run record and evidence.
6. Do not print, store, or commit secrets.
7. If the wiki conflicts with code, finish from code truth and create a wiki follow-up.
8. Keep task slices atomic enough to review, test, and roll back.
""",
    ".ai-dev/context/code-map.md": """# Code Map

This is an initialization-time navigation map, not final evidence.

## Detected Roots

{{CODE_MAP_ROOTS}}

## Detected Entrypoint Candidates

{{CODE_MAP_ENTRYPOINTS}}

## Detected Test Files

{{CODE_MAP_TESTS}}

## Notes

- Verify all implementation claims against real files before using them as evidence.
- Re-check relevant paths during each concrete requirement run before coding.
""",
    ".ai-dev/context/tool-bindings.md": """# Tool Bindings

## MCP Servers

- Apifox: {{APIFOX_BINDING}}
- Codeup / Yunxiao: {{CODEUP_BINDING}}
- Yuque: {{YUQUE_ENABLED}}
- DingTalk: {{DINGTALK_ENABLED}}

## Local Commands

- Install: {{INSTALL_COMMANDS}}
- Compile: {{COMPILE_COMMANDS}}
- Lint: {{LINT_COMMANDS}}
- Unit tests: {{UNIT_TEST_COMMANDS}}
- API tests:
- Feature tests:
- Full test runner: {{FULL_TEST_COMMANDS}}

## Delivery

- Git remote: {{GIT_REMOTE}}
- Current branch: {{GIT_BRANCH}}
- Default branch: {{GIT_DEFAULT_BRANCH}}
- Feature branch convention:
- Commit convention:
- Merge request convention:
""",
    ".ai-dev/context/runtime/entrypoints.md": "# Runtime Entrypoints\n\nProject-level dynamic runtime candidates. Initialization may list candidates, but concrete flow analysis happens per requirement under `.ai-dev/runs/<task-id>/runtime-flow.md`.\n\n## Detected Candidates\n\n{{RUNTIME_ENTRYPOINTS}}\n\n## To Confirm\n\n- HTTP routes:\n- Frontend actions:\n- CLI commands:\n- Scheduled jobs:\n- Message events:\n- Webhooks:\n- Background workers:\n",
    ".ai-dev/context/runtime/request-flows.md": "# Request Flows\n\nReusable project-level flow notes. Fill only after confirming against real code or after a completed feature run.\n\n```text\nFlow name:\nTrigger:\nRoute / entrypoint:\nModules:\nData read:\nData written:\nExternal calls:\nAsync continuation:\nFailure handling:\nObservability:\n```\n",
    ".ai-dev/context/runtime/scheduled-jobs.md": "# Scheduled Jobs\n\n- Job:\n- Trigger:\n- Config:\n- Data touched:\n- Failure handling:\n- Logs / monitoring:\n",
    ".ai-dev/context/runtime/async-events.md": "# Async Events\n\n- Event / topic:\n- Producer:\n- Consumer:\n- Payload contract:\n- Retry / dead-letter behavior:\n- Idempotency:\n",
    ".ai-dev/context/runtime/config-switches.md": "# Config Switches\n\n- Config:\n- Default:\n- Environments:\n- Runtime effect:\n- Related tests:\n",
    ".ai-dev/context/runtime/observability.md": "# Observability\n\n- Logs:\n- Trace IDs:\n- Metrics:\n- Alerts:\n- Dashboards:\n- Test output locations:\n",
    ".ai-dev/context/static/module-map.md": "# Static Module Map\n\nProject-level static structure candidates. Confirm relevant modules per requirement before coding.\n\n## Modules\n\n- Module:\n- Responsibility:\n- Owners / conventions:\n- Main files:\n- Related tests:\n",
    ".ai-dev/context/static/dependencies.md": "# Static Dependencies\n\nRecord important compile-time or import-time dependencies after confirming from real code.\n\n- Source module:\n- Depends on:\n- Direction allowed:\n- Boundary rule:\n- Risk:\n",
    ".ai-dev/context/static/call-sites.md": "# Static Call Sites\n\nRecord important call-site relationships that matter for feature changes.\n\n- Caller:\n- Callee:\n- Contract assumed:\n- Tests covering it:\n",
    ".ai-dev/context/contracts/api-contracts.md": "# API Contracts\n\nProject-level contract candidates. Requirement-specific contract impact belongs in `.ai-dev/runs/<task-id>/contract-checklist.md`.\n\n## Sources\n\n- Apifox project id: `{{APIFOX_PROJECT_ID}}`\n- Local OpenAPI candidates:\n{{OPENAPI_CANDIDATES}}\n\n## To Fill\n\n- Endpoint:\n- Request fields:\n- Response fields:\n- Status codes:\n- Error codes:\n- Compatibility notes:\n- Apifox source:\n",
    ".ai-dev/context/contracts/data-contracts.md": "# Data Contracts\n\n## Detected Model / Migration Candidates\n\n{{DATA_CONTRACT_CANDIDATES}}\n\n## To Fill\n\n- Table / model:\n- Field:\n- Meaning:\n- Allowed values:\n- State transitions:\n- Uniqueness / idempotency:\n- Migration notes:\n",
    ".ai-dev/context/contracts/business-rules.md": "# Business Rules\n\n- Rule:\n- Source:\n- Applies when:\n- Forbidden behavior:\n- Tests:\n",
    ".ai-dev/context/contracts/error-contracts.md": "# Error Contracts\n\n## Detected Error / Exception Candidates\n\n{{ERROR_CONTRACT_CANDIDATES}}\n\n## To Fill\n\n- Error:\n- Retryable:\n- User-facing message:\n- Rollback / compensation:\n- Logging / alerting:\n",
    ".ai-dev/context/contracts/permission-contracts.md": "# Permission Contracts\n\n## Detected Auth / Permission Candidates\n\n{{PERMISSION_CONTRACT_CANDIDATES}}\n\n## To Fill\n\n- Role / actor:\n- Allowed actions:\n- Forbidden actions:\n- Data scope:\n- Tests:\n",
    ".ai-dev/context/contracts/compatibility-contracts.md": "# Compatibility Contracts\n\n- Existing caller:\n- Behavior depended on:\n- Compatibility risk:\n- Migration / rollout:\n- Tests:\n",
    ".ai-dev/harness/workflows/feature-delivery.md": """# Feature Delivery Workflow

Use for full AI-led feature delivery.

1. Read requirement source.
2. Read project context and external knowledge sources.
3. Inspect real code, relevant tests, and candidate maps.
4. For this requirement, map dynamic runtime flow, static code links, and contracts. In an empty project, mark existing-flow sections as `N/A` and design the target flow.
5. Create a run directory from `_task-template` and maintain `context-capsule.md`.
6. Produce requirement summary, design, and an atomic development plan.
7. Ask for user confirmation when behavior, runtime flow, API, data, or risk is uncertain.
8. Implement scoped changes task by task.
9. Review for scope, contracts, runtime integration, island code, and open-code-review findings when configured.
10. Write and run reproducible tests.
11. Record evidence and update the context capsule.
12. Run harness self-check before delivery.
13. Prepare Apifox, Codeup, Yuque, and DingTalk handoff notes when relevant.
""",
    ".ai-dev/harness/workflows/assisted-development.md": """# Assisted Development Workflow

Use when the human writes or drives the code and the agent assists.

1. Read the user's current change or intended change.
2. Inspect diff or affected files.
3. Identify requirement-specific runtime, static-link, and contract impact.
4. Maintain a lightweight run record and `context-capsule.md`.
5. Review scope, contracts, island code, test gaps, and open-code-review findings when configured.
6. Write or propose missing test scripts.
7. Run requested verification or provide exact commands.
8. Produce test evidence and delivery notes.
""",
    ".ai-dev/harness/workflows/quick-check.md": """# Quick Check Workflow

Use for small fixes or small feature changes.

Minimum record:

1. One-sentence requirement.
2. Changed files or intended files.
3. Runtime flow impact.
4. Static code-link impact.
5. API/data/permission/contract impact.
6. Context capsule with current facts and decisions.
7. Test script or command.
8. Actual result.
9. Delivery note.
""",
    ".ai-dev/harness/gates/requirement-gate.md": "# Requirement Gate\n\nPass when requirement source, behavior, scope, non-goals, open questions, and selected mode are recorded.\n",
    ".ai-dev/harness/gates/runtime-flow-gate.md": "# Runtime Flow Gate\n\nPass when the requirement-specific dynamic path is recorded: entrypoint, modules, data, async/scheduled behavior, config, failure handling, and observability. For empty projects, pass only when existing flow is marked `N/A` and target flow is described.\n",
    ".ai-dev/harness/gates/static-link-gate.md": "# Static Link Gate\n\nPass when requirement-specific static code links are recorded: affected modules, callers/callees, dependency direction, shared types/models, configuration, and related tests. Use real code paths, not only candidate maps.\n",
    ".ai-dev/harness/gates/contract-gate.md": "# Contract Gate\n\nPass when requirement-specific API, data, business, error, permission, and compatibility contracts are checked. Do not silently change contracts.\n",
    ".ai-dev/harness/gates/design-gate.md": "# Design Gate\n\nPass when requirement summary, runtime flow, static links, contract checklist, affected code paths, risks, rollback, and verification focus exist.\n",
    ".ai-dev/harness/gates/implementation-gate.md": "# Implementation Gate\n\nPass when changes are scoped, style matches project conventions, and new code is connected to runtime flow.\n",
    ".ai-dev/harness/gates/atomic-task-gate.md": "# Atomic Task Gate\n\nPass when each implementation task has an objective, affected files, dependencies, verification, and a deterministic pass/fail result.\n\nGood task size: small enough to review, test, and roll back independently.\n",
    ".ai-dev/harness/gates/context-capsule-gate.md": "# Context Capsule Gate\n\nPass when the active run has `context-capsule.md` with current goal, confirmed facts, decisions, changed files, tests run, open blockers, and next step.\n",
    ".ai-dev/harness/gates/code-review-gate.md": "# Code Review Gate\n\nPass when scope, security, permissions, runtime integration, contract safety, errors, tests, and `No orphan module / no island code` are checked.\n\nIf open-code-review is configured, save its raw output under the active run's `review/` directory, classify findings, and record fixes or accepted risks.\n",
    ".ai-dev/harness/gates/test-gate.md": "# Test Gate\n\nPass when evidence includes script paths or commands, inputs, expected assertions, actual results, rerun history, unrun risks, and runtime/contract coverage notes.\n",
    ".ai-dev/harness/gates/apifox-gate.md": "# Apifox Gate\n\nPass when API contract impact is checked and Apifox update needs are recorded.\n",
    ".ai-dev/harness/gates/codeup-delivery-gate.md": "# Codeup Delivery Gate\n\nPass before push/MR when git status, diff, secrets, unrelated files, commit/MR notes, verification evidence, and user approval are checked.\n",
    ".ai-dev/harness/gates/doc-sync-gate.md": "# Doc Sync Gate\n\nPass when delivery docs include requirement, design, runtime, contracts, changed files, tests, Apifox, Codeup, and Yuque/DingTalk drafts when needed.\n",
    ".ai-dev/harness/gates/state-gate.md": "# State Gate\n\nPass when active task, progress, handoff, and run artifacts match the selected workflow.\n",
    ".ai-dev/harness/gates/quick-scope-gate.md": "# Quick Scope Gate\n\nPass when a small change records requirement, affected files, non-goals, and why quick-check is sufficient.\n",
    ".ai-dev/harness/gates/runtime-impact-gate.md": "# Runtime Impact Gate\n\nPass when runtime behavior impact is recorded for the active requirement. If changed, identify the entrypoint and affected flow.\n",
    ".ai-dev/harness/gates/static-impact-gate.md": "# Static Impact Gate\n\nPass when static code-link impact is recorded for the active requirement. If changed, identify modules, dependencies, call sites, config, and tests.\n",
    ".ai-dev/harness/gates/contract-impact-gate.md": "# Contract Impact Gate\n\nPass when API, data, business, error, permission, and compatibility impact is recorded. If changed, use full contract gate.\n",
    ".ai-dev/harness/gates/delivery-note-gate.md": "# Delivery Note Gate\n\nPass when the run includes what changed, how it was verified, remaining risks, and suggested commit/MR summary.\n",
    ".ai-dev/harness/state/active-task.json": '{\n  "activeTaskId": "",\n  "mode": "{{DEFAULT_MODE}}",\n  "status": "idle",\n  "runPath": "",\n  "updatedAt": "{{INIT_DATE}}"\n}\n',
    ".ai-dev/harness/state/progress.md": "# Progress\n\n- Status: idle\n- Active task: none\n- Current run: none\n\nDo not claim completion without test evidence and gate results.\n",
    ".ai-dev/harness/state/session-handoff.md": "# Session Handoff\n\n- Current task: none\n- Next step: start with `feature-delivery`, `assisted-development`, or `quick-check`.\n- Blockers: none recorded.\n",
    ".ai-dev/mcp/servers.md": "# MCP Servers\n\nProject-level MCP binding notes. Do not store secrets here.\n\n- `apifox_api_docs`: API contract lookup.\n- `yunxiao_codeup`: Codeup repository, branch, MR, pipeline context.\n- `yuque_docs`: PRD and internal documentation.\n- `dingtalk`: delivery notification drafts or sends.\n",
    ".ai-dev/mcp/env.example": "YUQUE_TOKEN=\nDINGTALK_Client_ID=\nDINGTALK_Client_Secret=\nYUNXIAO_ACCESS_TOKEN=\nYUNXIAO_API_BASE_URL=\nAPIFOX_ACCESS_TOKEN=\nAPIFOX_PROJECT_ID=\n",
    ".ai-dev/mcp/tool-usage.md": "# MCP Tool Usage\n\n- Use Yuque for PRD and internal docs when configured.\n- Use Apifox before changing API fields.\n- Use Codeup for branch, MR, work item, or pipeline context.\n- Draft DingTalk messages first; send only with explicit approval.\n",
    ".ai-dev/mcp/codex-config.example.toml": "[mcp_servers.apifox_api_docs]\ncommand = \"/path/to/apifox-wrapper.sh\"\n\n[mcp_servers.yunxiao_codeup]\ncommand = \"/path/to/yunxiao-wrapper.sh\"\n",
    ".ai-dev/mcp/claude-mcp.example.json": '{\n  "mcpServers": {\n    "apifox_api_docs": {\n      "command": "npx",\n      "args": ["-y", "apifox-mcp-server@latest", "--project-id=${APIFOX_PROJECT_ID}"],\n      "env": {"APIFOX_ACCESS_TOKEN": "${APIFOX_ACCESS_TOKEN}"}\n    },\n    "yunxiao_codeup": {\n      "command": "npx",\n      "args": ["-y", "alibabacloud-devops-mcp-server"],\n      "env": {"YUNXIAO_ACCESS_TOKEN": "${YUNXIAO_ACCESS_TOKEN}"}\n    }\n  }\n}\n',
    ".ai-dev/adapters/open-code-review.md": """# Open Code Review Adapter

Use this adapter when `alibaba/open-code-review` is available for an extra review pass.

## Setup

- Keep credentials outside the repository.
- Project rules live in `.opencodereview/rule.json`.
- Confirm the tool works before relying on it for delivery.

## Suggested Run

```bash
mkdir -p .ai-dev/runs/<task-id>/review
ocr llm test
ocr review --format json > .ai-dev/runs/<task-id>/review/open-code-review.json
```

If the project uses branch comparison, prefer the team's supported `from` and `to` arguments and record the exact command.

## Required Handling

1. Save raw output under `.ai-dev/runs/<task-id>/review/`.
2. Classify findings as `blocker`, `should-fix`, `note`, or `false-positive`.
3. Fix blockers before delivery unless the user explicitly accepts the risk.
4. Record fixes and remaining risks in `code-review.md` and `delivery-report.md`.
5. Do not auto-apply patches without reviewing the diff.
""",
    ".ai-dev/harness/eval/harness-self-check.md": """# Harness Self Check

Run before claiming a task is complete.

## Checklist

- Requirement source and selected mode are recorded.
- External wiki sources consulted or explicitly marked not needed.
- Code evidence includes real file paths.
- Runtime flow impact is recorded.
- Static code-link impact is recorded.
- Contract impact is recorded.
- Development plan is split into atomic tasks when more than one code step is needed.
- Test scripts or commands are reproducible.
- Actual test results are saved under the run directory.
- Code review findings are classified.
- Apifox / Codeup / Yuque / DingTalk follow-up is recorded when relevant.
- `context-capsule.md`, `test-report.md`, and `delivery-report.md` are current.
""",
    ".opencodereview/rule.json": '{\n  "rules": [\n    {\n      "path": "**/*",\n      "rule": "Review for scoped changes, runtime integration, contract compatibility, permission safety, error handling, and missing tests. Flag unused island code and unverifiable behavior claims."\n    },\n    {\n      "path": "**/*.{ts,tsx,js,jsx}",\n      "rule": "Check async errors, null or undefined handling, API response shape changes, state updates, and user-visible regressions."\n    },\n    {\n      "path": "**/*.{py}",\n      "rule": "Check input validation, exception handling, data boundary assumptions, and missing pytest or integration coverage."\n    },\n    {\n      "path": "**/*.{java,kt}",\n      "rule": "Check transaction boundaries, permission checks, DTO compatibility, null safety, and service/controller wiring."\n    }\n  ],\n  "exclude": [\n    "**/generated/**",\n    "vendor/**",\n    "node_modules/**",\n    "dist/**",\n    "build/**"\n  ]\n}\n',
    ".ai-dev/templates/requirement-summary.md": "# Requirement Summary\n\n- Source:\n- Goal:\n- In scope:\n- Out of scope:\n- Open questions:\n",
    ".ai-dev/templates/runtime-flow.md": "# Runtime Flow\n\nRequirement-specific dynamic runtime flow. For empty projects, mark existing flow as `N/A` and describe the target flow.\n\n- Entrypoint:\n- Modules:\n- Data read:\n- Data written:\n- External calls:\n- Async/scheduled behavior:\n- Config switches:\n- Failure handling:\n- Observability:\n",
    ".ai-dev/templates/static-links.md": "# Static Links\n\nRequirement-specific static code links. Use real code paths, imports, call sites, shared types, config, and tests.\n\n- Affected modules:\n- Callers:\n- Callees:\n- Shared types / models:\n- Dependency direction:\n- Config files:\n- Related tests:\n- Static risks:\n",
    ".ai-dev/templates/contract-checklist.md": "# Contract Checklist\n\n- API contracts:\n- Data contracts:\n- Business rules:\n- Error contracts:\n- Permission contracts:\n- Compatibility contracts:\n- Intentional changes:\n- Risks:\n",
    ".ai-dev/templates/design.md": "# Design\n\n## Requirement\n\n## Runtime Flow\n\n## Static Links\n\n## Contracts\n\n## Implementation Plan\n\n## Risks And Rollback\n\n## Verification Focus\n",
    ".ai-dev/templates/context-capsule.md": "# Context Capsule\n\n## Current Goal\n\n## Confirmed Facts\n\n## Key Decisions\n\n## Runtime / Contract Constraints\n\n## Changed Files\n\n## Tests Run\n\n## Open Questions / Blockers\n\n## Next Step\n",
    ".ai-dev/templates/development-plan.md": "# Development Plan\n\n## Summary\n\n- Task:\n- Files:\n- Verification:\n- Risks:\n\n## Atomic Tasks\n\n| ID | Objective | Files | Depends On | Verification | Status |\n| --- | --- | --- | --- | --- | --- |\n",
    ".ai-dev/templates/code-review.md": "# Code Review\n\n- Scope fit:\n- Runtime integration:\n- Contract safety:\n- Security/permissions:\n- Error handling:\n- Test coverage:\n- Island-code check:\n\n## Open Code Review\n\n- Tool used:\n- Command:\n- Raw output path:\n- Findings classified:\n\n## Findings\n\n| ID | Source | Severity | File | Finding | Action | Status |\n| --- | --- | --- | --- | --- | --- | --- |\n",
    ".ai-dev/templates/bug-list.md": "# Bug List\n\n| ID | Source | Description | Severity | Fix | Retest |\n| --- | --- | --- | --- | --- | --- |\n",
    ".ai-dev/templates/test-report.md": "# Test Report\n\n| Test | Purpose | Script/Command | Input | Expected | Actual | Runtime Flow | Static Link | Contract | Status |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n\n## Failures And Reruns\n\n## Unrun Tests And Risk\n",
    ".ai-dev/templates/delivery-report.md": "# Delivery Report\n\n## Summary\n\n## Changed Files\n\n## Runtime / Static / Contract Notes\n\n## Test Evidence\n\n## Code Review Evidence\n\n## Apifox Sync\n\n## Codeup Delivery\n\n## Yuque/DingTalk Draft\n\n## Wiki Follow-up\n\n## Residual Risk\n",
    ".ai-dev/templates/wiki-follow-up.md": "# Wiki Follow-up\n\n| ID | Source | Problem | Code Truth | Suggested Wiki Update | Owner | Status |\n| --- | --- | --- | --- | --- | --- | --- |\n",
    ".ai-dev/templates/quick-check.md": "# Quick Check\n\n- Requirement:\n- Changed files:\n- Runtime impact:\n- Static code-link impact:\n- API/data/permission/contract impact:\n- Context capsule path:\n- Test script or command:\n- Actual result:\n- Delivery note:\n",
    ".ai-dev/runs/_task-template/context-capsule.md": "# Context Capsule\n\n## Current Goal\n\n## Confirmed Facts\n\n## Key Decisions\n\n## Runtime / Contract Constraints\n\n## Changed Files\n\n## Tests Run\n\n## Open Questions / Blockers\n\n## Next Step\n",
    ".ai-dev/runs/_task-template/requirement-summary.md": "# Requirement Summary\n\n- Source:\n- Goal:\n- In scope:\n- Out of scope:\n- Open questions:\n",
    ".ai-dev/runs/_task-template/runtime-flow.md": "# Runtime Flow\n\nRequirement-specific dynamic runtime flow. For empty projects, mark existing flow as `N/A` and describe the target flow.\n\n- Entrypoint:\n- Modules:\n- Data read:\n- Data written:\n- External calls:\n- Async/scheduled behavior:\n- Config switches:\n- Failure handling:\n- Observability:\n",
    ".ai-dev/runs/_task-template/static-links.md": "# Static Links\n\nRequirement-specific static code links. Use real code paths, imports, call sites, shared types, config, and tests.\n\n- Affected modules:\n- Callers:\n- Callees:\n- Shared types / models:\n- Dependency direction:\n- Config files:\n- Related tests:\n- Static risks:\n",
    ".ai-dev/runs/_task-template/contract-checklist.md": "# Contract Checklist\n\n- API contracts:\n- Data contracts:\n- Business rules:\n- Error contracts:\n- Permission contracts:\n- Compatibility contracts:\n- Intentional changes:\n- Risks:\n",
    ".ai-dev/runs/_task-template/design.md": "# Design\n\n## Requirement\n\n## Runtime Flow\n\n## Static Links\n\n## Contracts\n\n## Implementation Plan\n\n## Risks And Rollback\n\n## Verification Focus\n",
    ".ai-dev/runs/_task-template/development-plan.md": "# Development Plan\n\n## Summary\n\n- Task:\n- Files:\n- Verification:\n- Risks:\n\n## Atomic Tasks\n\n| ID | Objective | Files | Depends On | Verification | Status |\n| --- | --- | --- | --- | --- | --- |\n",
    ".ai-dev/runs/_task-template/code-review.md": "# Code Review\n\n- Scope fit:\n- Runtime integration:\n- Contract safety:\n- Security/permissions:\n- Error handling:\n- Test coverage:\n- Island-code check:\n\n## Open Code Review\n\n- Tool used:\n- Command:\n- Raw output path:\n- Findings classified:\n\n## Findings\n\n| ID | Source | Severity | File | Finding | Action | Status |\n| --- | --- | --- | --- | --- | --- | --- |\n",
    ".ai-dev/runs/_task-template/bug-list.md": "# Bug List\n\n| ID | Source | Description | Severity | Fix | Retest |\n| --- | --- | --- | --- | --- | --- |\n",
    ".ai-dev/runs/_task-template/test-report.md": "# Test Report\n\n| Test | Purpose | Script/Command | Input | Expected | Actual | Runtime Flow | Static Link | Contract | Status |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n\n## Failures And Reruns\n\n## Unrun Tests And Risk\n",
    ".ai-dev/runs/_task-template/delivery-report.md": "# Delivery Report\n\n## Summary\n\n## Changed Files\n\n## Runtime / Static / Contract Notes\n\n## Test Evidence\n\n## Code Review Evidence\n\n## Apifox Sync\n\n## Codeup Delivery\n\n## Yuque/DingTalk Draft\n\n## Wiki Follow-up\n\n## Residual Risk\n",
    ".ai-dev/runs/_task-template/wiki-follow-up.md": "# Wiki Follow-up\n\n| ID | Source | Problem | Code Truth | Suggested Wiki Update | Owner | Status |\n| --- | --- | --- | --- | --- | --- | --- |\n",
    ".ai-dev/runs/_task-template/tests/scripts/.gitkeep": "",
    ".ai-dev/runs/_task-template/tests/evidence/.gitkeep": "",
    ".ai-dev/runs/_task-template/review/.gitkeep": "",
    ".ai-dev/runs/.gitkeep": "",
}


def detect_stack(project: Path) -> str:
    checks = [
        ("package.json", "node"),
        ("pyproject.toml", "python"),
        ("requirements.txt", "python"),
        ("pom.xml", "java-maven"),
        ("build.gradle", "java-gradle"),
        ("Dockerfile", "docker"),
        ("docker-compose.yml", "docker-compose"),
    ]
    found = [label for filename, label in checks if (project / filename).exists()]
    return ", ".join(dict.fromkeys(found)) or "generic"


def run_git(project: Path, args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=project,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def list_existing(project: Path, candidates: list[str]) -> list[str]:
    return [item for item in candidates if (project / item).exists()]


def find_files(project: Path, patterns: tuple[str, ...], limit: int = 40) -> list[str]:
    skip_parts = {
        ".git",
        "node_modules",
        ".venv",
        "venv",
        "__pycache__",
        "dist",
        "build",
        ".ai-dev",
    }
    found: list[str] = []
    for path in project.rglob("*"):
        if len(found) >= limit:
            break
        if not path.is_file():
            continue
        rel = path.relative_to(project)
        if any(part in skip_parts for part in rel.parts):
            continue
        rel_s = str(rel)
        lower = rel_s.lower()
        if any(pattern in lower for pattern in patterns):
            found.append(rel_s)
    return found


def bullets(items: list[str], empty: str = "- None detected.") -> str:
    if not items:
        return empty
    return "\n".join(f"- `{item}`" for item in items)


def package_scripts(project: Path) -> dict[str, str]:
    package = read_json(project / "package.json")
    scripts = package.get("scripts", {}) if isinstance(package, dict) else {}
    return scripts if isinstance(scripts, dict) else {}


def command_summary(project: Path) -> dict[str, str]:
    scripts = package_scripts(project)
    install = []
    compile_cmds = []
    lint = []
    tests = []
    full = []

    if (project / "package-lock.json").exists():
        install.append("npm ci")
    elif (project / "pnpm-lock.yaml").exists():
        install.append("pnpm install --frozen-lockfile")
    elif (project / "yarn.lock").exists():
        install.append("yarn install --frozen-lockfile")
    elif (project / "package.json").exists():
        install.append("npm install")

    if (project / "requirements.txt").exists():
        install.append("pip install -r requirements.txt")
    if (project / "pyproject.toml").exists():
        install.append("pip install -e .")

    for name in scripts:
        lower = name.lower()
        cmd = f"npm run {name}"
        if lower in {"build", "compile", "typecheck"} or "build" in lower:
            compile_cmds.append(cmd)
        if "lint" in lower or "format" in lower:
            lint.append(cmd)
        if "test" in lower:
            tests.append(cmd)
            if lower in {"test", "test:all", "test:ci"}:
                full.append(cmd)

    if (project / "pyproject.toml").exists() or (project / "requirements.txt").exists():
        tests.append("pytest")
        full.append("pytest")
    if (project / "pom.xml").exists():
        tests.append("mvn test")
        full.append("mvn test")
    if (project / "run_tests.py").exists():
        full.append("python run_tests.py")

    return {
        "install": "; ".join(dict.fromkeys(install)) or "Fill project-specific install command.",
        "compile": "; ".join(dict.fromkeys(compile_cmds)) or "Fill project-specific compile/build command.",
        "lint": "; ".join(dict.fromkeys(lint)) or "Fill project-specific lint command.",
        "unit": "; ".join(dict.fromkeys(tests)) or "Fill project-specific unit test command.",
        "full": "; ".join(dict.fromkeys(full)) or "Fill project-specific full test command.",
    }


def default_verify_commands(project: Path) -> str:
    commands = command_summary(project)["full"]
    return commands


def scan_project(project: Path, depth: str) -> dict[str, str | list[str]]:
    roots = list_existing(
        project,
        [
            "src",
            "app",
            "apps",
            "server",
            "backend",
            "frontend",
            "web",
            "tests",
            "test",
            "docs",
            "scripts",
            "config",
            "migrations",
        ],
    )
    route_files = find_files(project, ("route", "router", "controller", "urls.py", "views.py", "api"), 60)
    test_files = find_files(project, ("test_", "_test.", ".spec.", ".test.", "/tests/", "/test/"), 60)
    scheduled = find_files(project, ("cron", "schedule", "celery", "job", "task"), 40)
    async_events = find_files(project, ("consumer", "producer", "queue", "kafka", "rabbit", "event", "message"), 40)
    openapi = find_files(project, ("openapi", "swagger"), 20)
    data = find_files(project, ("model", "schema", "migration", "entity", "dao", "repository"), 60)
    errors = find_files(project, ("error", "exception", "errors", "exceptions"), 40)
    permissions = find_files(project, ("auth", "permission", "permissions", "guard", "middleware"), 40)

    if depth == "minimal":
        route_files = test_files = scheduled = async_events = openapi = data = errors = permissions = []

    return {
        "roots": roots,
        "route_files": route_files,
        "test_files": test_files,
        "scheduled": scheduled,
        "async_events": async_events,
        "openapi": openapi,
        "data": data,
        "errors": errors,
        "permissions": permissions,
    }


def build_initialization_report(
    *,
    project: Path,
    mode: str,
    depth: str,
    values: dict[str, str],
    scan: dict[str, str | list[str]],
    token_status: dict[str, bool],
    created: list[str],
    skipped: list[str],
) -> str:
    token_lines = "\n".join(f"- {key}: {'set' if value else 'missing'}" for key, value in token_status.items())
    created_lines = "\n".join(f"- `{item}`" for item in created[:80]) or "- None."
    skipped_lines = "\n".join(f"- `{item}`" for item in skipped[:80]) or "- None."
    gaps = []
    if not values.get("GLOBAL_WIKI_ROOT"):
        gaps.append("Global wiki root is not configured.")
    if not values.get("APIFOX_PROJECT_ID"):
        gaps.append("Apifox project id is not configured.")
    if not scan["route_files"]:
        gaps.append("No route/controller/API entrypoint candidates detected.")
    if not scan["test_files"]:
        gaps.append("No test files detected.")
    if not scan["data"]:
        gaps.append("No model/schema/migration candidates detected.")
    gap_lines = "\n".join(f"- {gap}" for gap in gaps) or "- No obvious gaps from initialization scan."

    return f"""# Initialization Report

## Summary

- Project: `{project}`
- Default mode: `{mode}`
- Initialization depth: `{depth}`
- Detected stack: `{values['DETECTED_STACK']}`
- Initialized at: `{values['INIT_DATE']}`

## Detected Roots

{bullets(scan['roots'])}

## Runtime Entrypoint Candidates

{bullets(scan['route_files'])}

## Scheduled / Async Candidates

Scheduled:

{bullets(scan['scheduled'])}

Async/events:

{bullets(scan['async_events'])}

## Contract Candidates

OpenAPI:

{bullets(scan['openapi'])}

Data:

{bullets(scan['data'])}

Errors:

{bullets(scan['errors'])}

Permissions:

{bullets(scan['permissions'])}

## Test Candidates

{bullets(scan['test_files'])}

## Token Status

Values are not printed.

{token_lines}

## Created Or Updated

{created_lines}

## Skipped Existing

{skipped_lines}

## Gaps To Fill

{gap_lines}

## Next Steps

1. Review `AGENTS.md` and `CLAUDE.md`.
2. Review `.ai-dev/context/constitution.md`.
3. Fill `.ai-dev/context/knowledge-sources.md`.
4. Fill `.ai-dev/context/tool-bindings.md`.
5. Review candidate runtime/static/contract maps; do not treat them as complete analysis.
6. Review `.ai-dev/adapters/open-code-review.md` if code review tooling is used.
7. Start with `feature-delivery`, `assisted-development`, or `quick-check`; analyze runtime/static/contracts inside the active run.
"""


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def write_file(path: Path, content: str, values: dict[str, str], force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(content, values))
    return True


def merge_entry(path: Path, content: str, values: dict[str, str], force: bool) -> bool:
    rendered = render(content, values)
    if force or not path.exists():
        return write_file(path, content, values, True)
    current = path.read_text()
    if ".ai-dev/instructions/agent-entry.md" in current:
        return False
    path.write_text(current.rstrip() + "\n\n---\n\n" + rendered)
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".", help="Target project root")
    parser.add_argument("--wiki-root", default=os.environ.get("AI_DEV_WIKI_ROOT", ""))
    parser.add_argument("--apifox-project-id", default=os.environ.get("APIFOX_PROJECT_ID", ""))
    parser.add_argument("--default-mode", default="quick-check", choices=["feature-delivery", "assisted-development", "quick-check"])
    parser.add_argument("--depth", default="standard", choices=["minimal", "standard", "deep"], help="Initialization content depth")
    parser.add_argument("--force", action="store_true", help="Overwrite existing generated files")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.exists():
        raise SystemExit(f"Project does not exist: {project}")

    today = dt.date.today().isoformat()
    scan = scan_project(project, args.depth)
    commands = command_summary(project)
    git_remote = run_git(project, ["remote", "get-url", "origin"])
    git_branch = run_git(project, ["branch", "--show-current"])
    git_default = run_git(project, ["rev-parse", "--abbrev-ref", "origin/HEAD"])
    if git_default.startswith("origin/"):
        git_default = git_default.removeprefix("origin/")
    if not git_default:
        git_default = "main"

    runtime_candidates = []
    runtime_candidates.extend(scan["route_files"])  # type: ignore[arg-type]
    runtime_candidates.extend(scan["scheduled"])  # type: ignore[arg-type]
    runtime_candidates.extend(scan["async_events"])  # type: ignore[arg-type]

    values = {
        "PROJECT_NAME": project.name,
        "PROJECT_ROOT": str(project),
        "INIT_DATE": today,
        "DEFAULT_MODE": args.default_mode,
        "DETECTED_STACK": detect_stack(project),
        "DEFAULT_VERIFY_COMMANDS": default_verify_commands(project),
        "GLOBAL_WIKI_ROOT": args.wiki_root,
        "YUQUE_ENABLED": "true" if os.environ.get("YUQUE_TOKEN") else "unknown",
        "APIFOX_ENABLED": "true" if args.apifox_project_id else "unknown",
        "APIFOX_PROJECT_ID": args.apifox_project_id,
        "CODEUP_ENABLED": "true" if os.environ.get("YUNXIAO_ACCESS_TOKEN") else "unknown",
        "DINGTALK_ENABLED": "true" if os.environ.get("DINGTALK_Client_ID") else "unknown",
        "CODE_MAP_ROOTS": bullets(scan["roots"]),  # type: ignore[arg-type]
        "CODE_MAP_ENTRYPOINTS": bullets(scan["route_files"]),  # type: ignore[arg-type]
        "CODE_MAP_TESTS": bullets(scan["test_files"]),  # type: ignore[arg-type]
        "RUNTIME_ENTRYPOINTS": bullets(runtime_candidates),
        "OPENAPI_CANDIDATES": bullets(scan["openapi"]),  # type: ignore[arg-type]
        "DATA_CONTRACT_CANDIDATES": bullets(scan["data"]),  # type: ignore[arg-type]
        "ERROR_CONTRACT_CANDIDATES": bullets(scan["errors"]),  # type: ignore[arg-type]
        "PERMISSION_CONTRACT_CANDIDATES": bullets(scan["permissions"]),  # type: ignore[arg-type]
        "INSTALL_COMMANDS": commands["install"],
        "COMPILE_COMMANDS": commands["compile"],
        "LINT_COMMANDS": commands["lint"],
        "UNIT_TEST_COMMANDS": commands["unit"],
        "FULL_TEST_COMMANDS": commands["full"],
        "GIT_REMOTE": git_remote or "unknown",
        "GIT_BRANCH": git_branch or "unknown",
        "GIT_DEFAULT_BRANCH": git_default,
        "APIFOX_BINDING": f"project id {args.apifox_project_id}" if args.apifox_project_id else "unknown",
        "CODEUP_BINDING": git_remote or "unknown",
    }

    created = []
    skipped = []
    for rel, content in FILES.items():
        path = project / rel
        if rel in {"AGENTS.md", "CLAUDE.md"}:
            changed = merge_entry(path, content, values, args.force)
        else:
            changed = write_file(path, content, values, args.force)
        (created if changed else skipped).append(rel)

    run_dir = project / ".ai-dev" / "runs" / f"init-{today}"
    report_path = run_dir / "initialization-report.md"
    report_content = build_initialization_report(
        project=project,
        mode=args.default_mode,
        depth=args.depth,
        values=values,
        scan=scan,
        token_status={key: bool(os.environ.get(key)) for key in TOKEN_KEYS},
        created=created,
        skipped=skipped,
    )
    if write_file(report_path, report_content, {}, args.force):
        created.append(str(report_path.relative_to(project)))
    else:
        skipped.append(str(report_path.relative_to(project)))

    report = {
        "project": str(project),
        "defaultMode": args.default_mode,
        "depth": args.depth,
        "detectedStack": values["DETECTED_STACK"],
        "wikiRootConfigured": bool(args.wiki_root),
        "apifoxProjectIdConfigured": bool(args.apifox_project_id),
        "tokenStatus": {key: bool(os.environ.get(key)) for key in TOKEN_KEYS},
        "createdOrUpdated": created,
        "skippedExisting": skipped,
        "nextSteps": [
            "Review AGENTS.md and CLAUDE.md.",
            "Review .ai-dev/context/constitution.md.",
            "Fill .ai-dev/context/knowledge-sources.md.",
            "Fill .ai-dev/context/tool-bindings.md.",
            "Review candidate runtime/static/contract maps; analyze them per requirement inside the active run.",
            "Review .ai-dev/adapters/open-code-review.md if code review tooling is used.",
            "Start with feature-delivery, assisted-development, or quick-check.",
        ],
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
