#!/usr/bin/env python3
"""Repository-local verification planning and execution (stdlib, Python 3.11+)."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import signal
import subprocess
import sys
import tempfile
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path

BINDING = ".ai-first/verification.toml"
SCHEMA = 1
IGNORED = {".git", ".jj", "node_modules", "target", ".venv", "venv", "__pycache__", ".pytest_cache", "dist", "build"}
LIMITS = [
    "Command success covers only the declared checks; product acceptance requires scenario evidence.",
    "Native runners that return zero after internal skips must expose those skips themselves.",
    "Source identity excludes ignored build/dependency files and submodule contents; it does not attest remote or live state.",
]


class VerificationError(ValueError):
    pass


def inside(root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or relative in {"", "."}:
        raise VerificationError("binding path must be repository-relative")
    result = root / path
    if not result.resolve().is_relative_to(root.resolve()):
        raise VerificationError("binding path escapes repository")
    return result


def check_definition(value: object) -> dict:
    if not isinstance(value, dict):
        raise VerificationError("each check must be a table")
    allowed = {"id", "argv", "coverage", "timeout_seconds", "skip_exit_codes"}
    if set(value) - allowed:
        raise VerificationError("unknown check field")
    name = value.get("id")
    argv = value.get("argv")
    coverage = value.get("coverage")
    timeout = value.get("timeout_seconds", 300)
    skip = value.get("skip_exit_codes", [])
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        raise VerificationError("check id must be lowercase kebab-case")
    if not isinstance(argv, list) or not argv or not all(isinstance(x, str) and x and "\0" not in x for x in argv):
        raise VerificationError("argv must be a non-empty string array")
    if not isinstance(coverage, list) or not coverage or not all(isinstance(x, str) and x.strip() for x in coverage):
        raise VerificationError("coverage must be a non-empty string array")
    if type(timeout) is not int or not 1 <= timeout <= 86400:
        raise VerificationError("timeout_seconds must be an integer from 1 to 86400")
    if not isinstance(skip, list) or not all(type(x) is int and 1 <= x <= 255 for x in skip):
        raise VerificationError("skip_exit_codes must contain nonzero exit codes")
    return dict(id=name, argv=argv, coverage=coverage, timeout_seconds=timeout, skip_exit_codes=skip)


def candidate(name: str, argv: list[str], coverage: str) -> dict:
    return check_definition(dict(id=name, argv=argv, coverage=[coverage]))


def discover(root: Path) -> list[dict]:
    native = []
    if (root / "scripts/check.sh").is_file():
        native.append(candidate("native-check", ["bash", "scripts/check.sh"], "Repository native check entrypoint; inspect modes and side effects before binding."))
    if (root / "package.json").is_file():
        try:
            package = json.loads((root / "package.json").read_text())
            scripts = package.get("scripts", {})
            manager = package.get("packageManager", "").split("@", 1)[0]
            if manager not in {"npm", "pnpm", "yarn", "bun"}:
                manager = next((tool for lock, tool in (("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lock", "bun")) if (root / lock).exists()), "npm")
            for name in ("check", "test"):
                if scripts.get(name):
                    native.append(candidate(f"package-{name}", [manager, "run", name], f"package.json scripts.{name}; inspect the script and its scope before binding."))
        except (ValueError, AttributeError, TypeError) as error:
            raise VerificationError("invalid package.json discovery metadata") from error
    # Native entrypoints own their command lists. Toolchain defaults are fallback candidates.
    if native:
        return native
    defaults = []
    if (root / "Cargo.toml").is_file():
        defaults.append(candidate("cargo-test", ["cargo", "test", "--workspace"], "Cargo workspace tests; runtime or release behavior is not established."))
    if (root / "go.mod").is_file():
        defaults.append(candidate("go-test", ["go", "test", "./..."], "Go package tests; live service behavior is not established."))
    if (root / "tests").is_dir() and any((root / "tests").rglob("test_*.py")):
        defaults.append(candidate("python-unittest", ["python3", "-m", "unittest", "discover", "-s", "tests"], "Python unittest discovery; confirm expected test count and framework compatibility."))
    return defaults


def load_checks(root: Path) -> list[dict] | None:
    path = inside(root, BINDING)
    if not path.exists():
        return None
    try:
        data = tomllib.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise VerificationError("invalid verification binding") from error
    if set(data) != {"schema_version", "checks"} or data.get("schema_version") != SCHEMA:
        raise VerificationError("binding requires schema_version=1 and checks only")
    if not isinstance(data["checks"], list) or not data["checks"]:
        raise VerificationError("binding requires at least one check")
    checks = [check_definition(value) for value in data["checks"]]
    if len({c["id"] for c in checks}) != len(checks):
        raise VerificationError("duplicate check id")
    return checks


def bind(root: Path, selected: list[str]) -> dict:
    choices = {c["id"]: c for c in discover(root)}
    if not selected or len(set(selected)) != len(selected) or set(selected) - choices.keys():
        raise VerificationError("select distinct discovery candidate ids")
    # JSON arrays and strings used here are valid TOML for these fixed generated values.
    lines = ["schema_version = 1", ""]
    for name in selected:
        lines.append("[[checks]]")
        lines.extend(f"{key} = {json.dumps(value, ensure_ascii=False)}" for key, value in choices[name].items())
        lines.append("")
    path = inside(root, BINDING)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write("\n".join(lines))
    except FileExistsError as error:
        raise VerificationError("binding already exists; edit the repository-owned binding explicitly") from error
    return {"status": "bound", "binding": BINDING, "checks": selected, "next": "Review coverage and run render to lock the binding before verification."}


def read_command(root: Path, argv: list[str]) -> bytes | None:
    try:
        done = subprocess.run(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=15, check=False)
        return done.stdout if done.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def snapshot(root: Path) -> dict:
    root = root.resolve()
    vcs = "filesystem"
    revision = None
    names = None
    # jj workspaces may have no .git. Snapshot through jj before obtaining their revision.
    if (root / ".jj").exists():
        listed = read_command(root, ["jj", "file", "list", "-T", 'path ++ "\\0"'])
        if listed is not None:
            names = [os.fsdecode(p) for p in listed.split(b"\0") if p]
            vcs = "jj"
            rev = read_command(root, ["jj", "log", "--no-graph", "-r", "@", "-T", "commit_id"])
            revision = rev.decode().strip() if rev else None
    if names is None:
        top = read_command(root, ["git", "rev-parse", "--show-toplevel"])
        if top and Path(os.fsdecode(top).strip()).resolve() == root:
            listed = read_command(root, ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"])
            if listed is not None:
                names = [os.fsdecode(p) for p in listed.split(b"\0") if p]
                vcs = "git"
                rev = read_command(root, ["git", "rev-parse", "HEAD"])
                revision = rev.decode().strip() if rev else None
    if names is None:
        names = []
        for directory, directories, files in os.walk(root):
            directories[:] = sorted(d for d in directories if d not in IGNORED)
            names.extend((Path(directory) / d).relative_to(root).as_posix() for d in directories if (Path(directory) / d).is_symlink())
            names.extend((Path(directory) / f).relative_to(root).as_posix() for f in files)
    digest = hashlib.sha256()
    for name in sorted(set(names)):
        path = root / name
        # Refuse VCS names outside the repository; hash links without following them.
        if Path(name).is_absolute() or ".." in Path(name).parts:
            raise VerificationError("unsafe source identity path")
        if not path.parent.resolve().is_relative_to(root):
            raise VerificationError("source identity path traverses an external symlink")
        digest.update(os.fsencode(name) + b"\0")
        try:
            if path.is_symlink():
                data = b"link:" + os.fsencode(os.readlink(path))
            elif path.is_file():
                data = b"file:" + path.read_bytes()
            else:
                data = b"missing"
            digest.update(hashlib.sha256(data).digest())
            digest.update(str(path.lstat().st_mode & 0o100).encode() if path.exists() else b"missing")
        except OSError as error:
            raise VerificationError("cannot fingerprint source content") from error
    return {"vcs": vcs, "revision": revision, "content_sha256": digest.hexdigest(), "file_count": len(set(names))}


def plan(root: Path) -> dict:
    checks = load_checks(root)
    return {"schema_version": SCHEMA, "status": "ready" if checks else "unbound", "checks": checks or [], "candidates": [] if checks else discover(root), "limitations": LIMITS}


def execute(check: dict, root: Path) -> dict:
    start = time.monotonic()
    code = None
    status = "unavailable"
    # A temporary file avoids unbounded in-memory output; replay to stderr, never into the report.
    with tempfile.TemporaryFile() as log:
        try:
            process = subprocess.Popen(check["argv"], cwd=root, stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
            try:
                code = process.wait(timeout=check["timeout_seconds"])
                status = "passed" if code == 0 else "skipped" if code in check["skip_exit_codes"] else "failed"
            except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
                try:
                    if os.name == "posix":
                        os.killpg(process.pid, signal.SIGKILL)
                    else:
                        process.kill()
                except ProcessLookupError:
                    pass
                process.wait()
                status = "timeout" if isinstance(error, subprocess.TimeoutExpired) else "interrupted"
        except OSError:
            pass
        log.seek(0)
        while chunk := log.read(65536):
            sys.stderr.write(chunk.decode("utf-8", errors="replace"))
    return {"id": check["id"], "coverage": check["coverage"], "status": status, "exit_code": code, "elapsed_seconds": round(time.monotonic() - start, 3)}


def run(root: Path, selected: list[str] | None = None) -> dict:
    checks = load_checks(root)
    if not checks:
        raise VerificationError("no binding; inspect --plan and choose --bind before --run")
    ids = {c["id"] for c in checks}
    if selected and (set(selected) - ids or len(set(selected)) != len(selected)):
        raise VerificationError("unknown or duplicate selected check")
    started_at = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    before = snapshot(root)
    results = []
    interrupted = False
    for check in checks:
        if interrupted or (selected and check["id"] not in selected):
            results.append({"id": check["id"], "coverage": check["coverage"], "status": "not_run", "exit_code": None, "elapsed_seconds": 0})
        else:
            result = execute(check, root)
            results.append(result)
            interrupted = result["status"] == "interrupted"
    after = snapshot(root)
    stale = before != after
    status = "stale" if stale else "passed" if all(r["status"] == "passed" for r in results) else "incomplete"
    return {"schema_version": SCHEMA, "kind": "ai-first-verification", "status": status, "started_at": started_at, "elapsed_seconds": round(time.monotonic() - start, 3), "started_source": before, "finished_source": after, "environment": {"os": platform.system(), "python": platform.python_version()}, "checks": results, "limitations": LIMITS}


def inspect_report(root: Path, path: Path) -> dict:
    try:
        report = json.loads(path.read_text())
        if report["schema_version"] != SCHEMA or report["kind"] != "ai-first-verification":
            raise ValueError
        checks = report["checks"]
        if not isinstance(checks, list) or not checks or not all(isinstance(c, dict) and c.get("status") in {"passed", "failed", "skipped", "unavailable", "timeout", "interrupted", "not_run"} for c in checks):
            raise ValueError
        expected = load_checks(root)
        if not expected or [(c["id"], c["coverage"]) for c in checks] != [(c["id"], c["coverage"]) for c in expected]:
            raise ValueError
        for check, definition in zip(checks, expected):
            status, code = check["status"], check.get("exit_code")
            if status == "passed" and (type(code) is not int or code != 0):
                raise ValueError
            if status == "skipped" and code not in definition["skip_exit_codes"]:
                raise ValueError
            if status == "failed" and (type(code) is not int or code == 0):
                raise ValueError
        stale = report["started_source"] != report["finished_source"] or snapshot(root) != report["finished_source"]
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise VerificationError("invalid report or report does not match current binding") from error
    report["status"] = "stale" if stale else "passed" if all(c["status"] == "passed" for c in checks) else "incomplete"
    return report


def configure_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--plan", action="store_true")
    actions.add_argument("--bind", nargs="+", metavar="CANDIDATE")
    actions.add_argument("--run", action="store_true")
    actions.add_argument("--report", type=Path, metavar="FILE")
    parser.add_argument("--select", nargs="+", metavar="CHECK")
    parser.add_argument("--output", type=Path, help="new report file outside the repository")


def dispatch(arguments: argparse.Namespace) -> int:
    root = arguments.repo.resolve()
    try:
        if not root.is_dir():
            raise VerificationError("repository root does not exist")
        if arguments.select and not arguments.run:
            raise VerificationError("--select requires --run")
        if arguments.output and not arguments.run:
            raise VerificationError("--output requires --run")
        if arguments.output:
            output = arguments.output.resolve()
            if output.is_relative_to(root) or output.exists():
                raise VerificationError("output must be a new file outside the repository")
            if not output.parent.is_dir():
                raise VerificationError("output parent directory must exist")
        if arguments.plan:
            result = plan(root)
        elif arguments.bind:
            result = bind(root, arguments.bind)
        elif arguments.report:
            result = inspect_report(root, arguments.report)
        else:
            result = run(root, arguments.select)
        encoded = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        if arguments.output:
            with arguments.output.open("x", encoding="utf-8") as handle:
                handle.write(encoded)
        print(encoded, end="")
        return 0 if result["status"] in {"ready", "unbound", "bound", "passed"} else 1
    except (VerificationError, OSError) as error:
        print(json.dumps({"status": "error", "error": str(error)}))
        return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    configure_parser(parser)
    return dispatch(parser.parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
