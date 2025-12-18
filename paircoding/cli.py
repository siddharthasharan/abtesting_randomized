"""Command line interface for the pair coding IDE."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .workspace import Workspace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pair coding IDE toolkit")
    parser.add_argument(
        "--state",
        type=Path,
        default=Path(".pairide/state.json"),
        help="Path to the workspace state file",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a workspace")
    init_parser.add_argument("--title", default="Shared notebook")
    init_parser.add_argument("--description", default="Scratchpad for data experiments")

    notebook_parser = subparsers.add_parser("new-notebook", help="Create a notebook")
    notebook_parser.add_argument("title")
    notebook_parser.add_argument("--description", default="")

    session_parser = subparsers.add_parser("create-session", help="Create a collaboration session")
    session_parser.add_argument("name")
    session_parser.add_argument("notebook_id")
    session_parser.add_argument(
        "--collaborator",
        action="append",
        metavar="NAME:ROLE",
        help="Seed collaborators in the format name:role",
    )

    collaborator_parser = subparsers.add_parser("add-collaborator", help="Add a collaborator")
    collaborator_parser.add_argument("session_id")
    collaborator_parser.add_argument("name")
    collaborator_parser.add_argument("--role", default="navigator")

    cell_parser = subparsers.add_parser("add-cell", help="Append a cell to a notebook")
    cell_parser.add_argument("notebook_id")
    cell_parser.add_argument("cell_type", choices=["code", "markdown", "text"])
    cell_parser.add_argument("--source", help="Inline source content; omit to read from stdin")

    run_parser = subparsers.add_parser("run-cell", help="Execute a cell")
    run_parser.add_argument("session_id")
    run_parser.add_argument("notebook_id")
    run_parser.add_argument("cell_id")

    chat_parser = subparsers.add_parser("chat", help="Post a chat message")
    chat_parser.add_argument("session_id")
    chat_parser.add_argument("author")
    chat_parser.add_argument("message")

    list_parser = subparsers.add_parser("list", help="List notebooks or sessions")
    list_parser.add_argument("target", choices=["notebooks", "sessions"])

    dataset_parser = subparsers.add_parser("register-dataset", help="Register a dataset")
    dataset_parser.add_argument("name")
    dataset_parser.add_argument("path", type=Path)
    dataset_parser.add_argument("--description", default="")

    preview_parser = subparsers.add_parser("preview-dataset", help="Preview rows from a dataset")
    preview_parser.add_argument("name")
    preview_parser.add_argument("--limit", type=int, default=5)

    return parser


def _print_json(payload: object) -> None:
    sys.stdout.write(json.dumps(payload, indent=2))
    sys.stdout.write("\n")


def _parse_collaborators(raw_values: list[str] | None) -> list[tuple[str, str]]:
    collaborators: list[tuple[str, str]] = []
    for value in raw_values or []:
        if ":" in value:
            name, role = value.split(":", 1)
        else:
            name, role = value, "navigator"
        collaborators.append((name, role))
    return collaborators


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    workspace = Workspace(args.state)

    if args.command == "init":
        notebook = workspace.create_notebook(args.title, args.description)
        _print_json({"notebook_id": notebook.id})
        return 0

    if args.command == "new-notebook":
        notebook = workspace.create_notebook(args.title, args.description)
        _print_json(notebook.to_dict())
        return 0

    if args.command == "create-session":
        collaborators = _parse_collaborators(args.collaborator)
        session = workspace.create_session(args.name, args.notebook_id, collaborators)
        _print_json(session.to_dict())
        return 0

    if args.command == "add-collaborator":
        collaborator = workspace.add_collaborator(args.session_id, args.name, args.role)
        _print_json(collaborator.to_dict())
        return 0

    if args.command == "add-cell":
        source = args.source if args.source is not None else sys.stdin.read()
        cell = workspace.add_cell(args.notebook_id, args.cell_type, source)
        _print_json(cell.to_dict())
        return 0

    if args.command == "run-cell":
        cell = workspace.run_cell(args.session_id, args.notebook_id, args.cell_id)
        payload = cell.to_dict()
        _print_json(payload)
        return 0

    if args.command == "chat":
        message = workspace.post_message(args.session_id, args.author, args.message)
        _print_json(message.to_dict())
        return 0

    if args.command == "list":
        if args.target == "notebooks":
            _print_json([notebook.to_dict() for notebook in workspace.list_notebooks()])
        else:
            _print_json([session.to_dict() for session in workspace.list_sessions()])
        return 0

    if args.command == "register-dataset":
        workspace.register_dataset(args.name, args.path, args.description)
        _print_json({"status": "registered", "name": args.name, "path": str(args.path)})
        return 0

    if args.command == "preview-dataset":
        preview = workspace.preview_dataset(args.name, args.limit)
        _print_json(preview)
        return 0

    parser.error(f"Unknown command {args.command}")
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
