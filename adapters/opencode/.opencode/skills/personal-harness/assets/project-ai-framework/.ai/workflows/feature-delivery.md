# Feature Delivery Workflow

## Sequence

1. Planner defines the single feature, scope, non-goals, and verification target.
2. Implementer changes code only for that feature.
3. Reviewer checks scope fit, boundary safety, and verification readiness.
4. Verifier runs the required checks and records evidence.
5. State moves to `verified` only after evidence exists.

## Handback Rules

- If scope is unclear, go back to planning.
- If implementation is wrong, go back to implementer.
- If verification fails, go back to implementer.
- If definition of done is unclear, fix policy before claiming success.
