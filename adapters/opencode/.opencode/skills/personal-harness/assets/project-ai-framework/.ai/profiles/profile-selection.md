# Profile Selection

Choose the profile that best matches repository markers.

## Generic Full-Stack AI App

Use this profile when the repository includes some combination of:

- `langgraph.json`, `langchain`, or agent orchestration code
- `django`, `spring-boot`, `pom.xml`, or backend service folders
- `react`, `vite`, `next`, `vue`, or frontend app folders
- `docker`, `k8s`, `helm`, or CI delivery files

## Process

1. Inspect top-level files and package manifests.
2. Pick the closest profile.
3. Write the chosen profile name into `.ai/state/active-task.md`.
4. Add profile-specific verification commands to the active feature record.
