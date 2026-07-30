from __future__ import annotations

import argparse
from pathlib import Path

from . import VERSION
from .config import ConfigError
from .render import DriftError, check_repository, render_repository


def framework_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        prog="ai-first",
        description="Render and verify AI-first repository contracts.",
    )
    result.add_argument("--version", action="version", version=VERSION)
    subcommands = result.add_subparsers(dest="command", required=True)

    for name in ("render", "check"):
        command = subcommands.add_parser(name)
        command.add_argument(
            "--repo",
            type=Path,
            default=Path.cwd(),
            help="consumer repository root",
        )
    return result


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        if arguments.command == "render":
            changed = render_repository(arguments.repo, framework_root())
            if changed:
                print("rendered " + ", ".join(changed))
            else:
                print("ai-first render is already current")
            return 0
        if arguments.command == "check":
            check_repository(arguments.repo, framework_root())
            print("ai-first framework check passed")
            return 0
    except (ConfigError, DriftError) as error:
        print(f"ai-first {arguments.command} failed: {error}")
        return 1
    raise AssertionError(f"unhandled command: {arguments.command}")
