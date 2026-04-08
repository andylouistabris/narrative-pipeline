"""Command-line interface for Narrative Pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .project import (
    build_spec_ready,
    create_critique_report,
    create_scene,
    init_project,
    project_status,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="narrative-pipeline",
        description="Simple filesystem workflow for collaborative narrative writing.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a new project scaffold.")
    init_parser.add_argument("project_name", help="Name for the new project folder.")
    init_parser.add_argument(
        "--projects-dir",
        default="projects",
        help="Folder that should contain your projects. Defaults to ./projects.",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite template files if they already exist.",
    )
    init_parser.set_defaults(handler=handle_init)

    status_parser = subparsers.add_parser(
        "status",
        help="Show which project files are still placeholders and what to do next.",
    )
    status_parser.add_argument("project_path", help="Path to a project folder.")
    status_parser.set_defaults(handler=handle_status)

    spec_parser = subparsers.add_parser(
        "build-spec",
        aliases=["check-spec"],
        help="Check whether premise, characters, and outline are ready for spec drafting.",
    )
    spec_parser.add_argument("project_path", help="Path to a project folder.")
    spec_parser.set_defaults(handler=handle_build_spec)

    scene_parser = subparsers.add_parser(
        "scene",
        aliases=["write-scene"],
        help="Create a scene file for a chosen episode and scene number.",
    )
    scene_parser.add_argument("project_path", help="Path to a project folder.")
    scene_parser.add_argument("--episode", type=int, required=True, help="Episode number.")
    scene_parser.add_argument("--scene", type=int, required=True, help="Scene number.")
    scene_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the scene file if it already exists.",
    )
    scene_parser.set_defaults(handler=handle_scene)

    critique_parser = subparsers.add_parser(
        "critique",
        aliases=["run-critique"],
        help="Create or refresh the merged critique report placeholder.",
    )
    critique_parser.add_argument("project_path", help="Path to a project folder.")
    critique_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the critique report if it already exists.",
    )
    critique_parser.set_defaults(handler=handle_critique)

    return parser


def handle_init(args: argparse.Namespace) -> int:
    result = init_project(
        project_name=args.project_name,
        projects_dir=Path(args.projects_dir),
        force=args.force,
    )
    print(f"Project ready: {result.project_root}")
    if result.created_files:
        print("Created files:")
        for path in result.created_files:
            print(f"- {path.relative_to(result.project_root)}")
    if result.skipped_files:
        print("Kept existing files:")
        for path in result.skipped_files:
            print(f"- {path.relative_to(result.project_root)}")
    print(f"Next: run `narrative-pipeline status {result.project_root}`")
    return 0


def handle_status(args: argparse.Namespace) -> int:
    summary = project_status(args.project_path)
    print(f"Project: {summary.project_root}")
    print("Checklist:")
    for item in summary.required_items:
        print(f"- {item.label}: {item.state}")
    print(f"- narrative spec: {summary.spec_state}")
    print(f"- scenes created: {summary.scene_count}")
    print(f"- critique reports: {summary.critique_count}")
    print(f"Next: {summary.next_action}")
    return 0


def handle_build_spec(args: argparse.Namespace) -> int:
    summary = build_spec_ready(args.project_path)
    print(f"Project is ready for spec drafting: {summary.project_root}")
    if summary.spec_state == "placeholder":
        print(
            "Next: write 02_spec/narrative_spec.md with prompts/spec/spec_generator.md."
        )
    else:
        print("Narrative Spec already has custom content.")
    return 0


def handle_scene(args: argparse.Namespace) -> int:
    scene_file = create_scene(
        project_path=args.project_path,
        episode=args.episode,
        scene=args.scene,
        force=args.force,
    )
    print(f"Scene placeholder ready: {scene_file}")
    print("Next: use the outline, narrative spec, and prompts/writing/scene_writer.md.")
    return 0


def handle_critique(args: argparse.Namespace) -> int:
    critique_file = create_critique_report(
        project_path=args.project_path,
        force=args.force,
    )
    print(f"Critique placeholder ready: {critique_file}")
    print("Next: paste in scene text and run your critique prompt(s).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
