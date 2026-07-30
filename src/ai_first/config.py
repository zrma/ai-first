from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from . import VERSION


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class OverlayPaths:
    agents_first_read: str
    agents_project: str
    harness_project: str


@dataclass(frozen=True)
class OutputPaths:
    agents: str
    harness: str
    standalone_check: str
    lock: str


@dataclass(frozen=True)
class Project:
    name: str
    objective: str
    publication_class: str


@dataclass(frozen=True)
class Config:
    repo_root: Path
    config_path: Path
    framework_version: str
    source_kind: str
    source_revision: str | None
    profiles: tuple[str, ...]
    project: Project
    overlay: OverlayPaths
    output: OutputPaths


def _table(data: dict[str, Any], name: str) -> dict[str, Any]:
    value = data.get(name)
    if not isinstance(value, dict):
        raise ConfigError(f"{name} must be a table")
    return value


def _string(data: dict[str, Any], name: str) -> str:
    value = data.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{name} must be a non-empty string")
    return value.strip()


def safe_relative(value: str, field: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value in {"", "."}:
        raise ConfigError(f"{field} must be a safe repository-relative path")
    return path.as_posix()


def path_within(root: Path, relative: str, field: str) -> Path:
    candidate = root / relative
    resolved_root = root.resolve()
    resolved_candidate = candidate.resolve(strict=False)
    if resolved_candidate != resolved_root and resolved_root not in resolved_candidate.parents:
        raise ConfigError(f"{field} must stay inside the repository")
    return candidate


def load_config(repo_root: Path) -> Config:
    root = repo_root.resolve()
    config_path = root / ".ai-first.toml"
    try:
        data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ConfigError("missing .ai-first.toml") from error
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(f"invalid .ai-first.toml: {error}") from error

    if data.get("schema_version") != 1:
        raise ConfigError("schema_version must be 1")

    framework_version = _string(data, "framework_version")
    if framework_version != VERSION:
        raise ConfigError(
            f"framework_version must match the running framework ({VERSION})"
        )

    source_kind = _string(data, "source_kind")
    if source_kind not in {"development", "commit", "release"}:
        raise ConfigError("source_kind must be development, commit or release")
    raw_source_revision = data.get("source_revision")
    if raw_source_revision is None:
        source_revision = None
    elif isinstance(raw_source_revision, str) and raw_source_revision.strip():
        source_revision = raw_source_revision.strip()
    else:
        raise ConfigError("source_revision must be a non-empty string")
    if source_kind == "commit":
        if source_revision is None or not re.fullmatch(
            r"[0-9a-f]{40}", source_revision
        ):
            raise ConfigError(
                "commit source_kind requires a full lowercase source_revision"
            )
    elif source_revision is not None:
        raise ConfigError("source_revision is only valid for commit source_kind")

    raw_profiles = data.get("profiles")
    if (
        not isinstance(raw_profiles, list)
        or not raw_profiles
        or not all(isinstance(item, str) and item for item in raw_profiles)
    ):
        raise ConfigError("profiles must be a non-empty string array")
    if len(set(raw_profiles)) != len(raw_profiles):
        raise ConfigError("profiles must not contain duplicates")
    for profile in raw_profiles:
        safe_relative(profile, "profiles")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", profile):
            raise ConfigError("profiles must use lowercase kebab-case identifiers")

    project_data = _table(data, "project")
    name = _string(project_data, "name")
    if "\n" in name or "\r" in name:
        raise ConfigError("project.name must be a single line")
    if not re.fullmatch(r"[\w][\w.-]*", name):
        raise ConfigError("project.name must be a simple repository identifier")
    objective = _string(project_data, "objective")
    publication_class = _string(project_data, "publication_class")
    if publication_class not in {"public", "internal"}:
        raise ConfigError("project.publication_class must be public or internal")

    overlay_data = _table(data, "overlay")
    overlay = OverlayPaths(
        agents_first_read=safe_relative(
            _string(overlay_data, "agents_first_read"),
            "overlay.agents_first_read",
        ),
        agents_project=safe_relative(
            _string(overlay_data, "agents_project"),
            "overlay.agents_project",
        ),
        harness_project=safe_relative(
            _string(overlay_data, "harness_project"),
            "overlay.harness_project",
        ),
    )

    output_data = _table(data, "output")
    output = OutputPaths(
        agents=safe_relative(_string(output_data, "agents"), "output.agents"),
        harness=safe_relative(_string(output_data, "harness"), "output.harness"),
        standalone_check=safe_relative(
            _string(output_data, "standalone_check"),
            "output.standalone_check",
        ),
        lock=safe_relative(_string(output_data, "lock"), "output.lock"),
    )
    output_values = {
        output.agents,
        output.harness,
        output.standalone_check,
        output.lock,
    }
    if len(output_values) != 4:
        raise ConfigError("output paths must be distinct")
    source_values = {
        ".ai-first.toml",
        overlay.agents_first_read,
        overlay.agents_project,
        overlay.harness_project,
    }
    if output_values & source_values:
        raise ConfigError("output paths must not overwrite configuration or overlays")

    for field, relative in (
        ("overlay.agents_first_read", overlay.agents_first_read),
        ("overlay.agents_project", overlay.agents_project),
        ("overlay.harness_project", overlay.harness_project),
        ("output.agents", output.agents),
        ("output.harness", output.harness),
        ("output.standalone_check", output.standalone_check),
        ("output.lock", output.lock),
    ):
        path_within(root, relative, field)

    return Config(
        repo_root=root,
        config_path=config_path,
        framework_version=framework_version,
        source_kind=source_kind,
        source_revision=source_revision,
        profiles=tuple(raw_profiles),
        project=Project(
            name=name,
            objective=objective,
            publication_class=publication_class,
        ),
        overlay=overlay,
        output=output,
    )
