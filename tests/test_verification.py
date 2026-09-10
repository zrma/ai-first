from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ai_first import verification as v
from ai_first.config import ConfigError
from ai_first.render import DriftError, build, check_repository, render_repository

FRAMEWORK = Path(__file__).resolve().parents[1]


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()

    def binding(self, commands):
        path = self.root / v.BINDING
        path.parent.mkdir(exist_ok=True)
        text = 'schema_version = 1\n'
        for name, argv, extra in commands:
            text += f'\n[[checks]]\nid = "{name}"\nargv = {json.dumps(argv)}\ncoverage = ["unit behavior"]\n{extra}\n'
        path.write_text(text)

    def python(self, body):
        return [sys.executable, '-c', body]

    def run_checks(self, selected=None):
        with contextlib.redirect_stderr(io.StringIO()):
            return v.run(self.root, selected)

    def test_statuses_are_not_flattened_to_success(self):
        self.binding([
            ('ok', self.python('print("passed")'), ''),
            ('bad', self.python('raise SystemExit(3)'), ''),
            ('skip', self.python('raise SystemExit(77)'), 'skip_exit_codes = [77]'),
            ('missing', ['ai-first-test-nonexistent-command'], ''),
        ])
        result = self.run_checks()
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual([c['status'] for c in result['checks']], ['passed', 'failed', 'skipped', 'unavailable'])
        self.assertEqual(result['checks'][1]['exit_code'], 3)

    def test_select_preserves_unexecuted_scope(self):
        self.binding([('a', self.python('pass'), ''), ('b', self.python('raise Exception()'), '')])
        report = self.run_checks(['a'])
        self.assertEqual(report['status'], 'incomplete')
        self.assertEqual(report['checks'][1]['status'], 'not_run')
        with self.assertRaises(v.VerificationError):
            self.run_checks(['unknown'])

    def test_timeout(self):
        self.binding([('slow', self.python('import time; time.sleep(20)'), 'timeout_seconds = 1')])
        result = self.run_checks()
        self.assertEqual(result['checks'][0]['status'], 'timeout')
        self.assertLess(result['checks'][0]['elapsed_seconds'], 5)

    def test_mutating_check_marks_evidence_stale(self):
        self.binding([('mutate', self.python('from pathlib import Path; Path("source.txt").write_text("new")'), '')])
        result = self.run_checks()
        self.assertEqual(result['checks'][0]['status'], 'passed')
        self.assertEqual(result['status'], 'stale')

    def test_report_reuse_detects_source_edit_and_checks_binding(self):
        self.binding([('unit', self.python('pass'), '')])
        report = self.run_checks()
        path = Path(self.temp.name) / 'report.json'
        path.write_text(json.dumps(report))
        self.assertEqual(v.inspect_report(self.root, path)['status'], 'passed')
        report['checks'][0]['exit_code'] = 9
        path.write_text(json.dumps(report))
        with self.assertRaises(v.VerificationError):
            v.inspect_report(self.root, path)
        report['checks'][0]['exit_code'] = 0
        path.write_text(json.dumps(report))
        (self.root / 'source.txt').write_text('edit')
        self.assertEqual(v.inspect_report(self.root, path)['status'], 'stale')
        report['checks'] = []
        path.write_text(json.dumps(report))
        with self.assertRaises(v.VerificationError):
            v.inspect_report(self.root, path)

    def test_log_does_not_enter_report(self):
        self.binding([('unit', self.python('print("LOCAL_LOG_SENTINEL")'), '')])
        result = self.run_checks()
        self.assertNotIn('LOCAL_LOG_SENTINEL', json.dumps(result))
        self.assertNotIn(str(self.root), json.dumps(result))

    def test_no_binding_never_executes_discovery(self):
        (self.root / 'scripts').mkdir()
        (self.root / 'scripts/check.sh').write_text('exit 0\n')
        self.assertEqual(v.plan(self.root)['status'], 'unbound')
        with self.assertRaises(v.VerificationError):
            self.run_checks()
        v.bind(self.root, ['native-check'])
        self.assertEqual(v.load_checks(self.root)[0]['argv'], ['bash', 'scripts/check.sh'])
        with self.assertRaises(v.VerificationError):
            v.bind(self.root, ['native-check'])

    def test_defaults_and_native_precedence(self):
        (self.root / 'Cargo.toml').touch()
        self.assertEqual(v.discover(self.root)[0]['argv'], ['cargo', 'test', '--workspace'])
        (self.root / 'package.json').write_text(json.dumps({'packageManager': 'pnpm@10.0.0', 'scripts': {'check': 'native --full'}}))
        self.assertEqual([c['id'] for c in v.discover(self.root)], ['package-check'])
        self.assertEqual(v.discover(self.root)[0]['argv'], ['pnpm', 'run', 'check'])

    def test_heldout_python_default_executes_real_test(self):
        (self.root / 'tests').mkdir()
        (self.root / 'tests/test_sum.py').write_text('import unittest\nclass Sum(unittest.TestCase):\n def test_sum(self): self.assertEqual(2+2,4)\n')
        v.bind(self.root, ['python-unittest'])
        self.assertEqual(self.run_checks()['status'], 'passed')

    def test_bad_binding_rejected_before_execution(self):
        invalid = ['timeout_seconds = 0', 'skip_exit_codes = [0]', 'unexpected = true']
        for extra in invalid:
            with self.subTest(extra=extra):
                self.binding([('unit', self.python('pass'), extra)])
                with self.assertRaises(v.VerificationError):
                    self.run_checks()
        self.binding([('same', self.python('pass'), ''), ('same', self.python('pass'), '')])
        with self.assertRaises(v.VerificationError):
            v.load_checks(self.root)

    def test_binding_symlink_escape_rejected(self):
        (self.root / '.ai-first').symlink_to(Path(self.temp.name), target_is_directory=True)
        with self.assertRaises(v.VerificationError):
            v.load_checks(self.root)

    def test_report_output_never_overwrites_or_enters_repository(self):
        self.binding([('unit', self.python('from pathlib import Path; Path("ran").touch()'), '')])
        for path in [self.root / 'report.json', Path(self.temp.name) / 'existing.json']:
            if path.name == 'existing.json':
                path.write_text('preserved')
            with contextlib.redirect_stdout(io.StringIO()):
                code = v.main(['--repo', str(self.root), '--run', '--output', str(path)])
            self.assertEqual(code, 2)
            self.assertFalse((self.root / 'ran').exists())

    def test_git_identity_sees_untracked_and_ignores_build_output(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / '.gitignore').write_text('cache/\n')
        before = v.snapshot(self.root)
        (self.root / 'cache').mkdir()
        (self.root / 'cache/result').write_text('ignored')
        self.assertEqual(before, v.snapshot(self.root))
        (self.root / 'new.py').write_text('pass')
        self.assertNotEqual(before, v.snapshot(self.root))

    def test_symlink_identity_does_not_read_target_content(self):
        target = Path(self.temp.name) / 'private'
        target.write_text('one')
        (self.root / 'link').symlink_to(target)
        before = v.snapshot(self.root)
        target.write_text('two')
        self.assertEqual(before, v.snapshot(self.root))

    def enable_profile(self):
        shutil.copytree(FRAMEWORK / 'tests/fixtures/minimal', self.root, dirs_exist_ok=True)
        config = self.root / '.ai-first.toml'
        config.write_text(config.read_text().replace('"public-repository"]', '"public-repository", "verification"]'))

    def test_generated_runtime_and_skill_work_standalone_and_detect_drift(self):
        self.enable_profile()
        self.binding([('unit', self.python('pass'), '')])
        render_repository(self.root, FRAMEWORK)
        check_repository(self.root, FRAMEWORK)
        runtime = self.root / '.ai-first/verify.py'
        completed = subprocess.run([sys.executable, str(runtime), '--repo', str(self.root), '--run'], cwd=self.temp.name, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(json.loads(completed.stdout)['status'], 'passed')
        skill = self.root / '.agents/skills/ai-first-verify/SKILL.md'
        skill.write_text(skill.read_text() + '\nmodified\n')
        completed = subprocess.run([sys.executable, '.ai-first/check.py'], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(completed.returncode, 1)
        self.assertIn('drifted .agents/skills/', completed.stdout)
        with self.assertRaises(DriftError):
            check_repository(self.root, FRAMEWORK)

    def test_optional_output_collision_rejected(self):
        self.enable_profile()
        config = self.root / '.ai-first.toml'
        original = config.read_text()
        for destination in ['.ai-first/verify.py', '.agents/skills']:
            with self.subTest(destination=destination):
                config.write_text(original.replace('agents = "AGENTS.md"', f'agents = "{destination}"'))
                with self.assertRaises(ConfigError):
                    build(self.root, FRAMEWORK)

    def test_adoption_preserves_existing_unowned_skill(self):
        self.enable_profile()
        skill = self.root / '.agents/skills/ai-first-verify/SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text('repository-owned custom skill')
        with self.assertRaises(ConfigError):
            render_repository(self.root, FRAMEWORK)
        self.assertEqual(skill.read_text(), 'repository-owned custom skill')
        self.assertFalse((self.root / '.ai-first/verify.py').exists())

    def test_opt_out_removes_owned_skill_but_preserves_binding(self):
        self.enable_profile()
        self.binding([('unit', self.python('pass'), '')])
        render_repository(self.root, FRAMEWORK)
        config = self.root / '.ai-first.toml'
        config.write_text(config.read_text().replace(', "verification"', ''))
        render_repository(self.root, FRAMEWORK)
        self.assertFalse((self.root / '.agents/skills/ai-first-verify/SKILL.md').exists())
        self.assertFalse((self.root / '.ai-first/verify.py').exists())
        self.assertTrue((self.root / v.BINDING).exists())
        check_repository(self.root, FRAMEWORK)

    def test_opt_out_does_not_delete_modified_skill(self):
        self.enable_profile()
        render_repository(self.root, FRAMEWORK)
        skill = self.root / '.agents/skills/ai-first-verify/SKILL.md'
        skill.write_text('user edits')
        config = self.root / '.ai-first.toml'
        config.write_text(config.read_text().replace(', "verification"', ''))
        with self.assertRaises(ConfigError):
            render_repository(self.root, FRAMEWORK)
        self.assertEqual(skill.read_text(), 'user edits')
