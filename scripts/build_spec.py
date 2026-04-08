from pathlib import Path
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/build_spec.py <project_path>")
        raise SystemExit(1)
    project = Path(sys.argv[1])
    spec_file = project / "02_spec" / "narrative_spec.md"
    if not spec_file.exists():
        raise SystemExit(f"Missing spec file: {spec_file}")
    print(f"Spec placeholder ready: {spec_file}")
    print("Next step: feed project files and prompts/spec/spec_generator.md into your model.")


if __name__ == "__main__":
    main()
