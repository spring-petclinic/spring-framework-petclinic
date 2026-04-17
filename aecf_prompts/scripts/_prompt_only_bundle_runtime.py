"""Runtime-safe helpers for prompt-only bundle identity and manifest handling."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


MANIFEST_FILENAME = ".aecf_prompts_user_bootstrap.json"
DOCUMENTATION_PATH_ENV = "AECF_PROMPTS_DOCUMENTATION_PATH"
DOCUMENTATION_PATH_ENV_ALIASES = (
    "AECF_PROMPTS_DOCUMENTATION_PATH",
    "AECF_PROMPTS_DIRECTORY_PATH",
)
_SAFE_USER_ID = re.compile(r"[^a-z0-9._-]+")
_SAFE_CANONICAL_USER_ID = re.compile(r"[^a-z0-9.@_+-]+")
_SAFE_AREA_ID = re.compile(r"[^a-z0-9_-]+")


class BootstrapError(RuntimeError):
    """Raised when a prompt bundle cannot be bootstrapped safely."""


@dataclass(frozen=True)
class IdentityBindings:
    canonical_user_id: str
    user_slug: str
    bundle_id: str


@dataclass(frozen=True)
class AttributionBinding:
    attribution_id: str
    attribution_kind: str
    attribution_source: str


def canonicalize_user_id(raw_value: str) -> str:
    """Return the canonical prompt-only user id, preserving email semantics."""

    candidate = str(raw_value or "").strip().lower()
    candidate = candidate.replace(" ", "_")
    candidate = _SAFE_CANONICAL_USER_ID.sub("_", candidate)
    candidate = re.sub(r"_+", "_", candidate)
    candidate = candidate.strip("._-@")
    if not candidate:
        return "anonymous_user"
    return candidate[:128]


def normalize_user_id(raw_value: str) -> str:
    """Return a filesystem-safe prompt-only user id."""

    candidate = canonicalize_user_id(raw_value)
    candidate = candidate.replace("@", "_")
    candidate = _SAFE_USER_ID.sub("_", candidate)
    candidate = candidate.strip("._-")
    if not candidate:
        return "anonymous_user"
    return candidate[:64]


def derive_identity_bindings(raw_value: str) -> IdentityBindings:
    """Derive the minimal stable identity tokens needed for prompt-only packaging."""

    canonical_user_id = canonicalize_user_id(raw_value)
    user_slug = normalize_user_id(canonical_user_id)
    payload = f"bundle|{canonical_user_id}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()[:8]
    bundle_id = f"bdl_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{digest}"
    return IdentityBindings(
        canonical_user_id=canonical_user_id,
        user_slug=user_slug,
        bundle_id=bundle_id,
    )


def manifest_identity_record(identity: IdentityBindings) -> str:
    """Serialize one authorized prompt-only user id."""

    return identity.canonical_user_id


def canonicalize_authorization_area(raw_value: str) -> str:
    """Return the canonical offline authorization area token."""

    candidate = str(raw_value or "").strip().lower().replace("-", "_")
    candidate = _SAFE_AREA_ID.sub("_", candidate)
    candidate = re.sub(r"_+", "_", candidate)
    candidate = candidate.strip("._-")
    return candidate[:64]


def normalize_authorization_areas(raw_value: object) -> list[str]:
    """Return normalized authorization areas from a manifest or CSV field."""

    raw_items: list[object]
    if raw_value is None:
        raw_items = []
    elif isinstance(raw_value, str):
        raw_items = [part for part in re.split(r"[|,;]", raw_value) if str(part).strip()]
    elif isinstance(raw_value, (list, tuple, set)):
        raw_items = list(raw_value)
    else:
        raw_items = [raw_value]

    normalized: list[str] = []
    seen: set[str] = set()
    for item in raw_items:
        area = canonicalize_authorization_area(str(item or ""))
        if not area or area in seen:
            continue
        seen.add(area)
        normalized.append(area)
    return normalized


def load_authorized_principals(manifest: dict[str, object] | None) -> list[dict[str, object]]:
    """Return normalized principals with offline authorization areas."""

    principals: list[dict[str, object]] = []
    seen: set[str] = set()
    raw_records = (manifest or {}).get("authorized_principals")

    if isinstance(raw_records, list):
        for item in raw_records:
            if not isinstance(item, dict):
                continue
            user_id = canonicalize_user_id(str(item.get("user_id") or item.get("email") or ""))
            if not user_id or user_id == "anonymous_user" or user_id in seen:
                continue
            principals.append({
                "user_id": user_id,
                "areas": normalize_authorization_areas(item.get("areas") or item.get("area")),
            })
            seen.add(user_id)

    if principals:
        return principals

    for user_id in load_authorized_users(manifest):
        if user_id in seen:
            continue
        principals.append({"user_id": user_id, "areas": []})
        seen.add(user_id)
    return principals


def load_authorized_areas_for_user(manifest: dict[str, object] | None, raw_user_id: str) -> list[str]:
    """Return the normalized offline authorization areas for one user."""

    candidate = canonicalize_user_id(raw_user_id)
    if not candidate or candidate == "anonymous_user":
        return []
    for principal in load_authorized_principals(manifest):
        if canonicalize_user_id(str(principal.get("user_id") or "")) == candidate:
            return normalize_authorization_areas(principal.get("areas"))
    return []


def user_has_authorization_area(manifest: dict[str, object] | None, raw_user_id: str, area: str) -> bool:
    """Return whether a user owns one offline authorization area."""

    normalized_area = canonicalize_authorization_area(area)
    if not normalized_area:
        return False
    return normalized_area in load_authorized_areas_for_user(manifest, raw_user_id)


def load_authorized_users(manifest: dict[str, object] | None) -> list[str]:
    """Return normalized authorized-user ids from a bundle manifest.

    Supports both the shared-bundle v3 manifest and the legacy v2 single-user
    manifest so previously packaged copies remain usable.
    """

    if not manifest:
        return []

    raw_records = manifest.get("authorized_users")
    records: list[str] = []
    seen: set[str] = set()
    if isinstance(raw_records, list):
        for item in raw_records:
            if isinstance(item, str):
                user_id = canonicalize_user_id(item)
            elif isinstance(item, dict):
                user_id = canonicalize_user_id(str(item.get("user_id") or ""))
            else:
                continue
            if not user_id:
                continue
            if user_id in seen:
                continue
            seen.add(user_id)
            records.append(user_id)
        if records:
            return records

    legacy_user_id = canonicalize_user_id(str(manifest.get("user_id") or ""))
    if legacy_user_id:
        return [legacy_user_id]

    return []


def find_authorized_user(manifest: dict[str, object] | None, raw_user_id: str) -> str | None:
    """Resolve one authorized user id by canonical user id."""

    candidate = canonicalize_user_id(raw_user_id)
    for record in load_authorized_users(manifest):
        if canonicalize_user_id(record) == candidate:
            return record
    return None


def resolve_configured_user_id(explicit_user_id: str | None = None) -> str:
    """Resolve a prompt-only user id from explicit input or AECF_PROMPTS_USER_ID only."""

    for candidate in (explicit_user_id, os.environ.get("AECF_PROMPTS_USER_ID")):
        canonical = canonicalize_user_id(str(candidate or ""))
        if canonical != "anonymous_user":
            return canonical
    raise BootstrapError(
        "This prompt bundle requires AECF_PROMPTS_USER_ID to be defined on the machine or passed explicitly with --user-id."
    )


def _resolve_named_candidate(value: str | None, *, kind: str, source: str) -> AttributionBinding | None:
    canonical = canonicalize_user_id(str(value or ""))
    if canonical == "anonymous_user":
        return None
    return AttributionBinding(
        attribution_id=canonical,
        attribution_kind=kind,
        attribution_source=source,
    )


def resolve_attribution(
    explicit_user_id: str | None = None,
    explicit_model_id: str | None = None,
    explicit_agent_id: str | None = None,
) -> AttributionBinding:
    """Resolve prompt-only attribution from user, model, or agent identifiers."""

    for value, source in (
        (explicit_user_id, "explicit_user_id"),
        (os.environ.get("AECF_PROMPTS_USER_ID"), "env:AECF_PROMPTS_USER_ID"),
    ):
        binding = _resolve_named_candidate(value, kind="user", source=source)
        if binding:
            return binding

    for env_name in (
        "AECF_PROMPTS_MODEL_ID",
        "AECF_MODEL_ID",
        "MODEL_ID",
        "ANTHROPIC_MODEL",
        "MODEL",
        "COPILOT_MODEL",
        "GITHUB_COPILOT_MODEL",
    ):
        source = f"env:{env_name}"
        value = explicit_model_id if env_name == "AECF_PROMPTS_MODEL_ID" and explicit_model_id else os.environ.get(env_name)
        if env_name == "AECF_PROMPTS_MODEL_ID" and explicit_model_id:
            source = "explicit_model_id"
        binding = _resolve_named_candidate(value, kind="model", source=source)
        if binding:
            return binding

    for env_name in (
        "AECF_PROMPTS_AGENT_ID",
        "AECF_AGENT_ID",
        "AGENT_ID",
        "AGENT",
        "COPILOT_AGENT",
        "GITHUB_COPILOT_AGENT",
    ):
        source = f"env:{env_name}"
        value = explicit_agent_id if env_name == "AECF_PROMPTS_AGENT_ID" and explicit_agent_id else os.environ.get(env_name)
        if env_name == "AECF_PROMPTS_AGENT_ID" and explicit_agent_id:
            source = "explicit_agent_id"
        binding = _resolve_named_candidate(value, kind="agent", source=source)
        if binding:
            return binding

    return AttributionBinding(
        attribution_id="prompt_only_agent",
        attribution_kind="agent",
        attribution_source="default_agent_fallback",
    )


def resolve_user_id(explicit_user_id: str | None = None) -> str:
    """Resolve the effective prompt-only identifier used for topic artifact paths."""

    binding = resolve_attribution(explicit_user_id=explicit_user_id)
    if binding.attribution_source == "default_agent_fallback":
        raise BootstrapError(
            "This prompt bundle requires one of these environment variables to be defined on the machine: "
            "AECF_PROMPTS_USER_ID, AECF_PROMPTS_MODEL_ID/MODEL_ID/ANTHROPIC_MODEL, or AECF_PROMPTS_AGENT_ID/AGENT_ID. "
            "You can also pass --user-id explicitly."
        )
    return binding.attribution_id


def _is_prompt_bundle_root(path: Path) -> bool:
    return path.is_dir() and (path / "prompts").is_dir() and (path / "skills").is_dir() and (path / "README.md").is_file()


def discover_bundle_root(explicit_root: str | None = None) -> Path:
    """Discover the `aecf_prompts` root for source or packaged execution."""

    candidates: list[Path] = []
    if explicit_root:
        candidates.append(Path(explicit_root).expanduser().resolve())

    cwd = Path.cwd().resolve()
    candidates.append(cwd)
    candidates.append(cwd / "aecf_prompts")

    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        candidates.extend([exe_dir, exe_dir.parent, exe_dir / "aecf_prompts"])
    else:
        script_dir = Path(__file__).resolve().parent
        candidates.extend([script_dir, script_dir.parent, script_dir.parent.parent])

    for candidate in candidates:
        if _is_prompt_bundle_root(candidate):
            return candidate

    raise BootstrapError(
        "Could not locate the aecf_prompts root. Run the executable from inside the extracted bundle "
        "or pass --root <path-to-aecf_prompts>."
    )


def resolve_workspace_root(bundle_root: Path) -> Path:
    """Return the user workspace that contains the prompt-only bundle."""

    bundle_path = Path(bundle_root).expanduser().resolve()
    parent = bundle_path.parent
    return parent if parent != bundle_path else bundle_path


def resolve_documentation_path_override() -> tuple[str, str] | tuple[None, None]:
    """Return the configured documentation root override and its source env name."""

    for env_name in DOCUMENTATION_PATH_ENV_ALIASES:
        configured = str(os.environ.get(env_name, "") or "").strip()
        if configured:
            return configured, env_name
    return None, None


def resolve_documentation_root(bundle_root: Path, *, create: bool = False) -> Path:
    """Resolve the prompt-only documentation root.

    Precedence:
    1. `AECF_PROMPTS_DOCUMENTATION_PATH` when defined.
    2. `AECF_PROMPTS_DIRECTORY_PATH` as legacy alias.
    3. `<workspace>/.aecf/runtime/documentation` by default.

    Relative overrides are anchored to the user workspace that contains the
    prompt-only bundle, not to the repository that produced the bundle.
    """

    bundle_path = Path(bundle_root).expanduser().resolve()
    workspace_root = resolve_workspace_root(bundle_path)
    configured, _ = resolve_documentation_path_override()
    if configured:
        candidate = Path(configured).expanduser()
        documentation_root = candidate.resolve() if candidate.is_absolute() else (workspace_root / candidate).resolve()
    else:
        documentation_root = (workspace_root / ".aecf" / "runtime" / "documentation").resolve()

    if create:
        documentation_root.mkdir(parents=True, exist_ok=True)
    return documentation_root


def resolve_topic_artifact_directory(
    bundle_root: Path,
    *,
    user_id: str,
    topic: str,
    create: bool = False,
) -> Path:
    """Resolve the canonical per-topic artifact directory for prompt-only runs."""

    topic_dir = resolve_documentation_root(bundle_root, create=create) / user_id / topic
    if create:
        topic_dir.mkdir(parents=True, exist_ok=True)
    return topic_dir


def load_manifest(root: Path) -> dict[str, object] | None:
    path = root / MANIFEST_FILENAME
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BootstrapError(f"Bootstrap manifest is invalid JSON: {path}") from exc