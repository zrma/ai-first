from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check-navigation.py"
SPEC = importlib.util.spec_from_file_location("navigation", MODULE_PATH)
assert SPEC and SPEC.loader
navigation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(navigation)


class NavigationTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for source, targets in navigation.REQUIRED_LINKS.items():
            for target in targets:
                path = self.root / target
                path.parent.mkdir(parents=True, exist_ok=True)
                if not path.exists():
                    path.write_text("# Document\n", encoding="utf-8")
            path = self.root / source
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("\n".join(f"`{target}`" for target in targets), encoding="utf-8")

    def test_completed_artifacts_need_no_archived_packet(self) -> None:
        self.assertEqual(navigation.check_links(self.root), [])

    def test_stale_reference_in_completion_summary_is_rejected(self) -> None:
        path = self.root / "docs" / "completed-milestones.md"
        path.write_text("See `docs/milestones/old/spec.md`.\n", encoding="utf-8")
        self.assertTrue(any(
            "missing document docs/milestones/old/spec.md" in failure
            for failure in navigation.check_links(self.root)
        ))

    def test_questions_without_active_spec_are_rejected(self) -> None:
        packet = self.root / "docs" / "todo-feature"
        packet.mkdir()
        (packet / "open-questions.md").write_text("# Questions\n", encoding="utf-8")
        self.assertTrue(any(
            "missing or empty spec.md" in failure
            for failure in navigation.check_links(self.root)
        ))
