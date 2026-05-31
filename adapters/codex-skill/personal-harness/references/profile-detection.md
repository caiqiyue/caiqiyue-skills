# Profile Detection

Look for these markers:

- orchestration: `langgraph`, `langchain`, `agents`, workflow folders
- backend: `django`, `manage.py`, `spring-boot`, `pom.xml`, `build.gradle`
- frontend: `react`, `vite`, `next`, `vue`, `package.json`
- delivery: `Dockerfile`, `docker-compose`, `k8s`, `.github/workflows`, `Jenkinsfile`

Pick the closest profile name that explains the current repository.

For MVP, a single generic profile is acceptable:

- `generic-full-stack-ai-app`

Empty repository fallback:

- If the repository root has no stack markers at all, still select `generic-full-stack-ai-app`.
- Record that the root was empty or marker-free.
- Treat the verification surface as the harness control files themselves.

Record:

- selected profile
- evidence for the selection
- verification surfaces implied by the stack
