from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ai_first.config import ConfigError
from ai_first.render import DriftError, build, check_repository, render_repository


FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = FRAMEWORK_ROOT / "tests" / "fixtures" / "minimal"


class AiFirstTest(unittest.TestCase):
    def copy_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "consumer"
        shutil.copytree(FIXTURE_ROOT, root)
        return temporary, root

    def test_render_is_deterministic_and_checkable(self) -> None:
        temporary, root = self.copy_fixture()
        self.addCleanup(temporary.cleanup)

        first = build(root, FRAMEWORK_ROOT)
        second = build(root, FRAMEWORK_ROOT)
        self.assertEqual(first, second)
        self.assertIn(
            b"- Publication boundary check: `scripts/check-publication-boundary.py`.",
            first.outputs["docs/agent-harness.md"],
        )
        self.assertIn(
            b"VCS-isolated checkout",
            first.outputs["docs/agent-harness.md"],
        )
        self.assertIn(
            b"Git-backed checkout",
            first.outputs["AGENTS.md"],
        )
        self.assertIn(
            b"repository-native gate",
            first.outputs["docs/agent-harness.md"],
        )

        changed = render_repository(root, FRAMEWORK_ROOT)
        self.assertEqual(
            changed,
            [
                ".ai-first.lock",
                ".ai-first/check.py",
                "AGENTS.md",
                "docs/agent-harness.md",
            ],
        )
        check_repository(root, FRAMEWORK_ROOT)
        self.assertEqual(render_repository(root, FRAMEWORK_ROOT), [])

        lock = json.loads((root / ".ai-first.lock").read_text(encoding="utf-8"))
        self.assertEqual(lock["framework"]["version"], "0.1.0-dev")
        self.assertIsNone(lock["framework"]["source_revision"])
        self.assertNotIn(str(FRAMEWORK_ROOT), json.dumps(lock))

        completed = subprocess.run(
            [sys.executable, ".ai-first/check.py"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_manual_output_drift_fails(self) -> None:
        temporary, root = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        render_repository(root, FRAMEWORK_ROOT)
        (root / "AGENTS.md").write_text("manual drift\n", encoding="utf-8")

        with self.assertRaisesRegex(DriftError, "drifted AGENTS.md"):
            check_repository(root, FRAMEWORK_ROOT)

    def test_overlay_drift_fails_until_rendered(self) -> None:
        temporary, root = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        render_repository(root, FRAMEWORK_ROOT)
        overlay = root / ".ai-first" / "overlays" / "agents-project.md"
        overlay.write_text(
            overlay.read_text(encoding="utf-8") + "\n- New repository rule.\n",
            encoding="utf-8",
        )

        with self.assertRaises(DriftError):
            check_repository(root, FRAMEWORK_ROOT)
        self.assertIn("AGENTS.md", render_repository(root, FRAMEWORK_ROOT))
        check_repository(root, FRAMEWORK_ROOT)

    def test_unsafe_output_path_is_rejected(self) -> None:
        temporary, root = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        config = root / ".ai-first.toml"
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                'agents = "AGENTS.md"',
                'agents = "../AGENTS.md"',
            ),
            encoding="utf-8",
        )

        with self.assertRaises(ConfigError):
            build(root, FRAMEWORK_ROOT)

    def test_unsafe_publication_check_path_is_rejected(self) -> None:
        temporary, root = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        config = root / ".ai-first.toml"
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                'publication = "scripts/check-publication-boundary.py"',
                'publication = "../check-publication-boundary.py"',
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ConfigError, "safe repository-relative path"):
            build(root, FRAMEWORK_ROOT)

    def test_commit_source_requires_full_revision(self) -> None:
        temporary, root = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        config = root / ".ai-first.toml"
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                'source_kind = "development"',
                'source_kind = "commit"',
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ConfigError, "full lowercase source_revision"):
            build(root, FRAMEWORK_ROOT)

    def test_commit_source_rejects_other_framework_checkout(self) -> None:
        temporary, root = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        config = root / ".ai-first.toml"
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                'source_kind = "development"',
                'source_kind = "commit"\n'
                'source_revision = "0000000000000000000000000000000000000000"',
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ConfigError, "does not match source_revision"):
            build(root, FRAMEWORK_ROOT)

    def test_commit_source_records_verified_framework_revision(self) -> None:
        temporary, root = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        revision = "1" * 40
        config = root / ".ai-first.toml"
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                'source_kind = "development"',
                f'source_kind = "commit"\nsource_revision = "{revision}"',
            ),
            encoding="utf-8",
        )

        revision_result = subprocess.CompletedProcess(
            args=["git", "rev-parse", "HEAD"],
            returncode=0,
            stdout=f"{revision}\n",
            stderr="",
        )
        clean_result = subprocess.CompletedProcess(
            args=["git", "status"],
            returncode=0,
            stdout="",
            stderr="",
        )
        with patch(
            "ai_first.render.subprocess.run",
            side_effect=[revision_result, clean_result],
        ):
            lock = json.loads(build(root, FRAMEWORK_ROOT).lock)
        self.assertEqual(lock["framework"]["source_kind"], "commit")
        self.assertEqual(lock["framework"]["source_revision"], revision)

    def test_commit_source_rejects_dirty_framework_checkout(self) -> None:
        temporary, root = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        revision = "1" * 40
        config = root / ".ai-first.toml"
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                'source_kind = "development"',
                f'source_kind = "commit"\nsource_revision = "{revision}"',
            ),
            encoding="utf-8",
        )
        revision_result = subprocess.CompletedProcess(
            args=["git", "rev-parse", "HEAD"],
            returncode=0,
            stdout=f"{revision}\n",
            stderr="",
        )
        dirty_result = subprocess.CompletedProcess(
            args=["git", "status"],
            returncode=0,
            stdout=" M src/ai_first/render.py\n",
            stderr="",
        )
        with patch(
            "ai_first.render.subprocess.run",
            side_effect=[revision_result, dirty_result],
        ):
            with self.assertRaisesRegex(ConfigError, "clean framework checkout"):
                build(root, FRAMEWORK_ROOT)

    def test_output_cannot_overwrite_overlay(self) -> None:
        temporary, root = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        config = root / ".ai-first.toml"
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                'agents = "AGENTS.md"',
                'agents = ".ai-first/overlays/agents-project.md"',
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ConfigError, "must not overwrite"):
            build(root, FRAMEWORK_ROOT)

    def test_symlinked_output_cannot_escape_repository(self) -> None:
        temporary, root = self.copy_fixture()
        self.addCleanup(temporary.cleanup)
        outside = Path(temporary.name) / "outside"
        outside.mkdir()
        (root / "generated").symlink_to(outside, target_is_directory=True)
        config = root / ".ai-first.toml"
        config.write_text(
            config.read_text(encoding="utf-8").replace(
                'agents = "AGENTS.md"',
                'agents = "generated/AGENTS.md"',
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ConfigError, "inside the repository"):
            build(root, FRAMEWORK_ROOT)
