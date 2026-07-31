#!/bin/sh
set -eu

repo_root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root"

scripts/ai-first check --repo .
python3 .ai-first/check.py
scripts/check-agent-harness-interface.sh
scripts/check-publication-boundary.py --self-test
scripts/check-publication-boundary.py
scripts/check-ci-contract.py

sh -n scripts/check.sh
sh -n scripts/check-agent-harness-interface.sh
sh -n scripts/ai-first

python3 - <<'PY'
import ast
from pathlib import Path

for path in sorted(Path("src").rglob("*.py")) + sorted(Path("scripts").glob("*.py")):
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

required_links = {
    "README.md": [
        "docs/AI_FIRST_CHARTER.md",
        "docs/ARCHITECTURE.md",
        "docs/COMPATIBILITY.md",
        "docs/HANDOFF.md",
        "docs/roadmap.md",
        "docs/agent-harness.md",
        "docs/PUBLICATION.md",
        "docs/completed-milestones.md",
        "docs/todo-active-work-lifecycle/spec.md",
    ],
    "docs/agent-harness.md": [
        "docs/AI_FIRST_CHARTER.md",
        "docs/ARCHITECTURE.md",
        "docs/COMPATIBILITY.md",
        "docs/HANDOFF.md",
        "docs/status.md",
        "docs/roadmap.md",
        "docs/completed-milestones.md",
        "docs/PUBLICATION.md",
        "docs/REPO_MANIFEST.yaml",
        "docs/milestones/representative-pilots/spec.md",
        "docs/milestones/stable-v1/spec.md",
        "docs/milestones/portfolio-adoption/spec.md",
        "docs/todo-active-work-lifecycle/spec.md",
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

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 -m unittest discover -s tests -p 'test_*.py'

printf 'ai-first checks passed\n'
