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
        result = self.run_command("python3", str(CHECK), *args, "--repo-root", str(self.root), ok=False)
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

    def session(self, action, *args, ok=True):
        return self.check(action, "--state", str(self.base / "session.json"), *args, ok=ok)

    def candidate(self):
        (self.root / "result").write_text("completed")
        self.run_command("jj", "describe", "-m", "test: completed")
        return self.value("@", "commit_id")

    def publish_local(self, candidate):
        self.run_command("jj", "bookmark", "set", "main", "-r", candidate)
        self.run_command("jj", "new", "main")

    def test_session_start_is_private_and_cannot_be_overwritten(self):
        self.session("start")
        path = self.base / "session.json"
        original = path.read_bytes()
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.session("start", ok=False)
        self.assertEqual(path.read_bytes(), original)
        self.check("start", "--state", str(self.root / "session.json"), ok=False)
        link = self.base / "link.json"
        link.symlink_to(path)
        self.check("start", "--state", str(link), ok=False)

    def test_session_requires_completed_durable_candidate_and_empty_working_copy(self):
        self.session("start")
        self.session("finish", ok=False)
        candidate = self.candidate()
        self.session("integrate", "--revision", candidate)
        self.assertIn("durable bookmark", self.session("finish", ok=False).stderr)
        self.run_command("jj", "bookmark", "set", "main", "-r", candidate)
        self.assertIn("not empty", self.session("finish", ok=False).stderr)
        self.run_command("jj", "new")
        self.session("finish")
        self.session("finish", ok=False)

    def test_session_keeps_an_inherited_empty_copy_on_unique_work(self):
        self.candidate()
        self.run_command("jj", "new")
        inherited = self.value("@", "commit_id")
        self.session("start")
        self.session("integrate", "--revision", "main")
        self.session("finish")
        self.assertEqual(self.value("@", "commit_id"), inherited)

    def test_native_resume_rejects_missing_or_finished_session(self):
        self.session("resume", ok=False)
        self.session("start")
        self.session("resume")
        self.session("integrate", "--revision", "main")
        self.session("finish")
        self.session("resume", ok=False)

    def test_session_preserves_main_without_publication_permission(self):
        initial = self.value("main", "commit_id")
        self.session("start")
        candidate = self.candidate()
        self.session("integrate", "--revision", candidate)
        self.run_command("jj", "bookmark", "create", "feature/completed", "-r", candidate)
        self.run_command("jj", "new")
        self.session("finish")
        self.assertEqual(self.value("main", "commit_id"), initial)

    def test_session_rejects_divergence_before_bookmark_move(self):
        self.session("start")
        candidate = self.candidate()
        self.run_command("jj", "new", "main")
        (self.root / "result").write_text("concurrent")
        concurrent = self.value("@", "commit_id")
        self.run_command("jj", "bookmark", "set", "main", "-r", concurrent)
        self.assertIn("extend current main", self.session("integrate", "--revision", candidate, ok=False).stderr)
        self.assertEqual(self.value("main", "commit_id"), concurrent)

    def test_session_rejects_linear_conflicted_candidate(self):
        self.session("start")
        (self.root / "baseline").write_text("left")
        self.run_command("jj", "describe", "-m", "test: left")
        left = self.value("@", "change_id")
        self.run_command("jj", "new", "main")
        (self.root / "baseline").write_text("right")
        self.run_command("jj", "describe", "-m", "test: right")
        right = self.value("@", "commit_id")
        self.run_command("jj", "bookmark", "set", "main", "-r", right)
        self.run_command("jj", "rebase", "-s", left, "-o", right)
        self.assertIn("unresolved conflicts", self.session("integrate", "--revision", left, ok=False).stderr)
        self.assertEqual(self.value("main", "commit_id"), right)

    def test_session_owns_copy_before_creation_and_checks_registration_and_directory(self):
        self.session("start")
        self.session("own", "--path", str(self.root), ok=False)
        copy = self.base / "copy"
        self.session("own", "--path", str(copy))
        self.run_command("jj", "workspace", "add", "--name", "task", "-r", "main", str(copy))
        canonical = self.root
        self.root = copy
        candidate = self.candidate()
        self.session("integrate", "--revision", "@")
        self.root = canonical
        self.publish_local(candidate)
        self.assertIn("secondary workspaces", self.session("finish", ok=False).stderr)
        self.run_command("jj", "workspace", "forget", "task")
        self.assertIn("still exists", self.session("finish", ok=False).stderr)
        shutil.rmtree(copy)
        self.session("finish")

    def test_session_retains_inherited_wip_and_release_history(self):
        self.run_command("jj", "tag", "set", "v0.0.1", "-r", "main")
        (self.root / "wip").write_text("must survive")
        inherited = self.value("@", "commit_id")
        self.session("start")
        copy = self.base / "copy"
        self.session("own", "--path", str(copy))
        self.run_command("jj", "workspace", "add", "--name", "task", "-r", "main", str(copy))
        canonical = self.root
        self.root = copy
        candidate = self.candidate()
        self.session("integrate", "--revision", candidate)
        self.root = canonical
        self.run_command("jj", "bookmark", "set", "main", "-r", candidate)
        self.run_command("jj", "workspace", "forget", "task")
        shutil.rmtree(copy)
        self.session("finish")
        self.assertEqual(self.value("@", "commit_id"), inherited)
        self.assertEqual((self.root / "wip").read_text(), "must survive")
        self.assertTrue(self.value("tags()", "commit_id"))

    def test_session_detects_inherited_wip_and_tag_mutation(self):
        self.run_command("jj", "tag", "set", "v0.0.1", "-r", "main")
        (self.root / "wip").write_text("existing")
        self.session("start")
        candidate = self.value("main", "commit_id")
        self.session("integrate", "--revision", candidate)
        (self.root / "wip").write_text("modified")
        self.assertIn("inherited working copy changed", self.session("finish", ok=False).stderr)
        self.run_command("jj", "tag", "delete", "v0.0.1")
        self.assertIn("release tags changed", self.session("finish", ok=False).stderr)

    def test_session_detects_new_orphan_heads_and_unregistered_clone(self):
        self.session("start")
        copy = self.base / "clone"
        self.session("own", "--path", str(copy))
        copy.mkdir()
        candidate = self.candidate()
        self.session("integrate", "--revision", candidate)
        self.publish_local(candidate)
        self.assertIn("still exists", self.session("finish", ok=False).stderr)
        copy.rmdir()
        self.run_command("jj", "new", "main")
        (self.root / "orphan").write_text("unique")
        self.run_command("jj", "new", "main")
        self.assertIn("unreferenced heads", self.session("finish", ok=False).stderr)

    def test_session_preserves_secondary_workspace_and_detects_concurrent_change(self):
        copy = self.base / "existing"
        self.run_command("jj", "workspace", "add", "--name", "existing", "-r", "main", str(copy))
        self.session("start")
        candidate = self.candidate()
        self.session("integrate", "--revision", candidate)
        self.publish_local(candidate)
        (copy / "other-work").write_text("concurrent")
        self.assertIn("secondary work changed", self.session("finish", ok=False).stderr)
        self.assertEqual((copy / "other-work").read_text(), "concurrent")

    def test_session_checks_live_remote_and_stops_when_fetch_is_stale(self):
        remote = self.base / "remote.git"
        self.run_command("git", "init", "-q", "--bare", str(remote))
        self.run_command("jj", "git", "remote", "add", "origin", str(remote))
        self.run_command("jj", "git", "push", "--bookmark", "main")
        self.session("start")
        candidate = self.candidate()
        self.session("integrate", "--revision", candidate, "--remote", "origin")
        other = self.base / "writer"
        self.run_command("git", "clone", "-q", "-b", "main", str(remote), str(other))
        canonical = self.root
        self.root = other
        self.run_command("git", "config", "user.name", "Fixture")
        self.run_command("git", "config", "user.email", "fixture@example.test")
        self.run_command("git", "config", "commit.gpgsign", "false")
        (other / "concurrent").write_text("other")
        self.run_command("git", "add", ".")
        self.run_command("git", "commit", "-qm", "test: concurrent")
        self.run_command("git", "push", "-q", "origin", "main")
        self.root = canonical
        self.assertIn("remote advanced", self.session("integrate", "--revision", candidate, "--remote", "origin", ok=False).stderr)



class CapabilityTests(GitRepository):
    def install(self):
        fixture = FRAMEWORK / "tests/fixtures/minimal"
        shutil.copytree(fixture, self.root, dirs_exist_ok=True)
        path = self.root / ".ai-first.toml"
        path.write_text(path.read_text().replace('"public-repository"]', '"public-repository", "vcs-closeout"]'))
        render_repository(self.root, FRAMEWORK)

    def standalone(self, **env):
        return subprocess.run(["python3", ".ai-first/check.py"], cwd=self.root, env=dict(self.env, **env), capture_output=True, text=True)

    def test_standalone_checks_integrity_without_running_local_vcs(self):
        self.install()
        self.assertTrue((self.root / ".ai-first/vcs.py").is_file())
        self.assertEqual(self.standalone().returncode, 0)
        self.merge()
        self.assertEqual(self.standalone(AI_FIRST_VCS_REVISION="missing").returncode, 0)
        self.assertIn("merge commits", self.check(ok=False).stderr)

    def test_shallow_standalone_needs_no_ci_history_binding(self):
        self.install()
        self.run_command("git", "add", ".")
        self.run_command("git", "commit", "-qm", "test: installed contract")
        clone = self.base / "standalone"
        self.run_command("git", "clone", "-q", "--depth=1", self.root.as_uri(), str(clone))
        self.root = clone
        self.assertEqual(self.standalone().returncode, 0)
        self.assertIn("full history", self.check(ok=False).stderr)

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
