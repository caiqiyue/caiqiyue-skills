# Personal Harness MVP Workflow

## Standard Flow

1. Read `AGENTS.md`.
2. Read `.ai/state/active-task.md`.
3. Read `.ai/state/feature-list.json`.
4. Read `.ai/policies/global-rules.md`.
5. Read `.ai/policies/definition-of-done.md`.
6. Confirm the target profile from `.ai/profiles/profile-selection.md`.
7. Plan the single active feature.
8. Implement only that feature.
9. Review scope, boundaries, and readiness for verification.
10. Run verification and collect evidence.
11. Update state from `implemented` to `verified` only after evidence is attached.

## Initialization Flow

1. Detect the repository profile from stack markers.
2. Copy the minimum framework into project root.
3. Fill in profile-specific defaults.
4. Register the first active feature.
5. Enter the standard flow above.

## Profile Goal

The profile does not change the harness rules. It only changes:

- common stack markers
- default verification commands
- architecture notes worth reading first
