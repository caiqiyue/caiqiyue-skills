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
3. `.ai-dev/context/knowledge-sources.md`
4. `.ai-dev/context/local-rules.md`
5. The selected workflow under `.ai-dev/harness/workflows/`
6. The relevant gates under `.ai-dev/harness/gates/`

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
3. `.ai-dev/context/knowledge-sources.md`
4. `.ai-dev/context/local-rules.md`
5. The selected workflow under `.ai-dev/harness/workflows/`
6. The relevant gates under `.ai-dev/harness/gates/`

Hard rules:

- Do not claim completion before verification evidence exists.
- Design before implementation when runtime flow, contracts, data, or API behavior may change.
- Tests must include reproducible scripts or commands, inputs, assertions, and actual results.
- Do not print or commit secrets.
""",
    ".ai-dev/README.md": """# Project AI Development Harness

This directory is the project-local adapter for external wiki knowledge, harness workflows, skills, and MCP tools.

It stores context pointers, runtime and contract notes, workflows, gates, run artifacts, templates, and MCP usage notes.

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
3. Read `.ai-dev/context/knowledge-sources.md`.
4. Read `.ai-dev/context/local-rules.md`.
5. Select one workflow:
   - `feature-delivery`
   - `assisted-development`
   - `quick-check`
6. Read the selected workflow and required gates.

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
    ".ai-dev/context/code-map.md": """# Code Map

This is a navigation map, not final evidence.

## Detected Roots

{{CODE_MAP_ROOTS}}

## Detected Entrypoint Candidates

{{CODE_MAP_ENTRYPOINTS}}

## Detected Test Files

{{CODE_MAP_TESTS}}

## Notes

- Verify all implementation claims against real files before using them as evidence.
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
    ".ai-dev/context/runtime/entrypoints.md": "# Runtime Entrypoints\n\n## Detected Candidates\n\n{{RUNTIME_ENTRYPOINTS}}\n\n## To Confirm\n\n- HTTP routes:\n- Frontend actions:\n- CLI commands:\n- Scheduled jobs:\n- Message events:\n- Webhooks:\n- Background workers:\n",
    ".ai-dev/context/runtime/request-flows.md": "# Request Flows\n\n```text\nFlow name:\nTrigger:\nRoute / entrypoint:\nModules:\nData read:\nData written:\nExternal calls:\nAsync continuation:\nFailure handling:\nObservability:\n```\n",
    ".ai-dev/context/runtime/scheduled-jobs.md": "# Scheduled Jobs\n\n- Job:\n- Trigger:\n- Config:\n- Data touched:\n- Failure handling:\n- Logs / monitoring:\n",
    ".ai-dev/context/runtime/async-events.md": "# Async Events\n\n- Event / topic:\n- Producer:\n- Consumer:\n- Payload contract:\n- Retry / dead-letter behavior:\n- Idempotency:\n",
    ".ai-dev/context/runtime/config-switches.md": "# Config Switches\n\n- Config:\n- Default:\n- Environments:\n- Runtime effect:\n- Related tests:\n",
    ".ai-dev/context/runtime/observability.md": "# Observability\n\n- Logs:\n- Trace IDs:\n- Metrics:\n- Alerts:\n- Dashboards:\n- Test output locations:\n",
    ".ai-dev/context/contracts/api-contracts.md": "# API Contracts\n\n## Sources\n\n- Apifox project id: `{{APIFOX_PROJECT_ID}}`\n- Local OpenAPI candidates:\n{{OPENAPI_CANDIDATES}}\n\n## To Fill\n\n- Endpoint:\n- Request fields:\n- Response fields:\n- Status codes:\n- Error codes:\n- Compatibility notes:\n- Apifox source:\n",
    ".ai-dev/context/contracts/data-contracts.md": "# Data Contracts\n\n## Detected Model / Migration Candidates\n\n{{DATA_CONTRACT_CANDIDATES}}\n\n## To Fill\n\n- Table / model:\n- Field:\n- Meaning:\n- Allowed values:\n- State transitions:\n- Uniqueness / idempotency:\n- Migration notes:\n",
    ".ai-dev/context/contracts/business-rules.md": "# Business Rules\n\n- Rule:\n- Source:\n- Applies when:\n- Forbidden behavior:\n- Tests:\n",
    ".ai-dev/context/contracts/error-contracts.md": "# Error Contracts\n\n## Detected Error / Exception Candidates\n\n{{ERROR_CONTRACT_CANDIDATES}}\n\n## To Fill\n\n- Error:\n- Retryable:\n- User-facing message:\n- Rollback / compensation:\n- Logging / alerting:\n",
    ".ai-dev/context/contracts/permission-contracts.md": "# Permission Contracts\n\n## Detected Auth / Permission Candidates\n\n{{PERMISSION_CONTRACT_CANDIDATES}}\n\n## To Fill\n\n- Role / actor:\n- Allowed actions:\n- Forbidden actions:\n- Data scope:\n- Tests:\n",
    ".ai-dev/context/contracts/compatibility-contracts.md": "# Compatibility Contracts\n\n- Existing caller:\n- Behavior depended on:\n- Compatibility risk:\n- Migration / rollout:\n- Tests:\n",
    ".ai-dev/harness/workflows/feature-delivery.md": """# Feature Delivery Workflow

Use for full AI-led feature delivery.

1. Read requirement source.
2. Read project context and external knowledge sources.
3. Inspect real code and relevant tests.
4. Map runtime flow and contracts.
5. Produce requirement summary, design, and development plan.
6. Ask for user confirmation when behavior, runtime flow, API, data, or risk is uncertain.
7. Implement scoped changes.
8. Review for scope, contracts, runtime integration, and island code.
9. Write and run reproducible tests.
10. Record evidence.
11. Prepare Apifox, Codeup, Yuque, and DingTalk handoff notes when relevant.
""",
    ".ai-dev/harness/workflows/assisted-development.md": """# Assisted Development Workflow

Use when the human writes or drives the code and the agent assists.

1. Read the user's current change or intended change.
2. Inspect diff or affected files.
3. Identify runtime and contract impact.
4. Review scope, contracts, island code, and test gaps.
5. Write or propose missing test scripts.
6. Run requested verification or provide exact commands.
7. Produce test evidence and delivery notes.
""",
    ".ai-dev/harness/workflows/quick-check.md": """# Quick Check Workflow

Use for small fixes or small feature changes.

Minimum record:

1. One-sentence requirement.
2. Changed files or intended files.
3. API/data/permission/contract impact.
4. Runtime flow impact.
5. Test script or command.
6. Actual result.
7. Delivery note.
""",
    ".ai-dev/harness/gates/requirement-gate.md": "# Requirement Gate\n\nPass when requirement source, behavior, scope, non-goals, open questions, and selected mode are recorded.\n",
    ".ai-dev/harness/gates/runtime-flow-gate.md": "# Runtime Flow Gate\n\nPass when entrypoint, modules, data, async/scheduled behavior, config, failure handling, and observability are recorded or blockers are listed.\n",
    ".ai-dev/harness/gates/contract-gate.md": "# Contract Gate\n\nPass when API, data, business, error, permission, and compatibility contracts are checked. Do not silently change contracts.\n",
    ".ai-dev/harness/gates/design-gate.md": "# Design Gate\n\nPass when requirement summary, runtime flow, contract checklist, affected code paths, risks, rollback, and verification focus exist.\n",
    ".ai-dev/harness/gates/implementation-gate.md": "# Implementation Gate\n\nPass when changes are scoped, style matches project conventions, and new code is connected to runtime flow.\n",
    ".ai-dev/harness/gates/code-review-gate.md": "# Code Review Gate\n\nPass when scope, security, permissions, runtime integration, contract safety, errors, tests, and `No orphan module / no island code` are checked.\n",
    ".ai-dev/harness/gates/test-gate.md": "# Test Gate\n\nPass when evidence includes script paths or commands, inputs, expected assertions, actual results, rerun history, unrun risks, and runtime/contract coverage notes.\n",
    ".ai-dev/harness/gates/apifox-gate.md": "# Apifox Gate\n\nPass when API contract impact is checked and Apifox update needs are recorded.\n",
    ".ai-dev/harness/gates/codeup-delivery-gate.md": "# Codeup Delivery Gate\n\nPass before push/MR when git status, diff, secrets, unrelated files, commit/MR notes, verification evidence, and user approval are checked.\n",
    ".ai-dev/harness/gates/doc-sync-gate.md": "# Doc Sync Gate\n\nPass when delivery docs include requirement, design, runtime, contracts, changed files, tests, Apifox, Codeup, and Yuque/DingTalk drafts when needed.\n",
    ".ai-dev/harness/gates/state-gate.md": "# State Gate\n\nPass when active task, progress, handoff, and run artifacts match the selected workflow.\n",
    ".ai-dev/harness/gates/quick-scope-gate.md": "# Quick Scope Gate\n\nPass when a small change records requirement, affected files, non-goals, and why quick-check is sufficient.\n",
    ".ai-dev/harness/gates/runtime-impact-gate.md": "# Runtime Impact Gate\n\nPass when runtime behavior impact is recorded. If changed, identify the entrypoint and affected flow.\n",
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
    ".ai-dev/templates/requirement-summary.md": "# Requirement Summary\n\n- Source:\n- Goal:\n- In scope:\n- Out of scope:\n- Open questions:\n",
    ".ai-dev/templates/runtime-flow.md": "# Runtime Flow\n\n- Entrypoint:\n- Modules:\n- Data read:\n- Data written:\n- External calls:\n- Async/scheduled behavior:\n- Config switches:\n- Failure handling:\n- Observability:\n",
    ".ai-dev/templates/contract-checklist.md": "# Contract Checklist\n\n- API contracts:\n- Data contracts:\n- Business rules:\n- Error contracts:\n- Permission contracts:\n- Compatibility contracts:\n- Intentional changes:\n- Risks:\n",
    ".ai-dev/templates/design.md": "# Design\n\n## Requirement\n\n## Runtime Flow\n\n## Contracts\n\n## Implementation Plan\n\n## Risks And Rollback\n\n## Verification Focus\n",
    ".ai-dev/templates/development-plan.md": "# Development Plan\n\n- Task:\n- Files:\n- Steps:\n- Verification:\n- Risks:\n",
    ".ai-dev/templates/code-review.md": "# Code Review\n\n- Scope fit:\n- Runtime integration:\n- Contract safety:\n- Security/permissions:\n- Error handling:\n- Test coverage:\n- Island-code check:\n- Findings:\n",
    ".ai-dev/templates/bug-list.md": "# Bug List\n\n| ID | Source | Description | Severity | Fix | Retest |\n| --- | --- | --- | --- | --- | --- |\n",
    ".ai-dev/templates/test-report.md": "# Test Report\n\n| Test | Purpose | Script/Command | Input | Expected | Actual | Runtime Flow | Contract | Status |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n\n## Failures And Reruns\n\n## Unrun Tests And Risk\n",
    ".ai-dev/templates/delivery-report.md": "# Delivery Report\n\n## Summary\n\n## Changed Files\n\n## Runtime And Contract Notes\n\n## Test Evidence\n\n## Apifox Sync\n\n## Codeup Delivery\n\n## Yuque/DingTalk Draft\n\n## Residual Risk\n",
    ".ai-dev/templates/quick-check.md": "# Quick Check\n\n- Requirement:\n- Changed files:\n- API/data/permission/contract impact:\n- Runtime impact:\n- Test script or command:\n- Actual result:\n- Delivery note:\n",
    ".ai-dev/runs/.gitkeep": "",
}


TOKEN_KEYS = [
    "YUQUE_TOKEN",
    "DINGTALK_Client_ID",
    "DINGTALK_Client_Secret",
    "YUNXIAO_ACCESS_TOKEN",
    "APIFOX_ACCESS_TOKEN",
    "APIFOX_PROJECT_ID",
]


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
2. Fill `.ai-dev/context/knowledge-sources.md`.
3. Fill `.ai-dev/context/tool-bindings.md`.
4. Confirm runtime entrypoints and contracts.
5. Start with `feature-delivery`, `assisted-development`, or `quick-check`.
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
            "Fill .ai-dev/context/knowledge-sources.md.",
            "Fill .ai-dev/context/tool-bindings.md.",
            "Start with feature-delivery, assisted-development, or quick-check.",
        ],
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
