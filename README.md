# caiqiyue-skills

Personal AI engineering skills and adapters.

This repository is organized as a small skill monorepo. It keeps reusable design assets in `core/`, platform-specific installable artifacts in `adapters/`, operating notes in `docs/`, and repository maintenance helpers in `scripts/`.

## Repository Layout

```text
caiqiyue-skills/
├─ adapters/
│  ├─ codex-skill/       # Installable Codex skills
│  ├─ claude-plugin/     # Claude Code plugin bundle
│  ├─ opencode/          # OpenCode adapter bundle
│  └─ agent-skills/      # Generic .agents-style skills kept as adapter assets
├─ core/
│  ├─ harness-spec/      # Platform-neutral harness rules and workflow notes
│  └─ templates/         # Shared project framework templates
├─ docs/                 # Design, usage, and delivery documentation
├─ scripts/              # Validation and maintenance helpers
└─ package.json          # Lightweight inventory metadata
```

See [docs/repository-structure.md](docs/repository-structure.md) for the file ownership rules.

## Main Codex Skills

| Skill | Purpose |
|---|---|
| `project-ai-dev-init` | Initialize a real project with `.ai-dev`, shared Codex/Claude entries, MCP notes, gates, and run templates. |
| `external-feature-flow` | Standard existing-project feature workflow using external tools such as OpenSpec, GSD, Superpowers, Graphify, OCR, Apifox, Codeup, and Git. |
| `personal-harness` | Earlier minimal personal harness skill using `.ai` controls. |
| `paper-ai-review` | Review paper drafts for AI-writing tells. |
| `word-doc-editor` | Rewrite AI drafts into readable workplace documents. |

## Platform Adapters

- Codex skills: [adapters/codex-skill](adapters/codex-skill)
- Claude Code plugin: [adapters/claude-plugin/personal-harness-plugin](adapters/claude-plugin/personal-harness-plugin)
- OpenCode adapter: [adapters/opencode](adapters/opencode)
- Generic agent-skill assets: [adapters/agent-skills](adapters/agent-skills)

## Validation

Run:

```bash
bash scripts/validate-skills.sh
```

The script validates Codex skill frontmatter with the local Codex skill validator when it is available, checks Python helper scripts, and catches whitespace errors with `git diff --check`.

## Current Status

The most actively maintained Codex skills are:

1. `project-ai-dev-init`
2. `external-feature-flow`

The older `personal-harness` adapters remain in the repository because they document the first cross-platform harness design and still provide useful references. New day-to-day feature work should usually use `external-feature-flow` unless the target project needs the heavier `.ai-dev` framework from `project-ai-dev-init`.

## Installation Notes

For local Codex testing, copy one skill directory into `~/.codex/skills/`, for example:

```bash
rsync -a --delete adapters/codex-skill/external-feature-flow/ ~/.codex/skills/external-feature-flow/
```

Do not store API keys or tokens in this repository. Use local environment files or the runtime's secret configuration.
