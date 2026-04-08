"""Core project helpers for Narrative Pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil

PROJECT_SUBDIRECTORIES = [
    "00_brief",
    "01_development",
    "02_spec",
    "03_outline",
    "04_scenes/ep01",
    "05_critiques",
    "06_revisions",
    "07_exports",
]

PROJECT_TEMPLATES = {
    "00_brief/premise.md": "templates/idea.template.md",
    "01_development/characters.yaml": "templates/character.template.yaml",
    "02_spec/narrative_spec.md": "templates/narrative_spec.template.md",
    "03_outline/outline.md": "templates/outline.template.md",
}

REQUIRED_INPUTS = {
    "premise": "00_brief/premise.md",
    "characters": "01_development/characters.yaml",
    "outline": "03_outline/outline.md",
}

SCENE_TEMPLATE = "templates/scene.template.md"
CRITIQUE_TEMPLATE = "templates/critique.template.md"
SPEC_TEMPLATE = "templates/narrative_spec.template.md"


@dataclass(frozen=True)
class StatusItem:
    label: str
    state: str
    path: Path


@dataclass(frozen=True)
class StatusSummary:
    project_root: Path
    required_items: list[StatusItem]
    spec_state: str
    scene_count: int
    critique_count: int
    next_action: str


@dataclass(frozen=True)
class InitResult:
    project_root: Path
    created_files: list[Path]
    skipped_files: list[Path]


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").strip()


def find_repo_root(start: Path | None = None) -> Path:
    candidates: list[Path] = []
    if start is not None:
        start = start.resolve()
        candidates.extend([start, *start.parents])

    module_path = Path(__file__).resolve()
    candidates.extend(module_path.parents)

    cwd = Path.cwd().resolve()
    candidates.extend([cwd, *cwd.parents])

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / "templates").is_dir() and (candidate / "prompts").is_dir():
            return candidate

    raise FileNotFoundError(
        "Could not locate the Narrative Pipeline repo root. Run commands inside the repo clone."
    )


def resolve_repo_path(path: Path, repo_root: Path) -> Path:
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def resolve_project_path(project_path: str | Path, repo_root: Path | None = None) -> Path:
    repo_root = repo_root or find_repo_root()
    return resolve_repo_path(Path(project_path), repo_root)


def read_template(repo_root: Path, template_relative_path: str) -> str:
    template_path = repo_root / template_relative_path
    return template_path.read_text(encoding="utf-8")


def file_state(path: Path, template_text: str | None = None) -> str:
    if not path.exists():
        return "missing"
    content = normalize_text(path.read_text(encoding="utf-8"))
    if not content:
        return "empty"
    if template_text is not None and content == normalize_text(template_text):
        return "placeholder"
    return "ready"


def project_status(project_path: str | Path, repo_root: Path | None = None) -> StatusSummary:
    repo_root = repo_root or find_repo_root()
    project_root = resolve_project_path(project_path, repo_root=repo_root)

    required_items: list[StatusItem] = []
    for label, relative_path in REQUIRED_INPUTS.items():
        template_relative_path = PROJECT_TEMPLATES[relative_path]
        state = file_state(
            project_root / relative_path,
            template_text=read_template(repo_root, template_relative_path),
        )
        required_items.append(
            StatusItem(label=label, state=state, path=project_root / relative_path)
        )

    spec_path = project_root / "02_spec" / "narrative_spec.md"
    spec_state = file_state(spec_path, template_text=read_template(repo_root, SPEC_TEMPLATE))
    scene_count = len(list((project_root / "04_scenes").glob("ep*/scene_*.md")))
    critique_count = len(list((project_root / "05_critiques").glob("*.md")))

    if any(item.state != "ready" for item in required_items):
        next_action = (
            "Fill in premise, characters, and outline, then run "
            f"`narrative-pipeline build-spec {project_root}`."
        )
    elif spec_state != "ready":
        next_action = (
            "Use prompts/spec/spec_generator.md to draft 02_spec/narrative_spec.md."
        )
    elif scene_count == 0:
        next_action = (
            "Create your first scene with "
            f"`narrative-pipeline scene {project_root} --episode 1 --scene 1`."
        )
    elif critique_count == 0:
        next_action = (
            "Create a critique placeholder with "
            f"`narrative-pipeline critique {project_root}`."
        )
    else:
        next_action = "Keep writing scenes, run critiques, and iterate on revisions."

    return StatusSummary(
        project_root=project_root,
        required_items=required_items,
        spec_state=spec_state,
        scene_count=scene_count,
        critique_count=critique_count,
        next_action=next_action,
    )


def default_project_config(project_name: str) -> str:
    return (
        f"name: {project_name}\n"
        "format: series\n"
        "status: development\n"
        "naming: Narrative Spec\n"
    )


def init_project(
    project_name: str,
    projects_dir: str | Path = "projects",
    repo_root: Path | None = None,
    force: bool = False,
) -> InitResult:
    repo_root = repo_root or find_repo_root()
    project_name = project_name.strip()
    if not project_name:
        raise ValueError("Project name cannot be empty.")

    projects_root = resolve_repo_path(Path(projects_dir), repo_root)
    project_root = projects_root / project_name
    project_root.mkdir(parents=True, exist_ok=True)

    for subdirectory in PROJECT_SUBDIRECTORIES:
        (project_root / subdirectory).mkdir(parents=True, exist_ok=True)

    created_files: list[Path] = []
    skipped_files: list[Path] = []

    for destination_relative_path, template_relative_path in PROJECT_TEMPLATES.items():
        destination_path = project_root / destination_relative_path
        if destination_path.exists() and not force:
            skipped_files.append(destination_path)
            continue
        shutil.copyfile(repo_root / template_relative_path, destination_path)
        created_files.append(destination_path)

    project_config_path = project_root / "project.yaml"
    if project_config_path.exists() and not force:
        skipped_files.append(project_config_path)
    else:
        project_config_path.write_text(
            default_project_config(project_name),
            encoding="utf-8",
        )
        created_files.append(project_config_path)

    return InitResult(
        project_root=project_root,
        created_files=created_files,
        skipped_files=skipped_files,
    )


def build_spec_ready(project_path: str | Path, repo_root: Path | None = None) -> StatusSummary:
    summary = project_status(project_path, repo_root=repo_root)
    incomplete_items = [item for item in summary.required_items if item.state != "ready"]
    if incomplete_items:
        details = ", ".join(f"{item.label} ({item.state})" for item in incomplete_items)
        raise ValueError(
            "Project is not ready for spec drafting yet. Update these files first: "
            f"{details}."
        )
    return summary


def create_scene(
    project_path: str | Path,
    episode: int,
    scene: int,
    repo_root: Path | None = None,
    force: bool = False,
) -> Path:
    if episode < 1 or scene < 1:
        raise ValueError("Episode and scene numbers must be 1 or greater.")

    repo_root = repo_root or find_repo_root()
    project_root = resolve_project_path(project_path, repo_root=repo_root)
    scene_dir = project_root / "04_scenes" / f"ep{episode:02d}"
    scene_dir.mkdir(parents=True, exist_ok=True)
    scene_path = scene_dir / f"scene_{scene:03d}.md"

    if scene_path.exists() and not force:
        return scene_path

    template = read_template(repo_root, SCENE_TEMPLATE)
    scene_text = f"# Episode {episode:02d} Scene {scene:03d}\n\n{template.strip()}\n"
    scene_path.write_text(scene_text, encoding="utf-8")
    return scene_path


def create_critique_report(
    project_path: str | Path,
    repo_root: Path | None = None,
    force: bool = False,
) -> Path:
    repo_root = repo_root or find_repo_root()
    project_root = resolve_project_path(project_path, repo_root=repo_root)
    critique_dir = project_root / "05_critiques"
    critique_dir.mkdir(parents=True, exist_ok=True)
    critique_path = critique_dir / "merged_report.md"

    if critique_path.exists() and not force:
        return critique_path

    critique_text = read_template(repo_root, CRITIQUE_TEMPLATE).strip() + "\n"
    critique_path.write_text(critique_text, encoding="utf-8")
    return critique_path
