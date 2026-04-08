from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout


def main() -> int:
    workspace = Path(tempfile.mkdtemp(prefix="narrative-pipeline-readme-"))
    try:
        projects_dir = workspace / "projects"
        project_path = projects_dir / "my_story"

        init_output = run(
            [
                sys.executable,
                "-m",
                "narrative_pipeline",
                "init",
                "my_story",
                "--projects-dir",
                str(projects_dir),
            ],
            cwd=REPO_ROOT,
        )
        if "Project ready:" not in init_output:
            raise AssertionError("CLI init output did not include the expected summary.")

        status_output = run(
            [
                sys.executable,
                "-m",
                "narrative_pipeline",
                "status",
                str(project_path),
            ],
            cwd=REPO_ROOT,
        )
        if "premise: placeholder" not in status_output:
            raise AssertionError("CLI status output did not report placeholder inputs.")

        (project_path / "00_brief" / "premise.md").write_text(
            "# Project Brief\n\nA washed-up action star wakes inside a live-streamed coup.\n",
            encoding="utf-8",
        )
        (project_path / "01_development" / "characters.yaml").write_text(
            "name: Ren\nrole: actor\nwant: survive the coup and expose the producers\n",
            encoding="utf-8",
        )
        (project_path / "03_outline" / "outline.md").write_text(
            "# Outline\n\n## Setup\nRen realizes the coup is scripted around him.\n",
            encoding="utf-8",
        )

        build_output = run(
            [
                sys.executable,
                "-m",
                "narrative_pipeline",
                "build-spec",
                str(project_path),
            ],
            cwd=REPO_ROOT,
        )
        if "ready for spec drafting" not in build_output:
            raise AssertionError("CLI build-spec output did not confirm readiness.")

        run(
            [
                sys.executable,
                "-m",
                "narrative_pipeline",
                "scene",
                str(project_path),
                "--episode",
                "1",
                "--scene",
                "1",
            ],
            cwd=REPO_ROOT,
        )
        run(
            [
                sys.executable,
                "-m",
                "narrative_pipeline",
                "critique",
                str(project_path),
            ],
            cwd=REPO_ROOT,
        )

        if not (project_path / "04_scenes" / "ep01" / "scene_001.md").exists():
            raise AssertionError("Scene creation smoke test failed.")
        if not (project_path / "05_critiques" / "merged_report.md").exists():
            raise AssertionError("Critique creation smoke test failed.")

        legacy_workspace = workspace / "legacy_repo"
        shutil.copytree(REPO_ROOT, legacy_workspace, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__"))
        run([sys.executable, "scripts/init_project.py", "legacy_story"], cwd=legacy_workspace)
        if not (legacy_workspace / "projects" / "legacy_story" / "project.yaml").exists():
            raise AssertionError("Legacy script smoke test failed.")

        print("README command smoke tests passed.")
        return 0
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
