# Platform Smoke Test

This document records a real local smoke test of the `personal-harness` assets on:

- `Codex`
- `Claude Code`
- `OpenCode`

It is intentionally practical. The goal is to show:

- where the assets were installed
- what command was used
- what happened
- how to observe whether the harness is working

## 1. Local Install Paths

### Codex

Installed to:

```text
C:\Users\Administrator\.codex\skills\personal-harness\
```

Expected files:

- `SKILL.md`
- `agents/openai.yaml`
- `references/*`
- `assets/project-ai-framework/*`

### Claude Code

Installed to:

```text
C:\Users\Administrator\.claude\plugins\local\personal-harness-plugin\
```

Expected files:

- `.claude-plugin/plugin.json`
- `skills/personal-harness/SKILL.md`
- `agents/*.md`
- `assets/project-ai-framework/*`

### OpenCode

Installed skill to:

```text
C:\Users\Administrator\.config\opencode\skills\personal-harness\
```

OpenCode CLI package was installed from npm:

```text
opencode-ai@1.15.13
```

On this machine the npm package did not create a stable `opencode.cmd` launcher automatically, so a local wrapper was added at:

```text
D:\nodejs\node_global\opencode.cmd
```

with this content:

```bat
@echo off
CALL D:\nodejs\node_global\.opencode.cmd-T71wzV4B %*
```

## 2. Test Repository

Smoke tests were executed in temporary repositories containing these markers:

- `langgraph.json`
- `manage.py`
- `package.json` with `react`
- `Dockerfile`

That combination is enough for the harness to detect:

```text
generic-full-stack-ai-app
```

## 3. Codex Result

### Command style

Codex was invoked non-interactively with `codex exec` and an instruction that explicitly referenced `personal-harness`.

### Result

Success.

Codex:

- loaded the `personal-harness` skill
- read the packaged references
- created `AGENTS.md`
- created `CLAUDE.md`
- created `.ai/`
- wrote a single active feature
- recorded the detected profile
- added verification evidence instead of claiming completion

### Observed state

Verified in the test repo:

- `AGENTS.md` exists
- `CLAUDE.md` exists
- `.ai/state/active-task.md` exists
- `.ai/state/feature-list.json` exists
- `.ai/profiles/profile-selection.md` exists
- `ACTIVE_FEATURE_COUNT=1`
- active feature name is `bootstrap-harness-validation`
- selected profile is `generic-full-stack-ai-app`

Important behavior:

- the skill did **not** mark the task complete
- it left the feature in `active` state pending verifier action

That matches the hard rule:

```text
never say complete before verification
```

## 4. Claude Code Result

### Validation

The plugin manifest was validated with:

```text
claude plugins validate C:\Users\Administrator\.claude\plugins\local\personal-harness-plugin
```

After adding `author`, validation passed cleanly.

### Command style

Claude Code was invoked with:

- `-p`
- `--dangerously-skip-permissions`
- `--plugin-dir`

and an explicit request to use the harness skill.

### Result

Success.

Claude Code:

- detected `generic-full-stack-ai-app`
- created the root entry files
- created `.ai/`
- wrote exactly one active feature
- returned a verifier-friendly summary instead of a false completion claim

### Observed state

Verified in the test repo:

- `AGENTS.md` exists
- `CLAUDE.md` exists
- `.ai/` exists
- `.ai/state/active-task.md` records the selected profile
- `.ai/state/feature-list.json` contains one active feature

## 5. OpenCode Result

### CLI status

The CLI now works locally and returns:

```text
1.15.13
```

### Provider behavior

Using `openai/gpt-5-mini` failed with:

```text
billing_not_active
```

This was not a harness problem. It was a provider/account problem.

Switching to the built-in free model worked:

```text
opencode/deepseek-v4-flash-free
```

### Command style

OpenCode was invoked with:

```text
opencode run --model opencode/deepseek-v4-flash-free "Use the personal-harness skill ..."
```

### Result

Success.

OpenCode:

- loaded `Skill "personal-harness"`
- read `references/profile-detection.md`
- read `references/template-map.md`
- created the `.ai/` directory tree
- wrote `AGENTS.md`
- wrote `CLAUDE.md`
- wrote state files
- verified that exactly one feature is active

### Observed state

Verified in the test repo:

- root files: `AGENTS.md`, `CLAUDE.md`
- `.ai/agents/*`
- `.ai/policies/*`
- `.ai/profiles/profile-selection.md`
- `.ai/state/active-task.md`
- `.ai/state/feature-list.json`
- `.ai/verify/*`
- `.ai/workflows/feature-delivery.md`

OpenCode ended with one active feature:

- id: `feature-001`
- name: `initial-harness-setup`
- status: `active`
- profile: `generic-full-stack-ai-app`

Again, it did not mark the feature verified.

## 6. How To Use It

### Codex

In a repository, ask Codex to use `personal-harness` to initialize or repair the harness.

Example intent:

```text
Use the personal-harness skill to initialize the minimum harness for this repo, record the selected profile, and keep exactly one active feature.
```

### Claude Code

Load the local plugin and ask for the same thing.

If you want a non-interactive one-shot run, use `--plugin-dir` and explicitly name the harness skill.

### OpenCode

Use a working model first. On this machine the reliable choice was:

```text
opencode/deepseek-v4-flash-free
```

Then run:

```text
opencode run --model opencode/deepseek-v4-flash-free "Use the personal-harness skill to initialize the minimum harness for this repo, record the selected profile, and keep exactly one active feature."
```

## 7. How To Observe That It Is Working

Do not trust the chat response alone. Observe the repository.

Check these files:

- `AGENTS.md`
- `CLAUDE.md`
- `.ai/state/active-task.md`
- `.ai/state/feature-list.json`
- `.ai/profiles/profile-selection.md`

You should see:

- a concrete selected profile
- exactly one active feature
- explicit scope and out-of-scope text
- verification requirements
- no false `complete` / `verified` claim without evidence

## 8. Minimum Pass Criteria

Treat the harness as installed and working only if all of these are true:

- the platform can load the skill or plugin
- the root entry files are created or respected
- `.ai/` is created or repaired
- exactly one feature is active
- profile detection is recorded
- the agent does not claim completion before verifier evidence exists

## 9. Known Caveats

- `OpenCode` may need a manual `opencode.cmd` wrapper on Windows if npm leaves only temporary launcher files.
- `OpenCode` model/provider choice matters. If one provider fails, switch to a working free model first before blaming the harness.
- `Codex` can emit unrelated warnings from other local plugins or skills. Those warnings do not necessarily mean `personal-harness` failed.

