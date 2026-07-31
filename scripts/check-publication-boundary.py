#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "src"))

from ai_first.publication import scan_repository, scan_text, self_test  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--label", default="candidate")
    arguments = parser.parse_args()

    if arguments.self_test:
        self_test()
        print("publication boundary self-test passed")
        return 0

    if arguments.stdin:
        findings = sorted(scan_text(arguments.label, sys.stdin.read()))
    else:
        findings = sorted(scan_repository(repo_root))
    if findings:
        for finding in findings:
            print(
                f"{finding.path}:{finding.line}: publication boundary finding: "
                f"{finding.kind}",
                file=sys.stderr,
            )
        return 1

    print("repository publication boundary check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
