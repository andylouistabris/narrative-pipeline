"""Narrative Pipeline package."""

from .project import (
    build_spec_ready,
    create_critique_report,
    create_scene,
    find_repo_root,
    init_project,
    project_status,
)

__all__ = [
    "build_spec_ready",
    "create_critique_report",
    "create_scene",
    "find_repo_root",
    "init_project",
    "project_status",
]

__version__ = "0.1.0"
