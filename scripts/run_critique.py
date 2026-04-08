from pathlib import Path
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_critique.py <project_path>")
        raise SystemExit(1)
    project = Path(sys.argv[1])
    out = project / "05_critiques" / "merged_report.md"
    out.write_text("# Merged Critique Report\n\n- structure:\n- pacing:\n- logic:\n- consistency:\n- revisions:\n", encoding="utf-8")
    print(f"Critique placeholder ready: {out}")
    print("Next step: feed scene text and prompts/critique/*.md into your model(s).")


if __name__ == "__main__":
    main()
