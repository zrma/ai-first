from __future__ import annotations

import unittest

from ai_first.publication import scan_text, self_test


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
