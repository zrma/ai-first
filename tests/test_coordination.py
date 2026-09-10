from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ai_first import coordination as work
from ai_first import verification
from ai_first.config import ConfigError
from ai_first.render import render_repository

FRAMEWORK = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("jj"), "coordination integration requires jj")
class CoordinationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "source"
        shutil.copytree(FRAMEWORK / "tests/fixtures/minimal", self.root)
        (self.root / ".gitignore").write_text("__pycache__/\n")
        config = self.root / ".ai-first.toml"
        config.write_text(config.read_text().replace('"public-repository"]', '"public-repository", "verification", "work-coordination"]'))
        (self.root / "left.py").write_text("value = 0\n")
        (self.root / "right.py").write_text("value = 0\n")
        (self.root / "policy.txt").write_text("preserve\n")
        text = "schema_version = 1\n"
        for name, code in [("left", "import left; assert left.value == 1"), ("right", "import right; assert right.value == 1"), ("combined", "import left,right; assert left.value + right.value == 2")]:
            text += f'\n[[checks]]\nid = "{name}"\nargv = {json.dumps([sys.executable, "-c", code])}\ncoverage = ["{name} behavior"]\n'
        (self.root / verification.BINDING).write_text(text)
        render_repository(self.root, FRAMEWORK)
        configuration = self.base / "jj-config.toml"
        configuration.write_text('[user]\nname = "Workflow Fixture"\nemail = "workflow@example.invalid"\n[signing]\nbehavior = "drop"\n')
        environment = patch.dict(os.environ, {"JJ_CONFIG": str(configuration)})
        environment.start()
        self.addCleanup(environment.stop)
        work.command(self.root, ["jj", "git", "init", "--colocate"])
        self.state = self.base / "state"
        work.initialize(self.root, self.state, "Implement both values", ["left.py", "right.py"])

    def assign(self, name):
        return work.assign(self.state, name, f"Implement {name}", [name + ".py"], [name])

    def handoff(self, name):
        with contextlib.redirect_stderr(io.StringIO()):
            return work.handoff(self.state, name)

    def integrate(self):
        with contextlib.redirect_stderr(io.StringIO()):
            return work.integrate(self.state)

    def prepared(self):
        for name in ["left", "right"]:
            packet = self.assign(name)
            (Path(packet["workspace"]) / (name + ".py")).write_text("value = 1\n")
            self.assertEqual(self.handoff(name)["status"], "handed_off")

    def test_two_real_clones_integrate_without_changing_source(self):
        before = verification.snapshot(self.root)
        self.prepared()
        result = self.integrate()
        self.assertEqual(result["status"], "verified", result)
        integration = Path(result["integration"]["workspace"])
        self.assertEqual((integration / "left.py").read_text(), "value = 1\n")
        self.assertEqual((integration / "right.py").read_text(), "value = 1\n")
        self.assertEqual(verification.snapshot(self.root), before)
        self.assertEqual(work.load(self.state)["phase"], "verified")

    def test_assignment_overlap_and_scope_expansion_rejected(self):
        self.assign("left")
        for name, scope in [("duplicate", ["left.py"]), ("outside", ["policy.txt"])]:
            with self.assertRaises(work.WorkError):
                work.assign(self.state, name, "Edit", scope, ["left"])
            self.assertFalse((self.state / name).exists())

    def test_out_of_scope_worker_change_rejected(self):
        packet = self.assign("left")
        root = Path(packet["workspace"])
        (root / "left.py").write_text("value = 1\n")
        (root / "policy.txt").write_text("changed\n")
        with self.assertRaisesRegex(work.WorkError, "outside"):
            self.handoff("left")
        self.assertEqual((self.root / "policy.txt").read_text(), "preserve\n")

    def test_missing_handoff_and_failed_check_do_not_integrate(self):
        packet = self.assign("left")
        with self.assertRaises(work.WorkError):
            self.integrate()
        self.assertEqual(self.handoff("left")["status"], "failed")
        (Path(packet["workspace"]) / "left.py").write_text("value = 1\n")
        self.assertEqual(self.handoff("left")["status"], "handed_off")

    def test_worker_revision_change_invalidates_handoff(self):
        self.prepared()
        (self.state / "left/left.py").write_text("value = 2\n")
        with self.assertRaisesRegex(work.WorkError, "after handoff"):
            self.integrate()

    def test_source_advancement_blocks_integration(self):
        self.prepared()
        (self.root / "policy.txt").write_text("source advanced\n")
        with self.assertRaisesRegex(work.WorkError, "source advanced"):
            self.integrate()
        self.assertFalse((self.state / "integration-1").exists())

    def test_native_combined_semantic_failure_is_executed(self):
        # 각 worker에 성공한 좁은 검증과 전체 검증의 차이를 실제 subprocess로 확인한다.
        text = (self.root / verification.BINDING).read_text()
        text = text.replace("left.value + right.value == 2", "left.value + right.value == 3")
        # 이 테스트만의 source acceptance를 작업 시작 상태에 일관되게 반영한다.
        other = self.base / "semantic-source"
        shutil.copytree(self.root, other, ignore=shutil.ignore_patterns(".git", ".jj", "__pycache__"))
        (other / verification.BINDING).write_text(text)
        render_repository(other, FRAMEWORK)
        work.command(other, ["jj", "git", "init", "--colocate"])
        semantic_state = self.base / "semantic-state"
        work.initialize(other, semantic_state, "Combined behavior", ["left.py", "right.py"])
        for name in ["left", "right"]:
            packet = work.assign(semantic_state, name, name, [name + ".py"], [name])
            (Path(packet["workspace"]) / (name + ".py")).write_text("value = 1\n")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(work.handoff(semantic_state, name)["status"], "handed_off")
        with contextlib.redirect_stderr(io.StringIO()):
            result = work.integrate(semantic_state)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["integration"]["report"]["checks"][-1]["exit_code"], 1)

    def test_resume_preserves_worker_files_and_attempt_history(self):
        packet = self.assign("left")
        root = Path(packet["workspace"])
        (root / "left.py").write_text("value = 1\n")
        state = work.load(self.state)
        state["tasks"]["left"]["status"] = "checking"
        work.save(self.state, state)
        restored = work.resume(self.state, "left")
        self.assertEqual(restored["workspace"], str(root))
        self.assertEqual((root / "left.py").read_text(), "value = 1\n")
        self.assertEqual(self.handoff("left")["status"], "handed_off")

    def test_standalone_packet_and_status_need_no_framework_checkout(self):
        packet = self.assign("left")
        root = Path(packet["workspace"])
        completed = subprocess.run([sys.executable, ".ai-first/work.py", "packet", "--state", str(self.state), "--id", "left"], cwd=root, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["write_scope"], ["left.py"])
        check = subprocess.run([sys.executable, ".ai-first/check.py"], cwd=root, capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_private_state_and_live_lock_are_protected(self):
        with self.assertRaises(work.WorkError):
            work.initialize(self.root, self.root / "state", "test", ["left.py"])
        with work.locked(self.state):
            with self.assertRaises(work.WorkError):
                work.unlock(self.state)
            with self.assertRaises(work.WorkError):
                self.assign("left")


class CoordinationDistributionTests(unittest.TestCase):
    def test_dependency_collision_and_opt_out_preserve_owned_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(FRAMEWORK / "tests/fixtures/minimal", root, dirs_exist_ok=True)
            config = root / ".ai-first.toml"
            original = config.read_text()
            config.write_text(original.replace('"public-repository"]', '"public-repository", "work-coordination"]'))
            with self.assertRaisesRegex(ConfigError, "requires"):
                render_repository(root, FRAMEWORK)
            enabled = original.replace('"public-repository"]', '"public-repository", "verification", "work-coordination"]')
            config.write_text(enabled)
            runtime = root / ".ai-first/work.py"
            runtime.write_text("repository owned")
            with self.assertRaisesRegex(ConfigError, "ownership"):
                render_repository(root, FRAMEWORK)
            self.assertEqual(runtime.read_text(), "repository owned")
            runtime.unlink()
            render_repository(root, FRAMEWORK)
            skill = root / ".agents/skills/ai-first-work/SKILL.md"
            generated = skill.read_text()
            skill.write_text("local change")
            config.write_text(enabled.replace(', "work-coordination"', ''))
            with self.assertRaisesRegex(ConfigError, "preserved"):
                render_repository(root, FRAMEWORK)
            self.assertEqual(skill.read_text(), "local change")
            skill.write_text(generated)
            render_repository(root, FRAMEWORK)
            self.assertFalse(runtime.exists())
            self.assertFalse(skill.exists())
            self.assertTrue((root / ".ai-first/verify.py").is_file())
