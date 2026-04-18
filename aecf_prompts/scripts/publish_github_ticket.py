"""Publish prompt-only GitHub issues and feature requests from a JSON payload."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_GITHUB_OWNER = "Seachad-TEAM"
DEFAULT_GITHUB_REPOSITORY = "AECF_MCP_issues"
DEFAULT_LABELS_BY_KIND = {
    "issue": ["Bug"],
    "feature": ["feature"],
}
TOKEN_ENV_NAMES = (
    "AECF_PROMPTS_GITHUB_TOKEN",
    "AECF_GITHUB_TOKEN",
    "GITHUB_TOKEN",
    "GH_TOKEN",
)
OWNER_ENV_NAMES = (
    "AECF_PROMPTS_GITHUB_ISSUES_OWNER",
    "AECF_GITHUB_ISSUES_OWNER",
)
REPOSITORY_ENV_NAMES = (
    "AECF_PROMPTS_GITHUB_ISSUES_REPOSITORY",
    "AECF_GITHUB_ISSUES_REPOSITORY",
)


class TicketPublisherError(RuntimeError):
    """Raised when the ticket payload or execution contract is invalid."""


def _first_non_empty(*values: str | None) -> str:
    for value in values:
        candidate = str(value or "").strip()
        if candidate:
            return candidate
    return ""


def _read_payload_text(payload_file: str) -> str:
    if payload_file == "-":
        return sys.stdin.read()
    return Path(payload_file).read_text(encoding="utf-8")


def load_payload(payload_file: str) -> dict[str, object]:
    raw_text = _read_payload_text(payload_file)
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as error:
        raise TicketPublisherError(f"Invalid JSON payload: {error.msg}.") from error
    if not isinstance(payload, dict):
        raise TicketPublisherError("Payload root must be a JSON object.")
    return payload


def build_payload_from_args(
    *,
    kind: str,
    title: str,
    body: str,
    labels: list[str] | None = None,
    owner: str = "",
    repo: str = "",
) -> dict[str, object]:
    payload: dict[str, object] = {
        "kind": normalize_ticket_kind(kind),
        "title": require_non_empty_text("title", title),
        "body": require_non_empty_text("body", body),
    }
    if labels:
        payload["labels"] = labels
    if str(owner or "").strip():
        payload["owner"] = str(owner).strip()
    if str(repo or "").strip():
        payload["repo"] = str(repo).strip()
    return payload


def normalize_ticket_kind(raw_value: object) -> str:
    candidate = str(raw_value or "").strip().lower()
    if candidate not in {"issue", "feature"}:
        raise TicketPublisherError("Payload field `kind` must be `issue` or `feature`.")
    return candidate


def require_non_empty_text(field_name: str, raw_value: object) -> str:
    candidate = str(raw_value or "").strip()
    if not candidate:
        raise TicketPublisherError(f"Payload field `{field_name}` is required.")
    return candidate


def normalize_labels(raw_value: object, kind: str) -> list[str]:
    if raw_value in (None, ""):
        return list(DEFAULT_LABELS_BY_KIND[kind])

    if isinstance(raw_value, str):
        labels = [raw_value.strip()]
    elif isinstance(raw_value, list):
        labels = [str(item or "").strip() for item in raw_value]
    else:
        raise TicketPublisherError("Payload field `labels` must be a string or an array of strings.")

    cleaned: list[str] = []
    seen: set[str] = set()
    for label in labels:
        if not label:
            continue
        lowered = label.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        cleaned.append(label)
    if not cleaned:
        return list(DEFAULT_LABELS_BY_KIND[kind])
    return cleaned


def resolve_repository_value(
    *,
    payload_value: object,
    explicit_value: str | None,
    env_names: tuple[str, ...],
    default_value: str,
) -> str:
    env_value = next((str(os.environ.get(name) or "").strip() for name in env_names if str(os.environ.get(name) or "").strip()), "")
    return _first_non_empty(str(payload_value or ""), explicit_value, env_value, default_value)


def resolve_github_token(explicit_token: str | None, *, allow_gh_cli_auth: bool = True) -> tuple[str, str]:
    direct_token = _first_non_empty(explicit_token)
    if direct_token:
        return direct_token, "explicit"

    for env_name in TOKEN_ENV_NAMES:
        token = str(os.environ.get(env_name) or "").strip()
        if token:
            return token, f"env:{env_name}"

    if allow_gh_cli_auth and shutil.which("gh"):
        try:
            result = subprocess.run(
                ["gh", "auth", "token"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=5,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            result = None
        if result and result.returncode == 0:
            token = str(result.stdout or "").strip()
            if token:
                return token, "gh_auth_token"

    return "", "missing"


def build_compose_url(owner: str, repo: str, title: str, body: str, labels: list[str]) -> str:
    params = {
        "title": title,
        "body": body,
    }
    if labels:
        params["labels"] = ",".join(labels)
    query = urllib.parse.urlencode(params)
    return f"https://github.com/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/issues/new?{query}"


def post_github_issue(*, owner: str, repo: str, token: str, title: str, body: str, labels: list[str]) -> dict[str, object]:
    request_payload = {
        "title": title,
        "body": body,
        "labels": labels,
    }
    request = urllib.request.Request(
        url=f"https://api.github.com/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/issues",
        data=json.dumps(request_payload).encode("utf-8"),
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "AECF-Prompt-Only-Ticket-Publisher",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8") or "{}")
            return {
                "ok": True,
                "status_code": getattr(response, "status", 200),
                "payload": payload,
            }
    except urllib.error.HTTPError as error:
        try:
            payload = json.loads(error.read().decode("utf-8") or "{}")
        except (OSError, json.JSONDecodeError):
            payload = {}
        return {
            "ok": False,
            "status_code": getattr(error, "code", 0),
            "message": str(payload.get("message") or f"GitHub API error ({getattr(error, 'code', 0)})").strip(),
            "payload": payload,
        }
    except OSError as error:
        return {
            "ok": False,
            "status_code": 0,
            "message": str(error).strip() or "Could not connect to GitHub.",
            "payload": {},
        }


def publish_ticket(
    payload: dict[str, object],
    *,
    explicit_token: str | None = None,
    explicit_owner: str | None = None,
    explicit_repo: str | None = None,
    allow_gh_cli_auth: bool = True,
) -> dict[str, object]:
    kind = normalize_ticket_kind(payload.get("kind"))
    title = require_non_empty_text("title", payload.get("title"))
    body = require_non_empty_text("body", payload.get("body"))
    labels = normalize_labels(payload.get("labels"), kind)
    owner = resolve_repository_value(
        payload_value=payload.get("owner"),
        explicit_value=explicit_owner,
        env_names=OWNER_ENV_NAMES,
        default_value=DEFAULT_GITHUB_OWNER,
    )
    repo = resolve_repository_value(
        payload_value=payload.get("repo"),
        explicit_value=explicit_repo,
        env_names=REPOSITORY_ENV_NAMES,
        default_value=DEFAULT_GITHUB_REPOSITORY,
    )
    token, token_source = resolve_github_token(explicit_token, allow_gh_cli_auth=allow_gh_cli_auth)
    compose_url = build_compose_url(owner, repo, title, body, labels)

    base_result = {
        "kind": kind,
        "owner": owner,
        "repo": repo,
        "title": title,
        "labels": labels,
        "compose_url": compose_url,
        "token_source": token_source,
    }

    if not token:
        return {
            **base_result,
            "ok": False,
            "status": "manual_publish_required",
            "message": "No GitHub token was found. Use GITHUB_TOKEN, GH_TOKEN, or gh auth token.",
        }

    api_result = post_github_issue(owner=owner, repo=repo, token=token, title=title, body=body, labels=labels)
    if api_result.get("ok"):
        response_payload = api_result.get("payload") or {}
        return {
            **base_result,
            "ok": True,
            "status": "created",
            "issue_number": response_payload.get("number"),
            "issue_url": response_payload.get("html_url"),
        }

    return {
        **base_result,
        "ok": False,
        "status": "manual_publish_required",
        "message": str(api_result.get("message") or "GitHub issue could not be created automatically.").strip(),
        "status_code": api_result.get("status_code"),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Publish prompt-only GitHub issues and feature requests from a JSON payload.",
    )
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create a GitHub issue or feature request.")
    create_parser.add_argument("--payload-file", default="-", help="Path to a JSON payload file. Use - to read stdin.")
    create_parser.add_argument("--token", default="", help="Explicit GitHub token override.")
    create_parser.add_argument("--owner", default="", help="Override GitHub owner or organization.")
    create_parser.add_argument("--repo", default="", help="Override GitHub repository.")
    create_parser.add_argument(
        "--no-gh-cli-auth",
        action="store_true",
        help="Do not use `gh auth token` as a credential fallback.",
    )

    create_args_parser = subparsers.add_parser(
        "create-from-args",
        help="Create a GitHub issue or feature request without preparing a JSON file.",
    )
    create_args_parser.add_argument("--kind", required=True, help="Ticket kind: issue or feature.")
    create_args_parser.add_argument("--title", required=True, help="GitHub issue title.")
    create_args_parser.add_argument(
        "--body",
        default="",
        help="Issue body text. Use --body-file - to read from stdin when the body is large.",
    )
    create_args_parser.add_argument(
        "--body-file",
        default="",
        help="Optional file containing the issue body. Use - to read the body from stdin.",
    )
    create_args_parser.add_argument(
        "--label",
        action="append",
        default=[],
        help="Repeatable GitHub label override. Defaults to Bug for issue and feature for feature.",
    )
    create_args_parser.add_argument("--token", default="", help="Explicit GitHub token override.")
    create_args_parser.add_argument("--owner", default="", help="Override GitHub owner or organization.")
    create_args_parser.add_argument("--repo", default="", help="Override GitHub repository.")
    create_args_parser.add_argument(
        "--no-gh-cli-auth",
        action="store_true",
        help="Do not use `gh auth token` as a credential fallback.",
    )
    return parser


def _emit_json(payload: dict[str, object]) -> None:
    sys.stdout.write(json.dumps(payload, indent=2, ensure_ascii=True) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command not in {"create", "create-from-args"}:
        parser.print_help(sys.stderr)
        return 2

    try:
        if args.command == "create":
            payload = load_payload(args.payload_file)
        else:
            body = str(args.body or "")
            if str(args.body_file or "").strip():
                body = _read_payload_text(args.body_file)
            payload = build_payload_from_args(
                kind=args.kind,
                title=args.title,
                body=body,
                labels=list(args.label or []),
                owner=args.owner,
                repo=args.repo,
            )
        result = publish_ticket(
            payload,
            explicit_token=args.token,
            explicit_owner=args.owner,
            explicit_repo=args.repo,
            allow_gh_cli_auth=not args.no_gh_cli_auth,
        )
    except TicketPublisherError as error:
        _emit_json(
            {
                "ok": False,
                "status": "invalid_payload",
                "message": str(error),
            }
        )
        return 2
    except OSError as error:
        _emit_json(
            {
                "ok": False,
                "status": "runtime_error",
                "message": str(error).strip() or "Could not read the payload file.",
            }
        )
        return 1

    _emit_json(result)
    if result.get("ok"):
        return 0
    if result.get("status") == "manual_publish_required":
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())