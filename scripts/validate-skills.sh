#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VALIDATOR="${CODEX_SKILL_VALIDATOR:-$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py}"

if [[ -f "$VALIDATOR" ]] && python3 - <<'PY' >/dev/null 2>&1
import yaml
PY
then
  while IFS= read -r skill_dir; do
    python3 "$VALIDATOR" "$skill_dir"
  done < <(find "$ROOT/adapters/codex-skill" -mindepth 1 -maxdepth 1 -type d | sort)
else
  echo "WARN: Codex skill validator unavailable or PyYAML missing; using lightweight validation." >&2
  while IFS= read -r skill_md; do
    python3 - "$skill_md" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
content = path.read_text(encoding="utf-8")
match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
if not match:
    raise SystemExit(f"{path}: missing YAML frontmatter")
frontmatter = match.group(1)
fields = {}
for line in frontmatter.splitlines():
    if ":" in line and not line.startswith(" "):
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
name = fields.get("name", "")
description = fields.get("description", "")
if not name or not re.match(r"^[a-z0-9-]+$", name):
    raise SystemExit(f"{path}: invalid or missing name")
if not description:
    raise SystemExit(f"{path}: missing description")
print(f"{path.parent.name}: lightweight skill validation passed")
PY
  done < <(find "$ROOT/adapters/codex-skill" -mindepth 2 -maxdepth 2 -name SKILL.md -type f | sort)
fi

while IFS= read -r py_file; do
  cache_dir="$(mktemp -d)"
  PYTHONPYCACHEPREFIX="$cache_dir" python3 -m py_compile "$py_file"
  rm -rf "$cache_dir"
done < <(find "$ROOT/adapters/codex-skill" -type f -path '*/scripts/*.py' | sort)

git -C "$ROOT" diff --check

echo "Validation passed."
