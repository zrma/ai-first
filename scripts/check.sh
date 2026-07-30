#!/bin/sh
set -eu

repo_root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root"

scripts/check-agent-harness-interface.sh

sh -n scripts/check.sh
sh -n scripts/check-agent-harness-interface.sh

python3 - <<'PY'
from pathlib import Path

required_links = {
    "README.md": [
        "docs/AI_FIRST_CHARTER.md",
        "docs/ARCHITECTURE.md",
        "docs/HANDOFF.md",
        "docs/roadmap.md",
        "docs/agent-harness.md",
        "docs/PUBLICATION.md",
        "docs/todo-bootstrap-core/spec.md",
    ],
    "docs/agent-harness.md": [
        "docs/AI_FIRST_CHARTER.md",
        "docs/ARCHITECTURE.md",
        "docs/HANDOFF.md",
        "docs/status.md",
        "docs/roadmap.md",
        "docs/PUBLICATION.md",
        "docs/REPO_MANIFEST.yaml",
        "docs/todo-bootstrap-core/spec.md",
    ],
}

for source, targets in required_links.items():
    text = Path(source).read_text(encoding="utf-8")
    for target in targets:
        if target not in text:
            raise SystemExit(f"{source} does not reference {target}")
        if not Path(target).is_file():
            raise SystemExit(f"{source} references missing file {target}")

print("repository navigation links are valid")
PY

printf 'ai-first bootstrap checks passed\n'
