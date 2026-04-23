from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _prompt_only_bundle_runtime import BootstrapError, discover_bundle_root, resolve_workspace_root


def _parse_json_safe(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _get_entries(config: dict, key: str) -> list[str]:
    entries = config.get(key, {}).get("entries")
    return list(entries) if isinstance(entries, list) else []


def _merge_entries(*groups: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for group in groups:
        for item in group:
            if item in seen:
                continue
            seen.add(item)
            merged.append(item)
    return merged


def _compile_patterns(patterns: list[str]) -> list[re.Pattern[str]]:
    compiled: list[re.Pattern[str]] = []
    for pattern in patterns:
        try:
            compiled.append(re.compile(pattern))
        except re.error:
            continue
    return compiled


def _is_likely_binary_buffer(buffer: bytes) -> bool:
    if not buffer:
        return False

    sample = buffer[:8000]
    suspicious_bytes = 0
    for byte in sample:
        if byte == 0:
            return True
        if byte < 7 or 13 < byte < 32:
            suspicious_bytes += 1
    return (suspicious_bytes / len(sample)) > 0.3


def _count_lines_in_buffer(buffer: bytes) -> int:
    if not buffer:
        return 0

    lines_with_content = 0
    current_line_has_content = False

    for byte in buffer:
        if byte == 10:
            if current_line_has_content:
                lines_with_content += 1
            current_line_has_content = False
            continue
        if byte == 13:
            continue
        if byte != 32 and byte != 9:
            current_line_has_content = True

    if current_line_has_content:
        lines_with_content += 1

    return lines_with_content


def _format_integer(value: int) -> str:
    return f"{int(value):,}"


def _format_bytes(value: int) -> str:
    return f"{_format_integer(value)} B"


def _build_top_extensions_markdown(extensions: dict[str, int], limit: int = 8) -> str:
    entries = sorted(extensions.items(), key=lambda item: (-item[1], item[0]))[:limit]
    if not entries:
        return "_Sin ficheros para clasificar por extension._"
    lines = ["| Extension | Ficheros |", "| --- | ---: |"]
    for extension, count in entries:
        lines.append(f"| {extension} | {_format_integer(count)} |")
    return "\n".join(lines)


def _build_loc_by_extension_markdown(loc_by_extension: dict[str, int]) -> str:
    entries = sorted(
        ((extension, loc) for extension, loc in loc_by_extension.items() if int(loc or 0) > 0),
        key=lambda item: (-item[1], item[0]),
    )
    if not entries:
        return "_No hay extensiones con LOC acumulado._"
    lines = ["| Extension | LOC |", "| --- | ---: |"]
    for extension, loc in entries:
        lines.append(f"| {extension} | {_format_integer(loc)} |")
    return "\n".join(lines)


def load_ci_exclusions(bundle_root: Path, workspace_root: Path) -> dict:
    built_in = _parse_json_safe(bundle_root / "ci_exclusions.json")
    custom = _parse_json_safe(workspace_root / ".aecf" / "custom" / "ci_exclusions.json")

    ignored_directories = _merge_entries(
        _get_entries(built_in, "ignored_directories"),
        _get_entries(custom, "ignored_directories"),
    )
    ignored_directory_patterns = _merge_entries(
        _get_entries(built_in, "ignored_directory_patterns"),
        _get_entries(custom, "ignored_directory_patterns"),
    )
    ignored_file_suffixes = _merge_entries(
        _get_entries(built_in, "ignored_file_suffixes"),
        _get_entries(custom, "ignored_file_suffixes"),
    )
    ignored_file_prefixes = _merge_entries(
        _get_entries(built_in, "ignored_file_prefixes"),
        _get_entries(custom, "ignored_file_prefixes"),
    )
    ignored_file_exact = _merge_entries(
        _get_entries(built_in, "ignored_file_exact"),
        _get_entries(custom, "ignored_file_exact"),
    )
    ignored_file_patterns = _merge_entries(
        _get_entries(built_in, "ignored_file_patterns"),
        _get_entries(custom, "ignored_file_patterns"),
    )

    return {
        "ignored_dir_set": set(ignored_directories),
        "ignored_dir_patterns": _compile_patterns(ignored_directory_patterns),
        "ignored_suffixes": [entry.lower() for entry in ignored_file_suffixes],
        "ignored_prefixes": [entry.lower() for entry in ignored_file_prefixes],
        "ignored_exact_set": set(ignored_file_exact),
        "ignored_file_patterns": _compile_patterns(ignored_file_patterns),
    }


def collect_workspace_statistics(workspace_root: Path, bundle_root: Path) -> dict:
    root = Path(workspace_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Workspace root not found: {root}")

    exclusions = load_ci_exclusions(bundle_root, root)
    stats = {
        "directories": 0,
        "files": 0,
        "files_excluded": 0,
        "total_bytes": 0,
        "text_files": 0,
        "binary_files": 0,
        "read_errors": 0,
        "symlinks_skipped": 0,
        "total_loc": 0,
        "extensions": {},
        "loc_by_extension": {},
    }

    def is_excluded_dir(name: str) -> bool:
        if name in exclusions["ignored_dir_set"]:
            return True
        return any(pattern.search(name) for pattern in exclusions["ignored_dir_patterns"])

    def is_excluded_file(name: str, relative_path: str) -> bool:
        if name in exclusions["ignored_exact_set"]:
            return True
        name_lower = name.lower()
        if any(name_lower.endswith(suffix) for suffix in exclusions["ignored_suffixes"]):
            return True
        if any(name_lower.startswith(prefix) for prefix in exclusions["ignored_prefixes"]):
            return True
        return any(pattern.search(relative_path) for pattern in exclusions["ignored_file_patterns"])

    def walk(current_dir: Path) -> None:
        try:
            entries = list(current_dir.iterdir())
        except OSError:
            stats["read_errors"] += 1
            return

        for entry in entries:
            try:
                if entry.is_symlink():
                    stats["symlinks_skipped"] += 1
                    continue

                if entry.is_dir():
                    if is_excluded_dir(entry.name):
                        continue
                    stats["directories"] += 1
                    walk(entry)
                    continue

                if not entry.is_file():
                    continue

                relative_path = entry.relative_to(root).as_posix()
                if is_excluded_file(entry.name, relative_path):
                    stats["files_excluded"] += 1
                    continue

                stats["files"] += 1
                extension = entry.suffix.lower() or "[no extension]"
                stats["extensions"][extension] = stats["extensions"].get(extension, 0) + 1

                try:
                    file_buffer = entry.read_bytes()
                except OSError:
                    stats["read_errors"] += 1
                    continue

                stats["total_bytes"] += len(file_buffer)
                if _is_likely_binary_buffer(file_buffer):
                    stats["binary_files"] += 1
                    continue

                stats["text_files"] += 1
                loc_for_file = _count_lines_in_buffer(file_buffer)
                stats["total_loc"] += loc_for_file
                if loc_for_file > 0:
                    stats["loc_by_extension"][extension] = stats["loc_by_extension"].get(extension, 0) + loc_for_file
            except OSError:
                stats["read_errors"] += 1

    walk(root)
    return stats


def build_workspace_statistics_markdown(workspace_root: Path, bundle_root: Path) -> str:
    root = Path(workspace_root).expanduser().resolve()
    stats = collect_workspace_statistics(root, bundle_root)
    return "\n".join(
        [
            "## AECF · Workspace Statistics",
            "",
            "_Estadísticas crudas del workspace actual. El recorrido no sigue symlinks; el LOC cuenta solo ficheros de texto detectados heurísticamente._",
            "",
            f"- workspace_root: `{root.as_posix()}`",
            f"- directories_below_root: {_format_integer(stats['directories'])}",
            f"- files_total: {_format_integer(stats['files'])}",
            f"- files_excluded_by_ci_rules: {_format_integer(stats['files_excluded'])}",
            f"- bytes_total: {_format_bytes(stats['total_bytes'])}",
            f"- text_files_for_loc: {_format_integer(stats['text_files'])}",
            f"- binary_files_detected: {_format_integer(stats['binary_files'])}",
            f"- read_errors: {_format_integer(stats['read_errors'])}",
            f"- symlinks_skipped: {_format_integer(stats['symlinks_skipped'])}",
            f"- loc_total: {_format_integer(stats['total_loc'])}",
            "",
            "### Top extensiones",
            _build_top_extensions_markdown(stats["extensions"]),
            "",
            "### Extensiones que contribuyen al LOC",
            _build_loc_by_extension_markdown(stats["loc_by_extension"]),
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build prompt-only workspace statistics for the active workspace.")
    parser.add_argument("--root", help="Path to the aecf_prompts bundle root.")
    parser.add_argument("--workspace-root", help="Path to the workspace to inspect. Defaults to the parent of the resolved aecf_prompts root.")
    args = parser.parse_args(argv)

    try:
        bundle_root = discover_bundle_root(args.root)
        workspace_root = Path(args.workspace_root).expanduser().resolve() if args.workspace_root else resolve_workspace_root(bundle_root)
        print(build_workspace_statistics_markdown(workspace_root, bundle_root))
    except (BootstrapError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())