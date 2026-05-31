---
name: personal-harness
description: Initialize and operate a personal AI engineering harness for a repository. Use when OpenCode or agent-compatible tools need to identify the repository profile, bootstrap a minimum `.ai` project framework, enforce the hard rules "never say complete before verification" and "only one active feature at a time", and move the user into the standard feature delivery workflow.
compatibility: opencode
---

# Personal Harness

Use this skill to turn an ordinary repository into a controlled AI engineering workspace inside OpenCode or another agent-skills compatible tool.

## Hard Rules

1. Never say work is complete before verification evidence exists.
2. Only one feature may be active at a time.

These rules override convenience. If the repository state conflicts with them, fix the control artifacts first.

## What To Do

1. Detect the repository profile.
2. Initialize the minimum project harness if `.ai/` or the entry files are missing.
3. Register exactly one active feature.
4. Move the repository into the standard workflow.

## Detect The Profile

Inspect the repository root for stack markers before writing anything.

Read `references/profile-detection.md` and classify the repository using the closest matching profile.

Minimum output from detection:

- selected profile
- key markers found
- expected verification surfaces

## Initialize The Harness

If the repository does not already have the minimum framework, copy the template from:

- `assets/project-ai-framework/AGENTS.md`
- `assets/project-ai-framework/CLAUDE.md`
- `assets/project-ai-framework/.ai/`

Keep the template minimal. Do not invent extra governance files during MVP initialization.

After copying:

1. Fill `.ai/state/active-task.md` with the selected profile.
2. Replace placeholder feature text in `.ai/state/feature-list.json`.
3. Confirm only one feature has status `active`.

Read `references/template-map.md` if you need the file-by-file purpose.

## Enter The Standard Workflow

After initialization or repair, operate in this order:

1. Read `AGENTS.md`.
2. Read `.ai/state/active-task.md`.
3. Read `.ai/state/feature-list.json`.
4. Read `.ai/policies/global-rules.md`.
5. Read `.ai/policies/definition-of-done.md`.
6. Read `.ai/workflows/feature-delivery.md`.
7. Implement only the active feature.
8. Run verification and collect evidence before saying the feature is done.

Read `references/workflow.md` for the standard flow.

## Guardrails

- If another feature is already active, do not start new work until state is repaired.
- If verification evidence is missing, say the work is implemented or pending verification, not complete.
- If the repository already has stronger local rules, follow the local rules unless they weaken the two hard rules above.
