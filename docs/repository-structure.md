# Repository Structure

This repo separates reusable knowledge from platform-specific delivery artifacts.

## Ownership Rules

| Path | Owner | What Belongs Here |
|---|---|---|
| `core/` | Platform-neutral source | Shared rules, workflow ideas, templates, and profile notes that can feed multiple adapters. |
| `adapters/codex-skill/` | Codex | One directory per installable Codex skill. Each skill must contain `SKILL.md`; `agents/openai.yaml`, `scripts/`, `references/`, and `assets/` are optional. |
| `adapters/claude-plugin/` | Claude Code | Plugin-style bundles, Claude agents, skills, and assets. |
| `adapters/opencode/` | OpenCode | OpenCode config, skills, agents, and plugin files. |
| `adapters/agent-skills/` | Generic agent skill format | Skills that use a `.agents/skills` style layout but are not installed from the repository root. |
| `docs/` | Human documentation | Architecture, usage, delivery plans, and smoke-test notes. |
| `scripts/` | Repo maintenance | Validation, sync, and release helpers. |

## Current Adapter Inventory

### Codex

- `external-feature-flow`
- `paper-ai-review`
- `personal-harness`
- `project-ai-dev-init`
- `word-doc-editor`

### Claude Code

- `personal-harness-plugin`

### OpenCode

- `personal-harness`
- `harness-guard`

### Generic Agent Skills

- `content-builder`

## Structure Decisions

- The repository root should not contain a live `.agents/` directory. Generic agent-skill assets live under `adapters/agent-skills/` so the root stays platform-neutral.
- Adapter outputs may duplicate content from `core/` while the sync scripts are still immature. When a shared rule changes, update the adapter copies intentionally and validate each platform.
- Skill directories should not contain generated caches such as `__pycache__/`.
- New Codex skills should be created under `adapters/codex-skill/<skill-name>/` and then synced to `~/.codex/skills/<skill-name>/` only for local testing.
