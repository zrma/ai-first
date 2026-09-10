#!/usr/bin/env python3
"""격리 작업과 인계를 준비하고 공개 없이 통합 결과를 검증한다."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import subprocess
import tempfile
import uuid
from pathlib import Path

if __package__:
    from . import verification
else:
    import verify as verification

SCHEMA = 1
HEX_REVISION = re.compile(r"[0-9a-f]{40}")
TASK_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,47}")


class WorkError(ValueError):
    pass


def command(root: Path, argv: list[str], timeout: int = 60, strip: bool = True) -> str:
    try:
        done = subprocess.run(argv, cwd=root, stdin=subprocess.DEVNULL, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise WorkError(f"cannot run {argv[0]}") from error
    if done.returncode:
        raise WorkError(f"{argv[0]} failed: {done.stderr.decode(errors='replace').strip()}")
    output = done.stdout.decode(errors="surrogateescape")
    return output.strip() if strip else output


def revision(root: Path) -> str:
    result = command(root, ["jj", "log", "-r", "@", "--no-graph", "-T", "commit_id"])
    if not HEX_REVISION.fullmatch(result):
        raise WorkError("cannot resolve working revision")
    return result


def git_root(root: Path) -> str:
    return command(root, ["jj", "git", "root"])


def binding_digest(root: Path) -> str:
    path = verification.inside(root.resolve(), verification.BINDING)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def paths(values: list[str]) -> list[str]:
    result = []
    for value in values:
        path = Path(value)
        if path.is_absolute() or ".." in path.parts or value in {"", "."} or any(c in value for c in "*?[]\0\n\r"):
            raise WorkError("write scope must contain literal repository-relative files or directories")
        if path.parts[0] in {".git", ".jj", ".ai-first"}:
            raise WorkError("VCS metadata and verification bindings are coordinator-owned")
        normalized = path.as_posix().rstrip("/")
        if normalized in result:
            raise WorkError("duplicate write scope")
        result.append(normalized)
    if not result:
        raise WorkError("at least one write path is required")
    return result


def covers(scope: str, path: str) -> bool:
    return path == scope or path.startswith(scope + "/")


def overlap(left: list[str], right: list[str]) -> bool:
    return any(covers(a, b) or covers(b, a) for a in left for b in right)


def save(state_dir: Path, state: dict) -> None:
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=state_dir, delete=False) as handle:
        json.dump(state, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, state_dir / "work.json")


def load(state_dir: Path) -> dict:
    try:
        state = json.loads((state_dir / "work.json").read_text())
        if state["schema_version"] != SCHEMA or not HEX_REVISION.fullmatch(state["base_revision"]):
            raise ValueError
        if not isinstance(state["tasks"], dict) or not Path(state["source"]).is_absolute():
            raise ValueError
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise WorkError("invalid private work state") from error
    if state_dir.resolve().is_relative_to(Path(state["source"]).resolve()):
        raise WorkError("private work state must stay outside the source repository")
    return state


@contextlib.contextmanager
def locked(state_dir: Path):
    lock = state_dir / ".lock"
    try:
        descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as error:
        raise WorkError("work state is locked; use unlock only after its owning process has stopped") from error
    try:
        os.write(descriptor, str(os.getpid()).encode())
        os.close(descriptor)
        yield
    finally:
        lock.unlink(missing_ok=True)


def unlock(state_dir: Path) -> dict:
    lock = state_dir / ".lock"
    try:
        owner = int(lock.read_text())
        if owner <= 0:
            raise ValueError
        os.kill(owner, 0)
    except ProcessLookupError:
        lock.unlink()
        return {"status": "unlocked"}
    except (OSError, ValueError) as error:
        raise WorkError("cannot prove that the lock owner has stopped") from error
    raise WorkError("lock owner is still running")


def initialize(root: Path, state_dir: Path, objective: str, scope: list[str]) -> dict:
    root = root.resolve()
    state_dir = state_dir.resolve()
    if state_dir.is_relative_to(root) or root.is_relative_to(state_dir):
        raise WorkError("private state must be outside and not contain the source repository")
    scope = paths(scope)
    checks = verification.load_checks(root)
    if not checks:
        raise WorkError("connect native checks using verify --plan and --bind before starting work")
    base = revision(root)
    identity = verification.snapshot(root)
    work_id = uuid.uuid4().hex[:12]
    base_bookmark = f"feature/ai-first-{work_id}-base"
    state_dir.mkdir(parents=True, exist_ok=False, mode=0o700)
    state = {
        "schema_version": SCHEMA, "id": work_id, "source": str(root),
        "base_revision": base, "base_identity": identity, "objective": objective,
        "write_scope": scope, "binding_digest": binding_digest(root),
        "check_ids": [check["id"] for check in checks],
        "base_bookmark": base_bookmark, "tasks": {}, "integrations": [],
        "phase": "open", "authority": "Local edits and verification only; no publication, deletion, or history rewrite.",
    }
    save(state_dir, state)
    # local bookmark로 현재 working-copy snapshot을 격리 clone에 전달한다.
    command(root, ["jj", "bookmark", "create", base_bookmark, "-r", base])
    return {"status": "open", "state": str(state_dir), "base_revision": base, "check_ids": state["check_ids"]}


def ensure_source(state: dict) -> None:
    if verification.snapshot(Path(state["source"])) != state["base_identity"]:
        raise WorkError("source advanced since work started; preserve this work and start from the current source")


def clone(state: dict, destination: Path) -> None:
    root = Path(state["source"])
    command(root, ["jj", "git", "clone", "--colocate", "--remote", "work-source", "--branch", state["base_bookmark"], git_root(root), str(destination)])
    # native visibility 검사를 위해 원본 origin만 연결하며 fetch/push하지 않는다.
    remotes = command(root, ["jj", "git", "remote", "list"]).splitlines()
    for remote in remotes:
        name, _, url = remote.partition(" ")
        if name == "origin" and url:
            command(destination, ["jj", "git", "remote", "add", "origin", url])
    if verification.snapshot(destination)["content_sha256"] != state["base_identity"]["content_sha256"]:
        raise WorkError("isolated clone does not match the captured source")


def packet(state_dir: Path, state: dict, task: dict) -> dict:
    return {
        "schema_version": SCHEMA, "task_id": task["id"], "objective": task["objective"],
        "work_objective": state["objective"], "base_revision": state["base_revision"],
        "workspace": task["workspace"], "write_scope": task["write_scope"],
        "check_ids": task["check_ids"], "authority": state["authority"],
        "instructions": "Read the repository's native instructions. Edit only the assigned paths. Other files are read-only. Preserve native acceptance. Hand off your actual change and unresolved issues; the coordinator verifies integration.",
        "handoff_argv": ["python3", ".ai-first/work.py", "handoff", "--state", str(state_dir), "--id", task["id"]],
        "runtime_support": "The host owns agent spawn, messaging and cancellation; this packet and CLI do not grant external tool permissions.",
    }


def assign(state_dir: Path, task_id: str, objective: str, scope: list[str], check_ids: list[str] | None) -> dict:
    if not TASK_ID.fullmatch(task_id):
        raise WorkError("task id must be a short lowercase kebab-case identifier")
    scope = paths(scope)
    with locked(state_dir):
        state = load(state_dir)
        ensure_source(state)
        if task_id in state["tasks"]:
            raise WorkError("task already exists; inspect packet or resume it instead of replacing its workspace")
        if not all(any(covers(parent, path) for parent in state["write_scope"]) for path in scope):
            raise WorkError("assignment exceeds the work's write scope")
        if any(overlap(scope, task["write_scope"]) for task in state["tasks"].values()):
            raise WorkError("write scope overlaps another assignment; perform dependent edits sequentially")
        selected = check_ids or state["check_ids"]
        if len(set(selected)) != len(selected) or set(selected) - set(state["check_ids"]):
            raise WorkError("unknown or duplicate check id")
        task = {"id": task_id, "objective": objective, "write_scope": scope, "check_ids": selected,
                "workspace": str(state_dir / task_id), "status": "preparing", "attempts": []}
        state["tasks"][task_id] = task
        save(state_dir, state)
        try:
            clone(state, Path(task["workspace"]))
        except WorkError as error:
            task["status"], task["error"] = "setup_failed", str(error)
            save(state_dir, state)
            raise
        task["status"] = "assigned"
        save(state_dir, state)
        return packet(state_dir, state, task)


def changed_paths(root: Path, base: str, head: str) -> list[str]:
    output = command(root, ["git", "--git-dir", git_root(root), "diff", "--name-only", "--no-renames", "-z", base, head], strip=False)
    return [value for value in output.split("\0") if value]


def inspect_change(state: dict, task: dict) -> tuple[str, list[str]]:
    root = Path(task["workspace"])
    if binding_digest(root) != state["binding_digest"]:
        raise WorkError("worker changed coordinator-owned verification binding")
    head = revision(root)
    if command(root, ["jj", "log", "--no-graph", "-r", f"{state['base_revision']} & ancestors({head})", "-T", "commit_id"]) != state["base_revision"]:
        raise WorkError("worker revision is not based on the assigned source")
    if command(root, ["jj", "log", "-r", head, "--no-graph", "-T", "conflict"]) == "true":
        raise WorkError("worker contains unresolved conflicts")
    changed = changed_paths(root, state["base_revision"], head)
    outside = [path for path in changed if not any(covers(scope, path) for scope in task["write_scope"])]
    if outside:
        raise WorkError("worker changed paths outside its assigned scope: " + ", ".join(outside))
    return head, changed


def selected_passed(report: dict, selected: list[str]) -> bool:
    results = {check["id"]: check["status"] for check in report["checks"]}
    return report["started_source"] == report["finished_source"] and all(results.get(check_id) == "passed" for check_id in selected)


def handoff(state_dir: Path, task_id: str) -> dict:
    with locked(state_dir):
        state = load(state_dir)
        task = state["tasks"][task_id]
        if task["status"] not in {"assigned", "failed"}:
            raise WorkError("task is not ready for handoff; inspect its status or explicitly resume it")
        head, changed = inspect_change(state, task)
        task["status"] = "checking"
        token = uuid.uuid4().hex
        task["verification_token"] = token
        save(state_dir, state)
    report = verification.run(Path(task["workspace"]), task["check_ids"])
    with locked(state_dir):
        state = load(state_dir)
        task = state["tasks"][task_id]
        if task["status"] != "checking" or task["verification_token"] != token:
            raise WorkError("handoff ownership changed during verification")
        attempt = {"revision": head, "changed_paths": changed, "report": report}
        task["attempts"].append(attempt)
        current = revision(Path(task["workspace"]))
        if current != head or not selected_passed(report, task["check_ids"]):
            task["status"] = "failed"
            save(state_dir, state)
            return {"status": "failed", "task_id": task_id, "report": report}
        bookmark = f"feature/ai-first-{state['id']}-{task_id}-{len(task['attempts'])}"
        command(Path(task["workspace"]), ["jj", "bookmark", "create", bookmark, "-r", head])
        task.update(status="handed_off", revision=head, bookmark=bookmark, identity=report["finished_source"])
        save(state_dir, state)
        return {"status": "handed_off", "task_id": task_id, "revision": head, "changed_paths": changed,
                "verified_checks": task["check_ids"], "remaining_acceptance": "Coordinator must review the requested outcome and verify the integrated result."}


def integrate(state_dir: Path) -> dict:
    with locked(state_dir):
        state = load(state_dir)
        ensure_source(state)
        if not state["tasks"] or any(task["status"] != "handed_off" for task in state["tasks"].values()):
            raise WorkError("all assignments need verified handoffs before integration")
        if state["phase"] == "integrating":
            raise WorkError("integration is already in progress")
        for task in state["tasks"].values():
            head, _ = inspect_change(state, task)
            if head != task["revision"] or verification.snapshot(Path(task["workspace"])) != task["identity"]:
                raise WorkError("worker changed after handoff; resume and verify its new result")
        destination = state_dir / f"integration-{len(state['integrations']) + 1}"
        attempt = {"workspace": str(destination), "status": "preparing", "token": uuid.uuid4().hex}
        state["integrations"].append(attempt)
        state["phase"] = "integrating"
        save(state_dir, state)
    try:
        clone(state, destination)
        heads = []
        for task in state["tasks"].values():
            remote = "worker-" + task["id"]
            command(destination, ["jj", "git", "remote", "add", remote, git_root(Path(task["workspace"]))])
            command(destination, ["jj", "git", "fetch", "--remote", remote, "--branch", task["bookmark"]])
            heads.append(task["revision"])
        command(destination, ["jj", "new", *heads])
        if command(destination, ["jj", "log", "-r", "@", "--no-graph", "-T", "conflict"]) == "true":
            raise WorkError("integration has unresolved conflicts")
        report = verification.run(destination)
        attempt.update(status="verified" if selected_passed(report, state["check_ids"]) else "failed", revision=revision(destination), report=report)
        ensure_source(state)
        if any(revision(Path(task["workspace"])) != task["revision"] for task in state["tasks"].values()):
            raise WorkError("worker advanced during integration; verify its current result before integrating again")
    except (WorkError, verification.VerificationError, OSError) as error:
        attempt.update(status="failed", error=str(error))
    with locked(state_dir):
        latest = load(state_dir)
        if latest["phase"] != "integrating" or latest["integrations"][-1]["token"] != attempt["token"]:
            raise WorkError("integration ownership changed; preserved result requires review")
        latest["integrations"][-1] = attempt
        latest["phase"] = attempt["status"]
        save(state_dir, latest)
    return {"status": attempt["status"], "integration": attempt,
            "remaining_acceptance": "Review product acceptance and choose the next local action. The source working copy and publication bookmarks were not advanced."}


def resume(state_dir: Path, task_id: str | None) -> dict:
    with locked(state_dir):
        state = load(state_dir)
        if task_id:
            task = state["tasks"][task_id]
            if task["status"] == "setup_failed":
                raise WorkError("setup failed; inspect the preserved directory and start a new work state")
            task["status"] = "assigned"
            state["phase"] = "open"
            save(state_dir, state)
            return packet(state_dir, state, task)
        if state["phase"] != "integrating":
            raise WorkError("no interrupted integration to resume")
        state["integrations"][-1]["status"] = "interrupted"
        state["phase"] = "open"
        save(state_dir, state)
        return {"status": "open", "next": "Re-run integrate after stopping the previous coordinator process; previous workspace is preserved."}


def configure_parser(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="work_command", required=True)
    init = subparsers.add_parser("init")
    init.add_argument("--repo", type=Path, default=Path.cwd())
    init.add_argument("--state", type=Path, required=True)
    init.add_argument("--objective", required=True)
    init.add_argument("--write", nargs="+", required=True)
    assign_parser = subparsers.add_parser("assign")
    assign_parser.add_argument("--state", type=Path, required=True)
    assign_parser.add_argument("--id", required=True)
    assign_parser.add_argument("--objective", required=True)
    assign_parser.add_argument("--write", nargs="+", required=True)
    assign_parser.add_argument("--check", nargs="+")
    for name in ("status", "packet", "handoff", "integrate", "resume", "unlock"):
        action = subparsers.add_parser(name)
        action.add_argument("--state", type=Path, required=True)
        if name in {"packet", "handoff", "resume"}:
            action.add_argument("--id", required=name != "resume")


def dispatch(arguments: argparse.Namespace) -> int:
    state_dir = arguments.state.resolve()
    try:
        action = arguments.work_command
        if action == "init":
            result = initialize(arguments.repo, state_dir, arguments.objective, arguments.write)
        elif action == "assign":
            result = assign(state_dir, arguments.id, arguments.objective, arguments.write, arguments.check)
        elif action == "handoff":
            result = handoff(state_dir, arguments.id)
        elif action == "integrate":
            result = integrate(state_dir)
        elif action == "resume":
            result = resume(state_dir, arguments.id)
        elif action == "unlock":
            result = unlock(state_dir)
        else:
            state = load(state_dir)
            result = packet(state_dir, state, state["tasks"][arguments.id]) if action == "packet" else state
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if result.get("status") == "failed" else 0
    except (WorkError, verification.VerificationError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}, ensure_ascii=False))
        return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    configure_parser(parser)
    return dispatch(parser.parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
