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
PY

python3 scripts/check-navigation.py

if [ "${AI_FIRST_REQUIRE_JJ_TESTS:-0}" = 1 ]; then
  command -v jj >/dev/null || { printf 'jj integration tests require jj\n' >&2; exit 1; }
fi

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 -m unittest discover -s tests -p 'test_*.py'

printf 'ai-first checks passed\n'
