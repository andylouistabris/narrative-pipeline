from pathlib import Path
import shutil
import sys

TEMPLATES = {
    "00_brief/premise.md": "templates/idea.template.md",
    "01_development/characters.yaml": "templates/character.template.yaml",
    "03_outline/outline.md": "templates/outline.template.md",
    "02_spec/narrative_spec.md": "templates/narrative_spec.template.md",
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/init_project.py <project_name>")
        raise SystemExit(1)
    repo_root = Path(__file__).resolve().parents[1]
    name = sys.argv[1]
    project_root = repo_root / "projects" / name
    for sub in [
        "00_brief", "01_development", "02_spec", "03_outline",
        "04_scenes/ep01", "05_critiques", "06_revisions", "07_exports"
    ]:
        (project_root / sub).mkdir(parents=True, exist_ok=True)
    for dst, src in TEMPLATES.items():
        shutil.copy(repo_root / src, project_root / dst)
    print(f"Initialized project at {project_root}")


if __name__ == "__main__":
    main()
