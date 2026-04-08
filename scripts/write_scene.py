from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path")
    parser.add_argument("--episode", type=int, required=True)
    parser.add_argument("--scene", type=int, required=True)
    args = parser.parse_args()

    project = Path(args.project_path)
    scene_dir = project / "04_scenes" / f"ep{args.episode:02d}"
    scene_dir.mkdir(parents=True, exist_ok=True)
    scene_file = scene_dir / f"scene_{args.scene:03d}.md"
    if not scene_file.exists():
        scene_file.write_text("INT./EXT. LOCATION - TIME\n\nAction.\n\nCHARACTER\nDialogue.\n", encoding="utf-8")
    print(f"Scene placeholder ready: {scene_file}")
    print("Next step: feed the outline, narrative spec, and prompts/writing/scene_writer.md into your model.")


if __name__ == "__main__":
    main()
