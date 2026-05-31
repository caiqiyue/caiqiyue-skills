# Personal Harness MVP Overview

This MVP defines a reusable personal AI harness that can be adapted into multiple agent platforms.

The first version solves four practical problems:

1. Give the repository a stable AI entrypoint.
2. Force a single active feature at a time.
3. Separate implementation from completion.
4. Make verification evidence part of normal delivery.

The repository is split into two layers:

- `core/`: shared source of truth for rules, workflow, and project framework assets.
- `adapters/`: platform-specific packaging. This MVP ships the real Codex skill first.

The minimum project framework initialized by this harness contains:

- root entry files: `AGENTS.md`, `CLAUDE.md`
- project control plane: `.ai/`
- policies for rules and definition of done
- state files for the one active feature
- workflow guidance for planner -> implementer -> reviewer -> verifier
- verification checklist and agent-flow verification notes
- profile selection guidance

Version 1 is intentionally narrow. It optimizes for control, not automation breadth.
