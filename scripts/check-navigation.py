#!/usr/bin/env python3
"""문서 참조와 active packet의 구조를 검증한다."""

from pathlib import Path
import re


REQUIRED_LINKS = {
    "README.md": (
        "docs/AI_FIRST_CHARTER.md", "docs/ARCHITECTURE.md", "docs/COMPATIBILITY.md",
        "docs/HANDOFF.md", "docs/roadmap.md", "docs/agent-harness.md",
        "docs/PUBLICATION.md", "docs/completed-milestones.md", "docs/WORK_LIFECYCLE.md",
    ),
    "docs/agent-harness.md": (
        "docs/AI_FIRST_CHARTER.md", "docs/ARCHITECTURE.md", "docs/COMPATIBILITY.md",
        "docs/HANDOFF.md", "docs/status.md", "docs/roadmap.md",
        "docs/PUBLICATION.md", "docs/REPO_MANIFEST.yaml",
        "docs/completed-milestones.md", "docs/WORK_LIFECYCLE.md",
    ),
}


def check_links(root: Path) -> list[str]:
    failures = []
    for source, targets in REQUIRED_LINKS.items():
        path = root / source
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for target in targets:
            if target not in text or not (root / target).is_file():
                failures.append(f"{source}: missing required document reference {target}")

    documents = [root / "README.md", root / "AGENTS.md"]
    documents += sorted((root / "docs").rglob("*.md"))
    documents += sorted((root / ".ai-first" / "overlays").glob("*.md"))
    for path in documents:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        # repository-root 기준의 명시적인 docs 경로만 검사한다. glob 예시는 제외한다.
        pattern = r"(?:`|\()(docs/[A-Za-z0-9_./-]+)(?:#[A-Za-z0-9_-]+)?(?:`|\))"
        for target in re.findall(pattern, text):
            if not (root / target).exists():
                failures.append(f"{path.relative_to(root)}: missing document {target}")

    for packet in sorted((root / "docs").glob("todo-*")):
        if packet.is_dir() and any(packet.rglob("*.md")):
            for name in ("spec.md", "open-questions.md"):
                path = packet / name
                if not path.is_file() or not path.read_text(encoding="utf-8").strip():
                    failures.append(f"{packet.relative_to(root)}: missing or empty {name}")
    return failures


if __name__ == "__main__":
    failures = check_links(Path(__file__).resolve().parents[1])
    if failures:
        raise SystemExit("\n".join(failures))
    print("repository navigation links and active packets are valid")
