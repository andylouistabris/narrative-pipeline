from pathlib import Path
import sys
import tempfile
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from narrative_pipeline.project import (  # noqa: E402
    build_spec_ready,
    create_critique_report,
    create_scene,
    init_project,
    project_status,
)


class WorkflowTests(unittest.TestCase):
    def test_init_project_creates_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            result = init_project(
                "demo_story",
                projects_dir=temp_root / "projects",
                repo_root=REPO_ROOT,
            )

            self.assertTrue((result.project_root / "00_brief" / "premise.md").exists())
            self.assertTrue(
                (result.project_root / "01_development" / "characters.yaml").exists()
            )
            self.assertTrue((result.project_root / "03_outline" / "outline.md").exists())
            self.assertTrue((result.project_root / "project.yaml").exists())

    def test_status_and_build_spec_require_real_input_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            result = init_project(
                "demo_story",
                projects_dir=temp_root / "projects",
                repo_root=REPO_ROOT,
            )
            project_root = result.project_root

            summary = project_status(project_root, repo_root=REPO_ROOT)
            self.assertEqual([item.state for item in summary.required_items], ["placeholder"] * 3)

            (project_root / "00_brief" / "premise.md").write_text(
                "# Project Brief\n\nA detective trapped on a night ferry must solve a murder.\n",
                encoding="utf-8",
            )
            (project_root / "01_development" / "characters.yaml").write_text(
                "name: Lin\nrole: detective\nwant: solve the murder before dawn\n",
                encoding="utf-8",
            )
            (project_root / "03_outline" / "outline.md").write_text(
                "# Outline\n\n## Setup\nA body is found on the ferry.\n",
                encoding="utf-8",
            )

            ready_summary = build_spec_ready(project_root, repo_root=REPO_ROOT)
            self.assertEqual([item.state for item in ready_summary.required_items], ["ready"] * 3)
            self.assertEqual(ready_summary.spec_state, "placeholder")

    def test_scene_and_critique_commands_create_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            project_root = init_project(
                "demo_story",
                projects_dir=temp_root / "projects",
                repo_root=REPO_ROOT,
            ).project_root

            scene_path = create_scene(project_root, episode=2, scene=3, repo_root=REPO_ROOT)
            critique_path = create_critique_report(project_root, repo_root=REPO_ROOT)

            self.assertTrue(scene_path.exists())
            self.assertTrue(critique_path.exists())
            self.assertIn("Episode 02 Scene 003", scene_path.read_text(encoding="utf-8"))
            self.assertIn("Critique Report", critique_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
