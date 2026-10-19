from __future__ import annotations

import os
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from ai_first import vcs

from ai_first.config import ConfigError
from ai_first.render import render_repository


FRAMEWORK = Path(__file__).resolve().parents[1]
CHECK = FRAMEWORK / "src/ai_first/vcs.py"


class RepositoryTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vcs-contract-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.env.pop("AI_FIRST_VCS_REVISION", None)

    def run_command(self, *args, ok=True):
        result = subprocess.run(args, cwd=self.root, env=self.env, text=True, capture_output=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result

    def check(self, *args, ok=True):
        result = self.run_command("python3", str(CHECK), "--repo-root", str(self.root), *args, ok=False)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result


class GitRepository(RepositoryTest):
    def setUp(self):
        super().setUp()
        self.run_command("git", "init", "-q", "--initial-branch=main")
        self.run_command("git", "config", "user.name", "Fixture")
        self.run_command("git", "config", "user.email", "fixture@example.test")
        self.run_command("git", "config", "commit.gpgsign", "false")
        self.commit("baseline")

    def commit(self, name):
        (self.root / name).write_text(name)
        self.run_command("git", "add", name)
        self.run_command("git", "commit", "-qm", f"test: {name}")

    def merge(self):
        self.run_command("git", "checkout", "-qb", "side")
        self.commit("side")
        self.run_command("git", "checkout", "-q", "main")
        self.commit("main")
        self.run_command("git", "merge", "--no-ff", "side", "-qm", "test: merge")

class GitHistoryTests(GitRepository):
    def test_linear_history_passes_and_merge_fails(self):
        self.check()
        self.merge()
        self.assertIn("merge commits", self.check(ok=False).stderr)

    def test_proposed_revision_is_checked_even_when_main_is_linear(self):
        initial = self.run_command("git", "rev-parse", "HEAD").stdout.strip()
        self.merge()
        merged = self.run_command("git", "rev-parse", "HEAD").stdout.strip()
        self.run_command("git", "checkout", "-q", "--detach", initial)
        self.run_command("git", "branch", "-f", "main", initial)
        self.check()
        self.check("--revision", merged, ok=False)

    def test_unrelated_release_tag_does_not_break_linear_main(self):
        initial = self.run_command("git", "rev-parse", "HEAD").stdout.strip()
        self.merge()
        self.run_command("git", "tag", "v0.0.1")
        self.run_command("git", "checkout", "-q", "--detach", initial)
        self.run_command("git", "branch", "-f", "main", initial)
        self.check()
        self.assertTrue(self.run_command("git", "rev-parse", "v0.0.1").stdout.strip())

    def test_shallow_clone_cannot_prove_linearity(self):
        self.commit("later")
        clone = self.base / "shallow"
        self.run_command("git", "clone", "-q", "--depth=1", self.root.as_uri(), str(clone))
        self.root = clone
        self.assertIn("full history", self.check(ok=False).stderr)

    def test_detached_ci_uses_origin_main_and_missing_revision_fails(self):
        self.run_command("git", "update-ref", "refs/remotes/origin/main", "HEAD")
        self.run_command("git", "checkout", "-q", "--detach")
        self.run_command("git", "branch", "-D", "main")
        self.check()
        self.check("--revision", "missing", ok=False)

    def test_legacy_checkpoint_preserves_old_merge_but_rejects_a_new_one(self):
        self.merge()
        checkpoint = self.run_command("git", "rev-parse", "HEAD").stdout.strip()
        (self.root / ".ai-first.toml").write_text(f'[vcs]\nlinear_history_base = "{checkpoint}"\n')
        self.check()
        self.run_command("git", "checkout", "-qb", "later-side")
        self.commit("later-side")
        self.run_command("git", "checkout", "-q", "main")
        self.commit("later-main")
        self.run_command("git", "merge", "--no-ff", "later-side", "-qm", "test: later merge")
        self.check(ok=False)

    def test_checkpoint_must_be_an_ancestor(self):
        self.run_command("git", "checkout", "-qb", "side")
        self.commit("side")
        other = self.run_command("git", "rev-parse", "HEAD").stdout.strip()
        self.run_command("git", "checkout", "-q", "main")
        self.assertIn("not an ancestor", self.check("--base", other, ok=False).stderr)

    def test_malformed_policy_is_rejected(self):
        (self.root / ".ai-first.toml").write_text('[vcs]\nlinear_history_base = "short"\n')
        self.assertIn("full lowercase", self.check(ok=False).stderr)


@unittest.skipUnless(shutil.which("jj"), "jj is required for native closeout tests")
class JujutsuCloseoutTests(RepositoryTest):
    def setUp(self):
        super().setUp()
        self.run_command("jj", "git", "init", "--colocate")
        for key, value in (("user.name", "Fixture"), ("user.email", "fixture@example.test"), ("signing.behavior", "drop")):
            self.run_command("jj", "config", "set", "--repo", key, value)
        (self.root / "baseline").write_text("baseline")
        self.run_command("jj", "describe", "-m", "test: baseline")
        self.run_command("jj", "bookmark", "create", "main", "-r", "@")
        self.run_command("jj", "new", "main")

    def value(self, revision, template):
        return self.run_command("jj", "log", "-r", revision, "--no-graph", "-T", template).stdout.strip()

    def test_clean_default_passes_but_dirty_or_wrong_parent_fails(self):
        self.check("--closeout")
        (self.root / "pending").write_text("keep")
        self.assertIn("not empty", self.check("--closeout", ok=False).stderr)
        self.run_command("jj", "new")
        self.assertIn("expected parent", self.check("--closeout", ok=False).stderr)
        self.check("--closeout", "--revision", "@-")
        self.assertEqual((self.root / "pending").read_text(), "keep")

    def test_legacy_current_workspace_uses_verified_root_but_unknown_secondary_fails(self):
        original = vcs.jj
        def legacy(root, *args):
            result = original(root, *args)
            if args[:2] == ("workspace", "list"):
                result = "\n".join("\0".join((row[0], "", row[2])) for row in (line.split("\0") for line in result.splitlines()))
            return result
        target = self.value("main", "commit_id")
        with patch.object(vcs, "jj", side_effect=legacy):
            vcs.check_closeout(self.root, target, {"default"}, [])
        active = self.base / "active"
        self.run_command("jj", "workspace", "add", "--name", "active", "-r", "main", str(active))
        with patch.object(vcs, "jj", side_effect=legacy):
            with self.assertRaisesRegex(vcs.StateError, "root metadata"):
                vcs.check_closeout(self.root, target, {"default", "active"}, [])
        self.assertTrue(active.is_dir())

    def test_secondary_workspace_requires_explicit_retention_and_is_not_deleted(self):
        path = self.base / "active"
        self.run_command("jj", "workspace", "add", "--name", "active", "-r", "main", str(path))
        self.assertIn("secondary workspaces", self.check("--closeout", ok=False).stderr)
        self.check("--closeout", "--keep-workspace", "active")
        self.assertTrue(path.is_dir())

    def test_unreferenced_nonempty_head_requires_preservation(self):
        (self.root / "unique").write_text("preserve")
        self.run_command("jj", "describe", "-m", "test: unique work")
        tip = self.value("@", "commit_id")
        self.run_command("jj", "new", "main")
        self.assertIn("unreferenced heads", self.check("--closeout", ok=False).stderr)
        self.run_command("jj", "bookmark", "create", "feature/retained", "-r", tip)
        self.check("--closeout")
        self.assertIn("preserve", self.run_command("jj", "file", "show", "-r", tip, "unique").stdout)

    def test_unreferenced_empty_head_is_also_detected(self):
        self.run_command("jj", "new", "main", "-m", "test: unused empty head")
        self.run_command("jj", "new", "main")
        self.assertIn("unreferenced heads", self.check("--closeout", ok=False).stderr)

    def test_retired_clone_directory_and_dangling_link_are_detected(self):
        clone = self.base / "retired-clone"
        clone.mkdir()
        self.check("--closeout", "--retired-path", str(clone), ok=False)
        self.assertTrue(clone.is_dir())
        clone.rmdir()
        self.check("--closeout", "--retired-path", str(clone))
        clone.symlink_to(self.base / "absent")
        self.check("--closeout", "--retired-path", str(clone), ok=False)

    def test_git_worktree_registration_is_checked_separately(self):
        path = self.base / "git-only"
        self.run_command("git", "worktree", "add", "--detach", str(path), "main")
        self.assertIn("Git worktree", self.check("--closeout", ok=False).stderr)
        shutil.rmtree(path)
        self.assertIn("Git worktree", self.check("--closeout", ok=False).stderr)

    def test_exact_inherited_working_copy_is_preserved_and_changes_are_detected(self):
        path = self.root / "user-work"
        path.write_text("preserve")
        original = self.value("@", "commit_id")
        self.check("--closeout", "--inherited-working-copy", original)
        self.assertEqual(path.read_text(), "preserve")
        path.write_text("new user edit")
        self.assertIn("inherited working copy changed", self.check("--closeout", "--inherited-working-copy", original, ok=False).stderr)
        self.assertEqual(path.read_text(), "new user edit")

    def test_classified_preexisting_head_and_git_worktree_are_retained(self):
        (self.root / "unique").write_text("user history")
        head = self.value("@", "commit_id")
        self.run_command("jj", "new", "main")
        worktree = self.base / "retained-git"
        self.run_command("git", "worktree", "add", "--detach", str(worktree), "main")
        self.check("--closeout", "--keep-head", head, "--keep-worktree", str(worktree))
        self.assertTrue(worktree.exists())
        self.assertIn("user history", self.run_command("jj", "file", "show", "-r", head, "unique").stdout)

    def test_native_checkpoint_preserves_existing_merge(self):
        (self.root / "left").write_text("left")
        left = self.value("@", "commit_id")
        self.run_command("jj", "new", "main")
        (self.root / "right").write_text("right")
        right = self.value("@", "commit_id")
        self.run_command("jj", "new", left, right)
        merged = self.value("@", "commit_id")
        self.run_command("jj", "bookmark", "set", "main", "-r", merged)
        self.check(ok=False)
        self.check("--base", merged)


class CapabilityTests(GitRepository):
    def install(self):
        fixture = FRAMEWORK / "tests/fixtures/minimal"
        shutil.copytree(fixture, self.root, dirs_exist_ok=True)
        path = self.root / ".ai-first.toml"
        path.write_text(path.read_text().replace('"public-repository"]', '"public-repository", "vcs-closeout"]'))
        render_repository(self.root, FRAMEWORK)

    def standalone(self, **env):
        return subprocess.run(["python3", ".ai-first/check.py"], cwd=self.root, env=dict(self.env, **env), capture_output=True, text=True)

    def test_generated_runtime_is_locked_and_runs_in_standalone(self):
        self.install()
        self.assertTrue((self.root / ".ai-first/vcs.py").is_file())
        self.assertEqual(self.standalone().returncode, 0)
        self.merge()
        self.assertNotEqual(self.standalone().returncode, 0)

    def test_ci_binding_checks_the_proposed_revision(self):
        self.install()
        self.run_command("git", "add", ".")
        self.run_command("git", "commit", "-qm", "test: installed contract")
        initial = self.run_command("git", "rev-parse", "HEAD").stdout.strip()
        self.merge()
        proposed = self.run_command("git", "rev-parse", "HEAD").stdout.strip()
        self.run_command("git", "checkout", "-q", "--detach", initial)
        self.run_command("git", "branch", "-f", "main", initial)
        self.assertEqual(self.standalone().returncode, 0)
        result = self.standalone(AI_FIRST_VCS_REVISION=proposed)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("merge commits", result.stderr)

    def test_missing_locked_runtime_fails_before_execution(self):
        self.install()
        path = self.root / ".ai-first.lock"
        lock = json.loads(path.read_text())
        del lock['outputs']['.ai-first/vcs.py']
        path.write_text(json.dumps(lock))
        result = self.standalone()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("locked VCS runtime", result.stdout)

    def test_opt_out_preserves_a_modified_runtime(self):
        self.install()
        runtime = self.root / '.ai-first/vcs.py'
        runtime.write_text('user modification\n')
        path = self.root / '.ai-first.toml'
        path.write_text(path.read_text().replace(', "vcs-closeout"', ''))
        with self.assertRaisesRegex(ConfigError, "modified optional"):
            render_repository(self.root, FRAMEWORK)
        self.assertEqual(runtime.read_text(), 'user modification\n')

    def test_capability_requires_jj_profile(self):
        self.install()
        path = self.root / '.ai-first.toml'
        path.write_text(path.read_text().replace('"vcs-jj", ', ''))
        with self.assertRaisesRegex(ConfigError, "requires the vcs-jj"):
            render_repository(self.root, FRAMEWORK)



if __name__ == "__main__":
    unittest.main()
