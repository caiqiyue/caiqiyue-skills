---
name: external-feature-flow
description: Use for standard feature development in an existing project using external tools instead of a custom harness. It routes each phase to concrete skills and CLIs such as spec-flow-analyzer, OpenSpec, GSD, Superpowers, Graphify, debug-hypothesis, ECC verification-loop, open-code-review, git skills, Apifox MCP, and Codeup Git, while archiving all outputs under .external-feature/runs/task-id/.
---

# External Feature Flow

Use this skill when the user wants to develop a feature in an existing project with a normal, reusable workflow powered by external tools. This is not the personal `.ai-dev` harness. It is a standard feature-delivery workflow that coordinates existing skills, MCPs, CLIs, Git, and project graph tools.

The official record for each feature run is:

```text
.external-feature/runs/<task-id>/
```

External tools may create their own default files, but this workflow must summarize, copy, or link the relevant output into the run directory before the phase is considered complete.

## Start A Run

From this skill directory:

```bash
python3 scripts/external_feature_run.py init --project /path/to/project \
  --task-id feature-slug \
  --title "Feature title"
```

If the user provides a PRD or requirement file:

```bash
python3 scripts/external_feature_run.py init --project /path/to/project \
  --task-id feature-slug \
  --title "Feature title" \
  --requirement-file /path/to/requirement.md
```

If no task id is provided, create a short lowercase hyphenated id from the title plus the current date.

## Non-Negotiable Rules

- Use concrete skills and CLI commands, not plugin names, when describing or executing a phase.
- Do not start coding before requirement review, project context, design, and task breakdown are recorded.
- Do not claim tests passed without fresh command output and saved evidence.
- Do not push, create merge requests, update Apifox, or post notifications without explicit user approval.
- Do not write secrets into the project. Use local environment files or existing MCP configuration.
- If a tool is unavailable, record the exact non-secret blocker and use the next best local evidence source.
- Treat real code and fresh test output as truth when they conflict with docs or generated plans.

## Standard Workflow

### 1. Requirement Intake

Concrete tools:
- Manual user prompt or attached file.
- Yuque or Codeup MCP only when configured and relevant.
- `external_feature_run.py init` to create the official run directory.

Archive to:

```text
00-input/requirement.md
00-input/source-links.md
```

Record:
- Requirement source.
- User goal.
- Known constraints.
- Links or file paths.

### 2. Requirement Review

Concrete tools:
- `spec-flow-analyzer` for user flows, missing states, ambiguity, and acceptance gaps.
- `openspec init` if the project has no OpenSpec setup and the user agrees.
- `openspec change`, `openspec validate`, and `openspec instructions` for change specs when the requirement is non-trivial.

Archive to:

```text
01-requirement-review/requirement-summary.md
01-requirement-review/acceptance-criteria.md
01-requirement-review/open-questions.md
01-requirement-review/spec-flow-analysis.md
01-requirement-review/openspec-change.md
```

Exit when acceptance criteria and blocking questions are explicit. If questions block implementation, stop and ask the user.

### 3. Project Context And Impact

Concrete tools:
- `graphify update <project>` or `graphify extract <project>` when graph data is missing or stale.
- `graphify query`, `graphify affected`, `graphify path`, or `graphify explain` for impact analysis.
- `rg`, `git log`, `git diff`, and real file reads for code evidence.
- `context7` for current library/framework docs when API usage matters.
- Apifox MCP for API contracts when endpoints, DTOs, request fields, response fields, or examples may change.
- Codeup/Yunxiao MCP for repository, branch, work item, MR, and pipeline context when available.

Archive to:

```text
02-context/code-map.md
02-context/graphify-notes.md
02-context/affected-nodes.md
02-context/apifox-contract.md
02-context/codeup-context.md
02-context/docs-references.md
```

Exit when the impacted modules, call paths, API contracts, and external constraints are clear enough to design.

### 4. Design

Concrete tools:
- OpenSpec change/spec artifacts for requirement-level design.
- `gsd-discuss-phase` when decisions need user clarification.
- `gsd-plan-phase --prd <file>` when the requirement should become a GSD phase plan.

Archive to:

```text
03-design/design.md
03-design/risks.md
03-design/compatibility.md
```

Design must include:
- Files or modules likely to change.
- Runtime behavior.
- Static dependencies and call sites.
- API/data/permission compatibility.
- Rollback or residual risk notes.

### 5. Atomic Task Plan

Concrete tools:
- `superpowers:writing-plans` for a detailed implementation plan with test-first steps.
- `gsd-plan-phase` when using GSD phases and wave execution.

Archive to:

```text
04-plan/plan.md
04-plan/atomic-tasks.md
04-plan/skill-routing.md
```

Every atomic task must specify:
- Exact file paths.
- Intended behavior.
- Test-first or verification step.
- Expected result.
- Commit boundary when useful.

### 6. Implementation

Concrete tools:
- `superpowers:test-driven-development` for new behavior and bug fixes.
- `superpowers:executing-plans` for executing a written plan inline.
- `gsd-execute-phase` for GSD wave execution.
- `debug-hypothesis` or `systematic-debugging` for non-trivial failures.
- `git-worktree` when isolated branch/worktree execution is useful.

Archive to:

```text
05-implementation/changed-files.md
05-implementation/debug.md
05-implementation/task-progress.md
```

Keep implementation scoped to the accepted plan. If the plan is wrong, update the plan and record why before continuing.

### 7. Testing And Verification

Concrete tools:
- `verification-loop` for build, typecheck, lint, tests, security scan, and diff review.
- `superpowers:verification-before-completion` before any completion claim.
- Project-native commands such as `npm test`, `pnpm test`, `pytest`, `go test`, `mvn test`, `run_tests.py`, or repository scripts.
- Playwright MCP or local Playwright tests for browser/E2E verification.
- Apifox MCP or local OpenAPI tests for API contract verification.

Archive to:

```text
06-tests/test-plan.md
06-tests/test-scripts/
06-tests/test-evidence/
06-tests/verification-report.md
```

Testing evidence must include:
- Script path or command.
- Inputs or fixtures.
- Assertions checked.
- Actual result and exit code.
- Failure and fix history.
- Explicitly skipped tests and remaining risk.

### 8. Code Review

Concrete tools:
- `ocr review --audience agent` for open-code-review.
- `ocr review --preview` before real review when scope is uncertain.
- `gsd-code-review --depth=standard` when using GSD phase artifacts.
- `gstack-review` for pre-landing review when available.
- `code-review` only when the current platform can run the required independent review lanes.

Archive to:

```text
07-review/ocr-review.md
07-review/gsd-code-review.md
07-review/gstack-review.md
07-review/fixes.md
```

Review is not complete until findings are either fixed or explicitly accepted as residual risk.

### 9. Git And Codeup Delivery

Concrete tools:
- `git status`, `git diff`, `git log`, and normal Git commands.
- `git-commit` for local commits.
- `git-commit-push-pr` or `gstack-ship` only when the user explicitly asks to push or open a PR/MR.
- Codeup uses Git for code delivery. Use Codeup/Yunxiao MCP for remote context when available, but ordinary Git remains the source of local truth.

Archive to:

```text
08-delivery/git-summary.md
08-delivery/commit-message.md
08-delivery/mr-description.md
08-delivery/release-note.md
```

Before push or MR:
- Confirm branch and target.
- Confirm no unrelated files or secrets are included.
- Confirm verification and review evidence paths.
- Ask explicit approval for the external action.

### 10. Knowledge And Graph Update

Concrete tools:
- `graphify update <project>` after meaningful code changes.
- `graphify query`, `graphify affected`, or `graphify explain` to record what changed in the code graph.
- `gsd learnings` or local documentation notes when a reusable lesson emerges.

Archive to:

```text
09-knowledge/graphify-update.md
09-knowledge/learnings.md
09-knowledge/wiki-follow-up.md
final-report.md
```

Record:
- What project knowledge changed.
- Whether the personal wiki or team docs should be updated.
- Whether Apifox, Codeup, Yuque, or other external docs need follow-up.

## Phase-To-Artifact Map

| Phase | Concrete skill or CLI | External default output | Official archive |
|---|---|---|---|
| Requirement review | `spec-flow-analyzer` | Chat output | `01-requirement-review/spec-flow-analysis.md` |
| Change spec | `openspec change`, `openspec validate` | `openspec/` files | `01-requirement-review/openspec-change.md` |
| Graph context | `graphify update/query/affected` | `graphify-out/` | `02-context/graphify-notes.md` |
| Context docs | `context7` | Chat output | `02-context/docs-references.md` |
| API contract | Apifox MCP | MCP result/cache | `02-context/apifox-contract.md` |
| Codeup context | Codeup/Yunxiao MCP | MCP result | `02-context/codeup-context.md` |
| Design | `gsd-discuss-phase`, OpenSpec | `.planning/` or `openspec/` | `03-design/design.md` |
| Plan | `superpowers:writing-plans`, `gsd-plan-phase` | `docs/superpowers/plans/`, `.planning/` | `04-plan/plan.md` |
| Execute | `superpowers:executing-plans`, `gsd-execute-phase` | changed code and plan state | `05-implementation/task-progress.md` |
| TDD | `superpowers:test-driven-development` | test files | `06-tests/test-scripts/` and `06-tests/test-evidence/` |
| Debug | `debug-hypothesis`, `systematic-debugging` | `DEBUG.md` or notes | `05-implementation/debug.md` |
| Verify | `verification-loop`, `superpowers:verification-before-completion` | command output | `06-tests/verification-report.md` |
| Review | `ocr review`, `gsd-code-review`, `gstack-review` | terminal/review files | `07-review/` |
| Commit/MR | `git-commit`, `git-commit-push-pr`, `gstack-ship` | Git and remote state | `08-delivery/` |
| Knowledge | `graphify update`, `gsd learnings` | `graphify-out/`, GSD state | `09-knowledge/` |

## Completion Checklist

Before final response:

- The run directory exists.
- Requirement, context, design, plan, tests, review, and delivery notes are archived or explicitly marked `N/A`.
- All concrete commands used are recorded.
- All test and review claims have fresh evidence.
- The Git diff was inspected.
- External actions were either approved and performed, or left as drafts.
- `final-report.md` summarizes what changed, evidence, risks, and next actions.
