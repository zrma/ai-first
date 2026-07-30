from __future__ import annotations

import ipaddress
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


SAFE_HOME_USERS = {
    "example",
    "local-user",
    "me",
    "runner",
    "user",
    "you",
}
DOCUMENTATION_NETWORKS = tuple(
    ipaddress.ip_network(value)
    for value in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24")
)
SKIPPED_IMPLEMENTATION_PATHS = {
    "scripts/check-publication-boundary.py",
    "src/ai_first/publication.py",
}


@dataclass(frozen=True, order=True)
class Finding:
    path: str
    line: int
    kind: str


def scan_text(relative: str, text: str) -> set[Finding]:
    findings: set[Finding] = set()
    home = re.compile(r"(?<![A-Za-z0-9_.-])/(?:Users|home)/([A-Za-z0-9._-]+)")
    windows_home = re.compile(
        r"(?i)(?<![A-Za-z0-9_.-])[A-Z]:\\Users\\([A-Za-z0-9._-]+)"
    )
    file_uri = re.compile(r"(?i)\bfile:///(?:Users|home|private|var)/")
    ipv4 = re.compile(r"(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])")
    raw_evidence = re.compile(
        r"(?i)(?:^|/)(?:healthcheck|diagnostic|support-bundle|cluster-dump)"
        r"[-_][0-9]{8}(?:[-_][0-9]{4,6})?(?:/|$)"
    )
    secret_assignment = re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*"
        r"['\"]?(?!<|\\$\\{|env:|example|redacted|placeholder)[A-Za-z0-9_./+=-]{12,}"
    )

    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in home.finditer(line):
            if match.group(1).lower() not in SAFE_HOME_USERS:
                findings.add(Finding(relative, line_number, "local-home-path"))
        for match in windows_home.finditer(line):
            if match.group(1).lower() not in SAFE_HOME_USERS:
                findings.add(Finding(relative, line_number, "local-home-path"))
        if file_uri.search(line):
            findings.add(Finding(relative, line_number, "local-file-uri"))
        if raw_evidence.search(line):
            findings.add(Finding(relative, line_number, "raw-evidence-path"))
        if secret_assignment.search(line):
            findings.add(Finding(relative, line_number, "literal-secret"))
        for match in ipv4.finditer(line):
            try:
                address = ipaddress.ip_address(match.group(0))
            except ValueError:
                continue
            if any(address in network for network in DOCUMENTATION_NETWORKS):
                continue
            if address.is_loopback or address.is_unspecified:
                continue
            if address.is_private or address.is_link_local or address in ipaddress.ip_network(
                "100.64.0.0/10"
            ):
                findings.add(
                    Finding(relative, line_number, "private-network-address")
                )
    return findings


def tracked_files(root: Path) -> list[str]:
    commands = (
        ["jj", "file", "list"],
        ["git", "ls-files"],
    )
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode == 0:
            return sorted(line for line in completed.stdout.splitlines() if line)
    raise RuntimeError("cannot list tracked files with jj or git")


def scan_repository(root: Path) -> set[Finding]:
    findings: set[Finding] = set()
    for relative in tracked_files(root):
        if relative in SKIPPED_IMPLEMENTATION_PATHS:
            continue
        path = root / relative
        if not path.is_file() or path.stat().st_size > 1_000_000:
            continue
        data = path.read_bytes()
        if b"\0" in data:
            continue
        findings.update(
            scan_text(relative, data.decode("utf-8", errors="ignore"))
        )
    return findings


def self_test() -> None:
    hidden_home = "/" + "Users" + "/private-person/project"
    hidden_ip = "10" + ".12.3.4"
    hidden_secret = "api_" + "key = abcdefghijklmnop"
    sample = "\n".join([hidden_home, hidden_ip, hidden_secret])
    kinds = {finding.kind for finding in scan_text("sample.md", sample)}
    expected = {"local-home-path", "private-network-address", "literal-secret"}
    if kinds != expected:
        raise AssertionError(f"unexpected self-test findings: {sorted(kinds)}")

    safe = "\n".join(
        [
            "<home>/project",
            "/Users/example/project",
            "192.0.2.10",
            "127.0.0.1",
            "api_key = <redacted>",
        ]
    )
    if scan_text("safe.md", safe):
        raise AssertionError("safe self-test content produced findings")
