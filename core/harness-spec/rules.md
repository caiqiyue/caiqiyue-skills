# Personal Harness MVP Rules

## Hard Rules

1. Never say work is complete before verification evidence exists.
2. Only one feature may be active at a time.

These rules are not advisory. They must appear in both the skill instructions and the initialized project framework.

## Operational Meaning

`implemented` is not `completed`.

A feature may move through these states:

- `not_started`
- `active`
- `implemented`
- `verified`
- `blocked`

Only `verified` counts as done.

## Required Controls

- `feature-list.json` must show at most one feature with status `active`.
- `active-task.md` must name the only active feature.
- `definition-of-done.md` must require evidence, not intent.
- `checklist.md` and `verify-agent-flow.md` must be read before claiming success.
- `implementer` may change code but may not declare completion.
- `reviewer` may allow or reject verification entry but may not silently implement.
- `verifier` may promote a feature to `verified` only with evidence.
