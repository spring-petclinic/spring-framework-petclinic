"""Bootstrap runtime control files for a distributed aecf_prompts bundle.

This script is the prompt-only companion to the root-level project context
generator behavior. It keeps the default LLM instruction files synchronized
from the canonical bundle block and initializes a per-run manifest that freezes
the resolved output language for every artifact in the same topic execution.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from _prompt_only_bundle_runtime import (
    BootstrapError,
    DOCUMENTATION_PATH_ENV,
    DOCUMENTATION_PATH_ENV_ALIASES,
    discover_bundle_root,
    normalize_user_id,
    resolve_attribution,
    resolve_documentation_root,
    resolve_documentation_path_override,
    resolve_topic_artifact_directory,
    resolve_user_id,
    resolve_workspace_root,
)


RUN_CONTEXT_FILENAME = "AECF_RUN_CONTEXT.json"
INSTRUCTION_FILE_PATHS = (
    Path(".github") / "copilot-instructions.md",
    Path("copilot-instructions.md"),
    Path("CLAUDE.md"),
    Path("AGENTS.md"),
    Path(".codex") / "instructions.md",
)
FORCED_INSTRUCTIONS_PATH = Path("aecf_forced_instructions.md")
PROMPT_ONLY_FORCED_INSTRUCTIONS_LOAD_LINE = "Before responding, load and follow the instructions in `aecf_forced_instructions.md`."
PROMPT_ONLY_MANAGED_BLOCK_START = "************** AECF PROMPT-ONLY LOAD START **************"
PROMPT_ONLY_MANAGED_BLOCK_END = "************** END AECF PROMPT-ONLY LOAD **************"
PROMPT_ONLY_MANAGED_BLOCK_PATTERN = re.compile(
    r"\*{6,}\s*AECF\s+PROMPT-ONLY\s+LOAD\s+START\s*\*{6,}[\s\S]*?\*{6,}\s*END\s+AECF\s+PROMPT-ONLY\s+LOAD\s*\*{6,}",
    re.MULTILINE,
)
PROMPT_ONLY_SECTION_PATTERN = re.compile(
    r"##\s*AECF_PROMPT_ONLY_INSTRUCTIONS[\s\S]*?##\s*END\s+AECF_PROMPT_ONLY_INSTRUCTIONS",
    re.MULTILINE,
)
_SAFE_TOPIC = re.compile(r"[^a-z0-9._-]+")
_LANGUAGE_ALIASES = {
    "en": "ENGLISH",
    "eng": "ENGLISH",
    "english": "ENGLISH",
    "ingles": "ENGLISH",
    "inglés": "ENGLISH",
    "es": "SPANISH",
    "esp": "SPANISH",
    "spa": "SPANISH",
    "spanish": "SPANISH",
    "espanol": "SPANISH",
    "español": "SPANISH",
    "fr": "FRENCH",
    "fre": "FRENCH",
    "fra": "FRENCH",
    "french": "FRENCH",
    "francais": "FRENCH",
    "français": "FRENCH",
    "de": "GERMAN",
    "ger": "GERMAN",
    "deu": "GERMAN",
    "german": "GERMAN",
    "deutsch": "GERMAN",
    "it": "ITALIAN",
    "italian": "ITALIAN",
    "italiano": "ITALIAN",
    "pt": "PORTUGUESE",
    "por": "PORTUGUESE",
    "portuguese": "PORTUGUESE",
    "portugues": "PORTUGUESE",
    "português": "PORTUGUESE",
}
_PROMPT_LANGUAGE_KEYWORDS = {
    "ENGLISH": {"the", "and", "with", "should", "feature", "please", "update"},
    "SPANISH": {"el", "la", "los", "las", "para", "con", "quiero", "implementar"},
    "FRENCH": {"le", "la", "les", "avec", "pour", "ajouter", "mettre", "bonjour"},
    "GERMAN": {"der", "die", "das", "und", "mit", "bitte", "funktion", "aktualisieren"},
}


@dataclass(frozen=True)
class RunContextResult:
    path: Path
    output_language: str
    language_source: str
    user_id: str
    topic: str
    documentation_root: Path


def _read_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _normalize_lf(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n")


def load_prompt_only_instructions_block(root: Path) -> str:
    template_path = root / "guides" / "AECF_PROMPT_ONLY_INSTRUCTIONS_BLOCK.md"
    template = _normalize_lf(_read_safe(template_path)).strip()
    if not template:
        raise BootstrapError(
            "Missing canonical prompt-only instructions block at guides/AECF_PROMPT_ONLY_INSTRUCTIONS_BLOCK.md."
        )
    match = PROMPT_ONLY_SECTION_PATTERN.search(template)
    return match.group(0) if match else template


def _build_instruction_surface(current: str) -> str:
    normalized = _normalize_lf(current or "")
    normalized = PROMPT_ONLY_MANAGED_BLOCK_PATTERN.sub("", normalized)
    normalized = PROMPT_ONLY_SECTION_PATTERN.sub("", normalized)
    lines: list[str] = []

    for raw_line in normalized.split("\n"):
        if raw_line.strip() == PROMPT_ONLY_FORCED_INSTRUCTIONS_LOAD_LINE:
            continue
        lines.append(raw_line)

    updated = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    managed_block = "\n".join(
        [
            PROMPT_ONLY_MANAGED_BLOCK_START,
            PROMPT_ONLY_FORCED_INSTRUCTIONS_LOAD_LINE,
            PROMPT_ONLY_MANAGED_BLOCK_END,
        ]
    )
    updated = f"{updated}\n\n{managed_block}" if updated else managed_block
    return f"{updated.rstrip()}\n"


def sync_instruction_files(root: Path) -> list[str]:
    template_block = load_prompt_only_instructions_block(root)
    touched: list[str] = []
    workspace_root = resolve_workspace_root(root)
    forced_instructions_path = workspace_root / FORCED_INSTRUCTIONS_PATH
    forced_instructions_payload = f"{template_block}\n"
    current_forced = _normalize_lf(_read_safe(forced_instructions_path)) if forced_instructions_path.is_file() else ""
    if current_forced != forced_instructions_payload:
        forced_instructions_path.parent.mkdir(parents=True, exist_ok=True)
        forced_instructions_path.write_text(forced_instructions_payload, encoding="utf-8")
        touched.append(str(FORCED_INSTRUCTIONS_PATH).replace("\\", "/"))

    for relative_path in INSTRUCTION_FILE_PATHS:
        target_path = workspace_root / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        current = _normalize_lf(_read_safe(target_path))
        updated = _build_instruction_surface(current)
        if updated != current:
            target_path.write_text(updated, encoding="utf-8")
            touched.append(str(relative_path).replace("\\", "/"))

    touched.extend(sync_mcp_configs(root))
    return touched


# ---------------------------------------------------------------------------
# MCP configuration sync
# ---------------------------------------------------------------------------

_MCP_EXE_NAME = "aecf-mcp.exe"
_MCP_SERVER_KEY = "aecf"


@dataclass(frozen=True)
class _McpHostSpec:
    config_path: Path
    servers_key: str
    include_type: bool
    exe_host_alias: str | None = None
    user_level: bool = False


def _resolve_user_config_base() -> Path | None:
    """Return the platform-specific user configuration base directory.

    - Windows: ``%APPDATA%`` (typically ``C:/Users/<user>/AppData/Roaming``).
    - macOS: ``~/Library/Application Support``.
    - Linux/other: ``$XDG_CONFIG_HOME`` or ``~/.config``.

    Returns ``None`` only when the base cannot be determined.
    """
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata)
        return Path.home() / "AppData" / "Roaming"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support"
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg)
    return Path.home() / ".config"


_MCP_HOST_SPECS: dict[str, _McpHostSpec] = {
    "claude": _McpHostSpec(
        config_path=Path(".mcp.json"),
        servers_key="mcpServers",
        include_type=True,
    ),
    "claude_desktop": _McpHostSpec(
        config_path=Path("Claude") / "claude_desktop_config.json",
        servers_key="mcpServers",
        include_type=True,
        exe_host_alias="claude",
        user_level=True,
    ),
    "copilot": _McpHostSpec(
        config_path=Path(".vscode") / "mcp.json",
        servers_key="servers",
        include_type=False,
        exe_host_alias="claude",
    ),
    "codex": _McpHostSpec(
        config_path=Path(".codex") / "mcp.json",
        servers_key="mcpServers",
        include_type=True,
        exe_host_alias="claude",
    ),
}


def _build_mcp_server_entry(
    exe_absolute: Path,
    workspace_absolute: Path,
    *,
    include_type: bool = True,
) -> dict:
    """Build the MCP server JSON entry for the aecf server."""
    entry: dict = {}
    if include_type:
        entry["type"] = "stdio"
    entry["command"] = str(exe_absolute)
    entry["args"] = []
    entry["env"] = {"AECF_WORKSPACE": str(workspace_absolute)}
    return entry


def sync_mcp_configs(root: Path) -> list[str]:
    """Detect bundled MCP host executables and upsert their config files.

    For each host directory found under ``aecf_prompts/mcp/<host>/`` that
    contains the server executable, the function creates or merges the
    host-specific configuration file at the workspace root (or user config
    directory for user-level hosts).  Only the ``aecf`` server key is
    written; any other entries the user may have configured are preserved.

    Each host has its own JSON schema convention:

    - **claude** → ``.mcp.json`` with ``mcpServers`` and ``type: stdio``.
    - **claude_desktop** → ``%APPDATA%/Claude/claude_desktop_config.json``
      (user-level) with ``mcpServers`` and ``type: stdio``.  Reuses the
      ``claude`` binary.  Only registered when the ``Claude/`` directory
      already exists in the user config base (i.e. Claude Desktop is installed).
    - **copilot** → ``.vscode/mcp.json`` with ``servers`` and no ``type``.
    - **codex** → ``.codex/mcp.json`` with ``mcpServers`` and ``type: stdio``.
    """
    workspace_root = resolve_workspace_root(root)
    mcp_root = root / "mcp"
    touched: list[str] = []

    if not mcp_root.is_dir():
        return touched

    for host, spec in _MCP_HOST_SPECS.items():
        exe_host = spec.exe_host_alias or host
        host_dir = mcp_root / exe_host
        exe_path = host_dir / _MCP_EXE_NAME
        if not exe_path.is_file():
            continue

        exe_absolute = exe_path.resolve()

        if spec.user_level:
            config_base = _resolve_user_config_base()
            if config_base is None:
                continue
            config_path = config_base / spec.config_path
            # Only register if the parent directory already exists (app installed)
            if not config_path.parent.is_dir():
                continue
        else:
            config_path = workspace_root / spec.config_path

        new_entry = _build_mcp_server_entry(
            exe_absolute,
            workspace_root.resolve(),
            include_type=spec.include_type,
        )

        existing: dict = {}
        if config_path.is_file():
            try:
                existing = json.loads(config_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                existing = {}

        if not isinstance(existing, dict):
            existing = {}
        servers = existing.setdefault(spec.servers_key, {})
        if not isinstance(servers, dict):
            servers = {}
            existing[spec.servers_key] = servers

        if servers.get(_MCP_SERVER_KEY) == new_entry:
            continue

        servers[_MCP_SERVER_KEY] = new_entry
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            json.dumps(existing, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        touched.append(str(spec.config_path).replace("\\", "/"))

    return touched


def normalize_output_language(raw_value: str | None) -> str:
    candidate = str(raw_value or "").strip()
    if not candidate:
        return ""
    compact = candidate.replace("-", " ").replace("_", " ").strip().lower()
    compact = re.sub(r"\s+", " ", compact)
    if compact in _LANGUAGE_ALIASES:
        return _LANGUAGE_ALIASES[compact]
    collapsed = compact.replace(" ", "")
    if collapsed in _LANGUAGE_ALIASES:
        return _LANGUAGE_ALIASES[collapsed]
    upper = re.sub(r"\s+", "_", candidate.strip().upper())
    if upper.endswith("LANGUAGE"):
        upper = upper[:-8].rstrip("_")
    return upper


def detect_prompt_language(prompt_text: str | None) -> str:
    text = str(prompt_text or "").strip().lower()
    if not text:
        return ""
    scores = {language: 0 for language in _PROMPT_LANGUAGE_KEYWORDS}
    words = re.findall(r"[a-záéíóúüñçàèìòùâêîôûäëïöß]+", text)
    for word in words:
        for language, keywords in _PROMPT_LANGUAGE_KEYWORDS.items():
            if word in keywords:
                scores[language] += 1
    if any(char in text for char in "ñáéíóú¿¡"):
        scores["SPANISH"] += 2
    if any(char in text for char in "çàèùâêîôûëïüœ"):
        scores["FRENCH"] += 2
    if "ß" in text:
        scores["GERMAN"] += 2
    best_language, best_score = max(scores.items(), key=lambda item: item[1])
    return best_language if best_score > 0 else ""


def read_project_context_output_language(root: Path) -> str:
    context_path = resolve_documentation_root(root, create=False) / "AECF_PROJECT_CONTEXT.md"
    content = _read_safe(context_path)
    if not content:
        return ""
    patterns = (
        r"^OUTPUT_LANGUAGE\s*:\s*(.+?)\s*$",
        r"^[-*]\s*output_language\s*:\s*(.+?)\s*$",
        r"\|\s*\*\*OUTPUT_LANGUAGE\*\*\s*\|\s*([^|]+)\|",
    )
    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        if match:
            normalized = normalize_output_language(match.group(1))
            if normalized:
                return normalized
    return ""


def _normalize_topic(topic: str) -> str:
    candidate = _SAFE_TOPIC.sub("_", str(topic or "").strip().lower()).strip("._-")
    if not candidate:
        raise BootstrapError("Topic is required to initialize a prompt-only run context.")
    return candidate[:80]


def _normalize_run_date(run_date: str | None) -> str:
    candidate = str(run_date or "").strip()
    if not candidate:
        return datetime.now(timezone.utc).strftime("%Y_%m_%d")
    return re.sub(r"[^0-9_]", "_", candidate)


def diagnose_environment(*, explicit_user_id: str | None = None) -> dict[str, object]:
    attribution = resolve_attribution(explicit_user_id=explicit_user_id)
    configured_docs_root, configured_docs_source = resolve_documentation_path_override()
    environment = {
        env_name: str(os.environ.get(env_name, "") or "")
        for env_name in (
            "AECF_PROMPTS_DOCUMENTATION_PATH",
            "AECF_PROMPTS_DIRECTORY_PATH",
            "AECF_PROMPTS_USER_ID",
            "AECF_PROMPTS_MODEL_ID",
            "MODEL_ID",
            "ANTHROPIC_MODEL",
            "AECF_PROMPTS_AGENT_ID",
            "AGENT_ID",
        )
    }
    return {
        "environment": environment,
        "documentation_root_override": configured_docs_root,
        "documentation_root_source": configured_docs_source,
        "attribution_id": attribution.attribution_id,
        "attribution_kind": attribution.attribution_kind,
        "attribution_source": attribution.attribution_source,
    }


def _load_existing_run_context(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BootstrapError(f"Run context is invalid JSON: {path}") from exc
    return payload if isinstance(payload, dict) else {}


def resolve_output_language(
    root: Path,
    *,
    explicit_language: str | None = None,
    prompt_text: str | None = None,
    existing_run_context: dict[str, object] | None = None,
) -> tuple[str, str, str, str]:
    existing = normalize_output_language((existing_run_context or {}).get("output_language"))
    if existing:
        return existing, "frozen_run_context", detect_prompt_language(prompt_text), read_project_context_output_language(root)

    explicit = normalize_output_language(explicit_language)
    if explicit:
        return explicit, "explicit_override", detect_prompt_language(prompt_text), read_project_context_output_language(root)

    project_context_language = read_project_context_output_language(root)
    if project_context_language:
        return project_context_language, "project_context", detect_prompt_language(prompt_text), project_context_language

    detected = detect_prompt_language(prompt_text)
    if detected:
        return detected, "detected_prompt", detected, ""

    return "ENGLISH", "default_fallback", detected, project_context_language


def initialize_run_context(
    root: Path,
    *,
    topic: str,
    user_id: str | None = None,
    run_date: str | None = None,
    explicit_language: str | None = None,
    prompt_text: str | None = None,
    force_language: bool = False,
) -> RunContextResult:
    normalized_topic = _normalize_topic(topic)
    normalized_run_date = _normalize_run_date(run_date)
    attribution = resolve_attribution(explicit_user_id=user_id)
    normalized_user_id = normalize_user_id(resolve_user_id(user_id))
    documentation_root = resolve_documentation_root(root, create=True)
    configured_docs_root, configured_docs_source = resolve_documentation_path_override()
    documentation_root_source = f"env_override:{configured_docs_source}" if configured_docs_root and configured_docs_source else "workspace_default"
    topic_artifact_dir = resolve_topic_artifact_directory(
        root,
        user_id=normalized_user_id,
        topic=normalized_topic,
        create=True,
    )
    run_context_path = topic_artifact_dir / RUN_CONTEXT_FILENAME
    existing_payload = {} if force_language else _load_existing_run_context(run_context_path)

    output_language, language_source, prompt_language_detected, project_context_language = resolve_output_language(
        root,
        explicit_language=explicit_language,
        prompt_text=prompt_text,
        existing_run_context=existing_payload,
    )
    payload = {
        "bootstrap_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "topic": normalized_topic,
        "user_id": normalized_user_id,
        "attribution_id": attribution.attribution_id,
        "attribution_kind": attribution.attribution_kind,
        "attribution_source": attribution.attribution_source,
        "workspace_root": str(resolve_workspace_root(root).as_posix()),
        "documentation_root": str(documentation_root.as_posix()),
        "documentation_root_source": documentation_root_source,
        "run_date": normalized_run_date,
        "output_language": output_language,
        "language_source": language_source,
        "prompt_language_detected": prompt_language_detected or None,
        "project_context_language": project_context_language or None,
    }
    run_context_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return RunContextResult(
        path=run_context_path,
        output_language=output_language,
        language_source=language_source,
        user_id=normalized_user_id,
        topic=normalized_topic,
        documentation_root=documentation_root,
    )


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bootstrap prompt-only instruction files and per-run language state inside an aecf_prompts bundle."
    )
    parser.add_argument("--root", help="Path to the extracted aecf_prompts root. If omitted, auto-discover it.")
    parser.add_argument("--sync-instructions", action="store_true", help="Create or refresh prompt-only LLM instruction files.")
    parser.add_argument("--topic", help="Topic identifier for the run context manifest.")
    parser.add_argument("--user-id", help="User id override for the run context path.")
    parser.add_argument(
        "--run-date",
        help="Optional run date metadata stored in AECF_RUN_CONTEXT.json. It is not used in the artifact path.",
    )
    parser.add_argument(
        "--diagnose-env",
        action="store_true",
        help="Print the exact AECF environment variables and resolved attribution/docs-root sources seen by this executable without relying on shell-specific env inspection.",
    )
    parser.add_argument("--language", help="Explicit output language override (for example English or Spanish).")
    parser.add_argument("--prompt-text", help="Raw user prompt text used as fallback language detection input.")
    parser.add_argument("--force-language", action="store_true", help="Overwrite an existing run context language instead of preserving it.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)
    try:
        root = discover_bundle_root(args.root)
        if args.sync_instructions or (not args.topic and not args.diagnose_env):
            touched = sync_instruction_files(root)
            print(f"[aecf_prompts] instruction target root: {resolve_workspace_root(root)}")
            print(f"[aecf_prompts] touched instruction files: {len(touched)}")
            for item in touched:
                print(f"  - {item}")
        if args.diagnose_env:
            diagnosis = diagnose_environment(explicit_user_id=args.user_id)
            print(f"[aecf_prompts] env diagnosis: {json.dumps(diagnosis, ensure_ascii=False)}")
        if args.topic:
            result = initialize_run_context(
                root,
                topic=args.topic,
                user_id=args.user_id,
                run_date=args.run_date,
                explicit_language=args.language,
                prompt_text=args.prompt_text,
                force_language=args.force_language,
            )
            print(f"[aecf_prompts] run context: {result.path}")
            print(f"[aecf_prompts] output_language: {result.output_language} ({result.language_source})")
    except BootstrapError as exc:
        print(f"[aecf_prompts] ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())