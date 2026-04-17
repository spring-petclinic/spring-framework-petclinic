"""Manage user-configurable AECF settings that affect prompt behavior.

Settings are scoped in two layers:
  - Global  (.aecf/user_settings.json)          — base for all users
  - Per-user (.aecf/user_settings_<user_id>.json) — overrides global

Effective value = user-specific if set, otherwise global if set, otherwise default.

Usage:
    python aecf_prompts/scripts/settings.py show
    python aecf_prompts/scripts/settings.py show --global
    python aecf_prompts/scripts/settings.py set output_language=es
    python aecf_prompts/scripts/settings.py set output_language=es --global
    python aecf_prompts/scripts/settings.py set language=en
    python aecf_prompts/scripts/settings.py set output_language   # shows allowed values
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _prompt_only_bundle_runtime import (
    BootstrapError,
    discover_bundle_root,
    resolve_attribution,
    resolve_workspace_root,
)


# ── File paths ────────────────────────────────────────────────────────────────

GLOBAL_SETTINGS_FILE = ".aecf/user_settings.json"
USER_SETTINGS_FILE_TEMPLATE = ".aecf/user_settings_{user_id}.json"
_UNSAFE_USER_ID_CHARS = re.compile(r"[^A-Za-z0-9_.@-]+")


def global_settings_path(workspace_root: Path) -> Path:
    return workspace_root / GLOBAL_SETTINGS_FILE


def safe_user_id_slug(user_id: str) -> str:
    """Normalize a user_id into a single safe filename segment."""
    slug = _UNSAFE_USER_ID_CHARS.sub("_", user_id.strip())
    slug = slug.strip("._-")
    return slug or "user"


def user_settings_path(workspace_root: Path, user_id: str) -> Path:
    return workspace_root / USER_SETTINGS_FILE_TEMPLATE.format(user_id=safe_user_id_slug(user_id))


# ── Settings schema ───────────────────────────────────────────────────────────

# Each entry describes a configurable setting that affects aecf_prompts behavior.
# Settings with a non-empty "allowed" list are closed enumerations: the user must
# choose one of the listed values.
SETTINGS_SCHEMA: dict[str, dict] = {
    "output_language": {
        "description": "Idioma de los outputs generados por AECF (prompts, artefactos, respuestas).",
        "allowed": ["auto", "es", "en", "fr", "de", "pt", "it"],
        "labels": {
            "auto": "Auto (detectar del prompt del usuario)",
            "es":   "Español",
            "en":   "English",
            "fr":   "Français",
            "de":   "Deutsch",
            "pt":   "Português",
            "it":   "Italiano",
        },
        "default": "auto",
        "aliases": ["language", "idiom", "idioma", "lang"],
        "impacts": ["AECF_RUN_CONTEXT.json → output_language", "todos los artefactos de fase"],
    },
}

# Reverse alias map: alias/canonical → canonical key
_ALIAS_TO_KEY: dict[str, str] = {}
for _key, _schema in SETTINGS_SCHEMA.items():
    _ALIAS_TO_KEY[_key] = _key
    for _alias in _schema.get("aliases", []):
        _ALIAS_TO_KEY[_alias] = _key


def _resolve_key(raw_key: str) -> str | None:
    """Resolve a key or alias to a canonical settings key."""
    return _ALIAS_TO_KEY.get(raw_key.strip().lower())


# ── I/O helpers ───────────────────────────────────────────────────────────────

class SettingsLoadError(RuntimeError):
    """Raised when a settings file exists but cannot be loaded safely."""

def _load_from_path(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SettingsLoadError(f"Could not read settings file: {path}") from exc
    try:
        raw = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise SettingsLoadError(f"Invalid JSON in settings file: {path}") from exc
    if not isinstance(raw, dict):
        raise SettingsLoadError(f"Settings file must contain a JSON object: {path}")
    return {k: v for k, v in raw.items() if isinstance(k, str) and isinstance(v, str)}


def _save_to_path(path: Path, settings: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(settings, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def load_global_settings(workspace_root: Path) -> dict[str, str]:
    return _load_from_path(global_settings_path(workspace_root))


def load_user_settings(workspace_root: Path, user_id: str) -> dict[str, str]:
    return _load_from_path(user_settings_path(workspace_root, user_id))


def load_effective_settings(workspace_root: Path, user_id: str) -> dict[str, str]:
    """Merge global (base) overridden by user-specific settings."""
    effective = load_global_settings(workspace_root)
    effective.update(load_user_settings(workspace_root, user_id))
    return effective


def _resolve_user_id(explicit: str | None) -> str | None:
    """Return user_id from explicit arg or from attribution env vars; None if unresolvable."""
    if explicit:
        return explicit.strip()
    try:
        binding = resolve_attribution()
        if binding.attribution_source != "default_agent_fallback":
            return binding.attribution_id
    except Exception:
        pass
    return None


# ── Formatting helpers ────────────────────────────────────────────────────────

def _format_show(workspace_root: Path, user_id: str | None, global_only: bool = False) -> str:
    global_settings = load_global_settings(workspace_root)
    user_settings = load_user_settings(workspace_root, user_id) if user_id else {}

    lines: list[str] = [
        "## AECF · User Settings",
        "",
        "_Configuración que afecta al comportamiento de los prompts y outputs de AECF._",
        "_Los settings de usuario sobreescriben los globales._",
        "",
        f"- global_settings_file: `{global_settings_path(workspace_root).as_posix()}`",
    ]
    if user_id:
        lines.append(f"- user_settings_file:   `{user_settings_path(workspace_root, user_id).as_posix()}`")
        lines.append(f"- user_id: `{user_id}`")
    else:
        lines.append("- user_id: (no resuelto — mostrando solo settings globales)")

    if global_only or not user_id:
        display_settings = global_settings
        scope_label = "Global"
        lines += [
            "",
            "### Settings globales",
            "",
            "| Setting | Valor | Valores permitidos |",
            "| --- | --- | --- |",
        ]
        for key, schema in SETTINGS_SCHEMA.items():
            current = display_settings.get(key, schema["default"])
            label = schema["labels"].get(current, current)
            allowed_str = ", ".join(f"`{v}`" for v in schema["allowed"])
            source = "global" if key in display_settings else "default"
            lines.append(f"| `{key}` | `{current}` ({label}) — {source} | {allowed_str} |")
    else:
        lines += [
            "",
            "### Configuración efectiva (usuario sobreescribe global)",
            "",
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

    lines += [
        "",
        "### Descripción de los settings",
        "",
    ]
    for key, schema in SETTINGS_SCHEMA.items():
        aliases = schema.get("aliases", [])
        alias_note = f" (aliases: {', '.join(aliases)})" if aliases else ""
        impacts = schema.get("impacts", [])
        impact_note = f"\n  - Impacta en: {'; '.join(impacts)}" if impacts else ""
        lines.append(f"- **`{key}`**{alias_note}: {schema['description']}{impact_note}")

    lines += [
        "",
        "### Para cambiar un setting:",
        "",
        "```",
        "@aecf settings set output_language=es          # por usuario",
        "@aecf settings set output_language=es --global # para todos",
        "python aecf_prompts/scripts/settings.py set output_language=es",
        "python aecf_prompts/scripts/settings.py set output_language=es --global",
        "```",
    ]
    return "\n".join(lines)


def _format_set_options(key: str, schema: dict, bad_value: str | None = None) -> str:
    """Return markdown showing available values when value is missing or invalid."""
    lines: list[str] = []
    if bad_value:
        lines += [
            f"## AECF · settings set `{key}` — valor no válido",
            "",
            f"El valor `{bad_value}` no está permitido para `{key}`.",
            "",
            "Selecciona uno de los valores permitidos:",
        ]
    else:
        lines += [
            f"## AECF · settings set `{key}`",
            "",
            schema["description"],
            "",
            "Selecciona uno de los valores permitidos:",
        ]
    lines += [
        "",
        "| Valor | Descripción |",
        "| --- | --- |",
    ]
    for value in schema["allowed"]:
        label = schema["labels"].get(value, value)
        lines.append(f"| `{value}` | {label} |")

    lines += [
        "",
        "Ejemplo de uso:",
        "",
        "```",
        f"@aecf settings set {key}=<valor>           # por usuario",
        f"@aecf settings set {key}=<valor> --global  # para todos",
        f"python aecf_prompts/scripts/settings.py set {key}=<valor>",
        f"python aecf_prompts/scripts/settings.py set {key}=<valor> --global",
        "```",
    ]
    return "\n".join(lines)


# ── Command handlers ──────────────────────────────────────────────────────────

def cmd_show(workspace_root: Path, user_id: str | None, global_only: bool) -> int:
    print(_format_show(workspace_root, user_id, global_only=global_only))
    return 0


def cmd_set(
    workspace_root: Path,
    user_id: str | None,
    key_value: str,
    global_scope: bool,
) -> int:
    """Set a setting. key_value must be 'key=value' or just 'key' (shows options)."""
    if "=" not in key_value:
        if key_value.strip():
            canonical_key = _resolve_key(key_value.strip())
            if canonical_key is None:
                available = ", ".join(f"`{k}`" for k in SETTINGS_SCHEMA)
                print(
                    f"ERROR: Setting desconocido: `{key_value.strip()}`. "
                    f"Settings disponibles: {available}",
                    file=sys.stderr,
                )
                return 2
            print(_format_set_options(canonical_key, SETTINGS_SCHEMA[canonical_key]))
            return 1
        print(_format_show(workspace_root, user_id, global_only=global_scope))
        return 0

    raw_key, _, raw_value = key_value.partition("=")
    canonical_key = _resolve_key(raw_key.strip())

    if canonical_key is None:
        available = ", ".join(f"`{k}`" for k in SETTINGS_SCHEMA)
        print(
            f"ERROR: Setting desconocido: `{raw_key.strip()}`. "
            f"Settings disponibles: {available}",
            file=sys.stderr,
        )
        return 2

    schema = SETTINGS_SCHEMA[canonical_key]
    value = raw_value.strip().lower()

    if value not in schema["allowed"]:
        print(_format_set_options(canonical_key, schema, bad_value=value))
        return 1

    if global_scope:
        settings = load_global_settings(workspace_root)
        settings[canonical_key] = value
        target_path = global_settings_path(workspace_root)
        scope_label = "global"
    else:
        if not user_id:
            print(
                "ERROR: No se pudo resolver el user_id. "
                "Usa --user-id <id> o define AECF_PROMPTS_USER_ID. "
                "Para settings globales usa --global.",
                file=sys.stderr,
            )
            return 2
        settings = load_user_settings(workspace_root, user_id)
        settings[canonical_key] = value
        target_path = user_settings_path(workspace_root, user_id)
        scope_label = f"usuario ({user_id})"

    _save_to_path(target_path, settings)

    label = schema["labels"].get(value, value)
    print("\n".join([
        "## AECF · settings set",
        "",
        f"- setting: `{canonical_key}`",
        f"- valor:   `{value}` ({label})",
        f"- scope:   {scope_label}",
        f"- guardado en: `{target_path.as_posix()}`",
    ]))
    return 0


# ── CLI entry point ───────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Show or change user-configurable AECF settings.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python settings.py show\n"
            "  python settings.py show --global\n"
            "  python settings.py set output_language=es\n"
            "  python settings.py set output_language=es --global\n"
            "  python settings.py set language=en\n"
            "  python settings.py set output_language   # shows allowed values\n"
        ),
    )
    parser.add_argument("--root", help="Path to the aecf_prompts bundle root.")
    parser.add_argument("--user-id", dest="user_id", help="Override the resolved user_id.")
    parser.add_argument(
        "--global",
        dest="global_scope",
        action="store_true",
        default=False,
        help="Read/write the global settings file instead of the user-scoped one.",
    )
    parser.add_argument(
        "subcommand",
        nargs="?",
        choices=["show", "set"],
        default="show",
        help="Subcommand: 'show' (default) or 'set'.",
    )
    parser.add_argument(
        "key_value",
        nargs="?",
        default="",
        help="For 'set': key=value pair (e.g. output_language=es). "
             "Pass only the key to see allowed values.",
    )

    args = parser.parse_args(argv)

    try:
        bundle_root = discover_bundle_root(args.root)
        workspace_root = resolve_workspace_root(bundle_root)
    except BootstrapError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    user_id = _resolve_user_id(args.user_id)

    try:
        if args.subcommand == "set":
            return cmd_set(workspace_root, user_id, args.key_value, global_scope=args.global_scope)
        return cmd_show(workspace_root, user_id, global_only=args.global_scope)
    except SettingsLoadError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
