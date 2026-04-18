from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from _prompt_only_bundle_runtime import (
    DOCUMENTATION_PATH_ENV_ALIASES,
    BootstrapError,
    discover_bundle_root,
    resolve_attribution,
    resolve_documentation_path_override,
    resolve_documentation_root,
    resolve_workspace_root,
)
from settings import (
    GLOBAL_SETTINGS_FILE,
    SETTINGS_SCHEMA,
    SettingsLoadError,
    global_settings_path,
    load_global_settings,
    load_user_settings,
    user_settings_path,
)


def _bool_label(value: bool) -> str:
    return "yes" if value else "no"


def _user_settings_rows(workspace_root: Path, user_id: str | None) -> str:
    global_settings = load_global_settings(workspace_root)
    user_settings = load_user_settings(workspace_root, user_id) if user_id else {}
    lines = [
        "| Setting | Efectivo | Fuente | Valores permitidos |",
        "| --- | --- | --- | --- |",
    ]
    for key, schema in SETTINGS_SCHEMA.items():
        user_val = user_settings.get(key)
        global_val = global_settings.get(key)
        if user_val is not None:
            effective, source = user_val, f"usuario ({user_id})"
        elif global_val is not None:
            effective, source = global_val, "global"
        else:
            effective, source = schema["default"], "default"
        label = schema["labels"].get(effective, effective)
        allowed_str = ", ".join(f"`{v}`" for v in schema["allowed"])
        lines.append(f"| `{key}` | `{effective}` ({label}) | {source} | {allowed_str} |")
    return "\n".join(lines)


def _helper_command_rows(bundle_root: Path) -> str:
    helpers = {
        "show settings / settings show": bundle_root / "scripts" / "show_settings.py",
        "settings set": bundle_root / "scripts" / "settings.py",
        "status": bundle_root / "scripts" / "status.py",
        "show workspace_statistics": bundle_root / "scripts" / "workspace_statistics.py",
        "send issue / send feature": bundle_root / "scripts" / "publish_github_ticket.py",
    }
    lines = ["| Command | Helper available |", "| --- | --- |"]
    for command_name, path in helpers.items():
        lines.append(f"| {command_name} | {_bool_label(path.is_file())} |")
    return "\n".join(lines)


def _environment_rows() -> str:
    env_names = [
        "AECF_PROMPTS_DOCUMENTATION_PATH",
        "AECF_PROMPTS_DIRECTORY_PATH",
        "AECF_PROMPTS_USER_ID",
        "AECF_PROMPTS_MODEL_ID",
        "MODEL_ID",
        "ANTHROPIC_MODEL",
        "AECF_PROMPTS_AGENT_ID",
        "AGENT_ID",
    ]
    lines = ["| Variable | Value |", "| --- | --- |"]
    for env_name in env_names:
        value = str(os.environ.get(env_name, "") or "").strip()
        lines.append(f"| {env_name} | {value or '(unset)'} |")
    return "\n".join(lines)


def build_show_settings_markdown(bundle_root: Path) -> str:
    bundle_path = Path(bundle_root).expanduser().resolve()
    workspace_root = resolve_workspace_root(bundle_path)
    configured_docs_root, configured_docs_source = resolve_documentation_path_override()
    documentation_root = resolve_documentation_root(bundle_path, create=False)
    attribution = resolve_attribution()
    effective_user_id = attribution.attribution_id if attribution.attribution_source != "default_agent_fallback" else None
    documentation_root_source = configured_docs_source or "workspace_default"

    global_present = global_settings_path(workspace_root).is_file()
    user_present = user_settings_path(workspace_root, effective_user_id).is_file() if effective_user_id else False

    return "\n".join(
        [
            "## AECF · Prompt-Only Settings",
            "",
            "_Valores efectivos del bundle prompt-only en el workspace actual._",
            "",
            f"- bundle_root: `{bundle_path.as_posix()}`",
            f"- workspace_root: `{workspace_root.as_posix()}`",
            f"- documentation_root: `{documentation_root.as_posix()}`",
            f"- documentation_root_source: {documentation_root_source}",
            f"- documentation_path_override: {configured_docs_root or '(unset)'}",
            f"- attribution_id: {attribution.attribution_id}",
            f"- attribution_kind: {attribution.attribution_kind}",
            f"- attribution_source: {attribution.attribution_source}",
            f"- effective_user_id_for_artifacts: {effective_user_id or 'unresolved'}",
            f"- forced_instructions_present: {_bool_label((workspace_root / 'aecf_forced_instructions.md').is_file())}",
            f"- command_router_guide_present: {_bool_label((bundle_path / 'guides' / 'AECF_PROMPT_ONLY_COMMANDS.md').is_file())}",
            f"- documentation_root_exists: {_bool_label(documentation_root.exists())}",
            "",
            "### User settings (afectan a prompts y outputs)",
            "_Los settings de usuario sobreescriben los globales._",
            _user_settings_rows(workspace_root, effective_user_id),
            f"- global_settings_file: `{global_settings_path(workspace_root).as_posix()}` (present: {_bool_label(global_present)})",
            f"- user_settings_file:   `{user_settings_path(workspace_root, effective_user_id).as_posix() if effective_user_id else '(user_id not resolved)'}` (present: {_bool_label(user_present)})",
            "",
            "### Helper-backed commands",
            _helper_command_rows(bundle_path),
            "",
            "### Environment bindings",
            _environment_rows(),
            "",
            "### Canonical prompt-only rules",
            f"- documentation_path_env_aliases: {', '.join(DOCUMENTATION_PATH_ENV_ALIASES)}",
            "- artifact_path_contract: <DOCS_ROOT>/<user_id>/<TOPIC>/...",
            "- explicit_commands_resolve_first: yes",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Show effective prompt-only settings for the active bundle.")
    parser.add_argument("--root", help="Path to the aecf_prompts bundle root.")
    args = parser.parse_args(argv)

    try:
        bundle_root = discover_bundle_root(args.root)
        print(build_show_settings_markdown(bundle_root))
    except (BootstrapError, SettingsLoadError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())