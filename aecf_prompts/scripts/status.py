from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _prompt_only_bundle_runtime import BootstrapError, discover_bundle_root, resolve_documentation_root, resolve_user_id


PHASE_ORDER = [
    "PLAN",
    "AUDIT_PLAN",
    "FIX_PLAN",
    "TEST_STRATEGY",
    "IMPLEMENT",
    "AUDIT_CODE",
    "FIX_CODE",
    "VERSION",
]
PHASE_SUFFIXES = sorted(PHASE_ORDER, key=len, reverse=True)
VERDICT_PATTERNS = (
    re.compile(r"^\s*(?:AECF\s+)?Verdict\s*[:|]\s*(GO|NO-GO|UNKNOWN)\b", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\*\*Verdict\*\*\s*:\s*(GO|NO-GO|UNKNOWN)\b", re.IGNORECASE),
)


def _parse_json_safe(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _read_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _infer_phase_from_filename(path: Path) -> tuple[str | None, str | None]:
    stem = path.stem
    match = re.match(r"^(\d+)_(.+)$", stem)
    if not match:
        return None, None
    suffix = match.group(2)
    for phase in PHASE_SUFFIXES:
        token = f"_{phase}"
        if suffix == phase:
            return phase, None
        if suffix.endswith(token):
            return phase, suffix[: -len(token)] or None
    return None, None


def _extract_verdict(content: str) -> str | None:
    for pattern in VERDICT_PATTERNS:
        match = pattern.search(content)
        if match:
            return match.group(1).upper()
    return None


def _collect_phase_artifacts(topic_dir: Path) -> tuple[list[dict[str, object]], list[str]]:
    artifacts: list[dict[str, object]] = []
    blockers: list[str] = []
    try:
        candidates = sorted(topic_dir.glob("*.md"))
    except OSError:
        return [], ["Topic directory could not be read."]

    for candidate in candidates:
        phase, skill_name = _infer_phase_from_filename(candidate)
        if not phase:
            continue
        content = _read_safe(candidate)
        artifacts.append(
            {
                "phase": phase,
                "skill": skill_name or "unknown",
                "file": candidate.name,
                "verdict": _extract_verdict(content),
            }
        )

    if not artifacts:
        blockers.append("No governed AECF markdown artifacts were found for this topic.")
    return artifacts, blockers


def _next_phase_from_artifacts(phases_present: set[str], verdicts: dict[str, str | None]) -> str:
    if "VERSION" in phases_present:
        return "COMPLETED"
    if "FIX_CODE" in phases_present:
        return "AUDIT_CODE"
    if "AUDIT_CODE" in phases_present:
        return "FIX_CODE" if verdicts.get("AUDIT_CODE") == "NO-GO" else "VERSION"
    if "IMPLEMENT" in phases_present:
        return "AUDIT_CODE"
    if "TEST_STRATEGY" in phases_present:
        return "IMPLEMENT"
    if "FIX_PLAN" in phases_present:
        return "AUDIT_PLAN"
    if "AUDIT_PLAN" in phases_present:
        return "FIX_PLAN" if verdicts.get("AUDIT_PLAN") == "NO-GO" else "TEST_STRATEGY"
    if "PLAN" in phases_present:
        return "AUDIT_PLAN"
    return "PLAN"


def _artifact_rows(artifacts: list[dict[str, object]]) -> str:
    if not artifacts:
        return "_No hay artefactos gobernados detectados._"
    lines = ["| Phase | File | Verdict |", "| --- | --- | --- |"]
    order_index = {phase: index for index, phase in enumerate(PHASE_ORDER)}
    for artifact in sorted(artifacts, key=lambda item: order_index.get(str(item["phase"]), 999)):
        lines.append(f"| {artifact['phase']} | {artifact['file']} | {artifact['verdict'] or 'n/a'} |")
    return "\n".join(lines)


def _resolve_topic_directory(docs_root: Path, user_id: str, topic: str | None) -> tuple[Path, str]:
    user_root = docs_root / user_id
    if not user_root.is_dir():
        raise FileNotFoundError(f"User documentation root not found: {user_root}")

    if topic:
        topic_dir = user_root / topic
        if not topic_dir.is_dir():
            raise FileNotFoundError(f"Topic directory not found: {topic_dir}")
        return topic_dir, topic

    topics = sorted(path.name for path in user_root.iterdir() if path.is_dir())
    if not topics:
        raise FileNotFoundError(f"No topic directories found under: {user_root}")
    if len(topics) > 1:
        raise BootstrapError(
            "Multiple topics are available for this user. Pass --topic explicitly. Candidates: " + ", ".join(topics)
        )
    return user_root / topics[0], topics[0]


def build_status_markdown(bundle_root: Path, *, topic: str | None = None, user_id: str | None = None) -> str:
    bundle_path = Path(bundle_root).expanduser().resolve()
    docs_root = resolve_documentation_root(bundle_path, create=False)
    effective_user_id = resolve_user_id(explicit_user_id=user_id)
    topic_dir, resolved_topic = _resolve_topic_directory(docs_root, effective_user_id, topic)
    run_context_path = topic_dir / "AECF_RUN_CONTEXT.json"
    run_context = _parse_json_safe(run_context_path)
    artifacts, blockers = _collect_phase_artifacts(topic_dir)
    phases_present = {str(artifact["phase"]) for artifact in artifacts}
    verdicts = {str(artifact["phase"]): artifact["verdict"] for artifact in artifacts}
    pending_phase = _next_phase_from_artifacts(phases_present, verdicts)
    last_verdict = verdicts.get("AUDIT_CODE") or verdicts.get("AUDIT_PLAN") or "n/a"

    if not run_context_path.is_file():
        blockers.append("AECF_RUN_CONTEXT.json is missing for this topic.")
    if last_verdict == "NO-GO":
        blockers.append(f"Latest audit verdict is NO-GO; next required phase is {pending_phase}.")
    if last_verdict == "n/a" and ("AUDIT_PLAN" in phases_present or "AUDIT_CODE" in phases_present):
        blockers.append("An audit artifact exists but no explicit GO/NO-GO verdict could be parsed.")

    completed_phases = [phase for phase in PHASE_ORDER if phase in phases_present]
    blocker_lines = blockers or ["No blocking issues detected from the available prompt-only artifacts."]

    return "\n".join(
        [
            "## AECF · Topic Status",
            "",
            "_Estado inferido desde artefactos prompt-only ya escritos en el workspace._",
            "",
            f"- topic: {resolved_topic}",
            f"- attribution_id: {effective_user_id}",
            f"- documentation_root: `{docs_root.as_posix()}`",
            f"- topic_directory: `{topic_dir.as_posix()}`",
            f"- output_language: {run_context.get('output_language', 'unknown')}",
            f"- context_mode: {run_context.get('context_mode', 'unknown')}",
            f"- completed_phases: {', '.join(completed_phases) if completed_phases else '(none)'}",
            f"- pending_phase: {pending_phase}",
            f"- last_verdict: {last_verdict}",
            "",
            "### Artefactos detectados",
            _artifact_rows(artifacts),
            "",
            "### Blockers",
            *[f"- {line}" for line in blocker_lines],
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect prompt-only topic status from generated artifacts.")
    parser.add_argument("--root", help="Path to the aecf_prompts bundle root.")
    parser.add_argument("--topic", help="Topic to inspect. If omitted, the helper requires exactly one topic directory.")
    parser.add_argument("--user-id", help="Explicit user id override for locating topic artifacts.")
    args = parser.parse_args(argv)

    try:
        bundle_root = discover_bundle_root(args.root)
        print(build_status_markdown(bundle_root, topic=args.topic, user_id=args.user_id))
    except (BootstrapError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())