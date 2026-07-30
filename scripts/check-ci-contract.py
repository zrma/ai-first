#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"CI contract check failed: {label}")


def main() -> int:
    workflow_path = Path(".github/workflows/ci.yml")
    dependabot_path = Path(".github/dependabot.yml")
    license_path = Path("LICENSE")
    readme_path = Path("README.md")
    manifest_path = Path("docs/REPO_MANIFEST.yaml")
    workflow = workflow_path.read_text(encoding="utf-8")
    dependabot = dependabot_path.read_text(encoding="utf-8")
    license_text = license_path.read_text(encoding="utf-8")
    readme = readme_path.read_text(encoding="utf-8")
    manifest = manifest_path.read_text(encoding="utf-8")

    require(workflow, "permissions:\n  contents: read", "read-only permissions missing")
    require(workflow, "persist-credentials: false", "checkout credentials persist")
    require(workflow, "ubuntu-24.04", "runner must be explicit")
    require(workflow, 'python-version: ["3.11", "3.14"]', "Python matrix drifted")
    require(
        workflow,
        "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
        "checkout action is not pinned",
    )
    require(
        workflow,
        "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
        "setup-python action is not pinned",
    )
    require(workflow, "run: scripts/check.sh", "canonical gate is not wired")
    if "pull_request_target" in workflow:
        raise SystemExit("CI contract check failed: pull_request_target is forbidden")

    require(dependabot, "package-ecosystem: github-actions", "Actions updates missing")
    require(dependabot, "interval: monthly", "Actions update cadence drifted")

    require(license_text, "Apache License", "Apache license heading missing")
    require(license_text, "Version 2.0, January 2004", "Apache license version missing")
    require(readme, "[Apache License 2.0](LICENSE)", "README license declaration missing")
    require(manifest, "license_status: Apache-2.0", "manifest license drifted")

    for path in ("CONTRIBUTING.md", "SECURITY.md"):
        if not Path(path).is_file():
            raise SystemExit(f"CI contract check failed: missing {path}")

    print("CI contract check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
