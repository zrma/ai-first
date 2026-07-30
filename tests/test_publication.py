from __future__ import annotations

import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from ai_first.publication import scan_text, self_test, tracked_files


class PublicationBoundaryTest(unittest.TestCase):
    def test_self_test(self) -> None:
        self_test()

    def test_findings_do_not_repeat_content(self) -> None:
        private_path = "/" + "home" + "/named-person/source"
        findings = scan_text("artifact.md", private_path)
        self.assertEqual(
            {(item.path, item.line, item.kind) for item in findings},
            {("artifact.md", 1, "local-home-path")},
        )

    def test_tracked_files_falls_back_when_jj_is_unavailable(self) -> None:
        git_result = subprocess.CompletedProcess(
            args=["git", "ls-files"],
            returncode=0,
            stdout="README.md\nLICENSE\n",
            stderr="",
        )
        with patch(
            "ai_first.publication.subprocess.run",
            side_effect=[FileNotFoundError("jj"), git_result],
        ) as run:
            self.assertEqual(
                tracked_files(Path(".")),
                ["LICENSE", "README.md"],
            )
        self.assertEqual(run.call_count, 2)
