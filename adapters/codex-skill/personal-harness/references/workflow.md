# Standard Workflow

1. Planner defines one feature and its verification target.
2. Implementer changes only that feature.
3. Reviewer checks boundaries and verification readiness.
4. Verifier runs checks and records evidence.
5. State changes to `verified` only after evidence exists.

If any step fails, return to the previous responsible role. Do not skip verification.
