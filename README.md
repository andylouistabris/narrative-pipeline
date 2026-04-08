# Narrative Pipeline

[繁體中文說明](README.zh-TW.md)

Narrative Pipeline is a lightweight repo for human-AI collaborative writing. It keeps the workflow simple: prepare story inputs, draft a `Narrative Spec`, write one scene at a time, then run critique and revision loops.

This is not a one-click writing toy. It is a controlled long-form workflow with clear files, prompts, and human decision points.

## Four Layers
1. Development: premise, characters, worldbuilding, outline.
2. Generation: scene-by-scene drafting.
3. Critique: structure, pacing, logic, consistency, and tone review.
4. Human Decision Layer: accept, reject, rewrite, and curate.

## Quick Start
### Fastest on Windows
Run the one-click setup script from the repo root:

```bat
start.bat
```

It creates `.venv`, installs the local package, and prints the next commands to run.

Create your first project with the same script:

```bat
start.bat init my_story
start.bat status projects\my_story
```

### Manual Setup
Clone the repo, create a virtual environment, and install the CLI.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Create your first project:

```bash
narrative-pipeline init my_story
narrative-pipeline status projects/my_story
```

Fill in these three files first:

- `projects/my_story/00_brief/premise.md`
- `projects/my_story/01_development/characters.yaml`
- `projects/my_story/03_outline/outline.md`

Then continue with the main workflow:

```bash
narrative-pipeline build-spec projects/my_story
narrative-pipeline scene projects/my_story --episode 1 --scene 1
narrative-pipeline critique projects/my_story
```

If you do not want to install the CLI, the old script entrypoints still work:

```bash
python scripts/init_project.py my_story
python scripts/build_spec.py projects/my_story
python scripts/write_scene.py projects/my_story --episode 1 --scene 1
python scripts/run_critique.py projects/my_story
```

## Simplified Workflow
1. Run `narrative-pipeline init <name>` to scaffold a project under `projects/<name>/`.
2. Run `narrative-pipeline status <project>` to see which files are still placeholders.
3. Replace the placeholder content in premise, characters, and outline.
4. Run `narrative-pipeline build-spec <project>` to confirm the project is ready for `narrative_spec.md`.
5. Draft `02_spec/narrative_spec.md` with `prompts/spec/spec_generator.md`.
6. Run `narrative-pipeline scene <project> --episode N --scene M` for each scene stub you want.
7. Run `narrative-pipeline critique <project>` to create a merged critique sheet.

## Project Structure
```text
narrative-pipeline/
|-- docs/
|-- examples/
|-- prompts/
|-- scripts/
|-- src/
|-- templates/
|-- tests/
`-- .github/workflows/
```

Each project created by `init` follows this layout:

```text
projects/my_story/
|-- 00_brief/
|-- 01_development/
|-- 02_spec/
|-- 03_outline/
|-- 04_scenes/
|-- 05_critiques/
|-- 06_revisions/
`-- 07_exports/
```

## Naming Decision
This repo does not use `Canon` as a system label. The rules document is called `Narrative Spec`, and the main file is `narrative_spec.md`.

## What the CLI Does
- `init`: creates a project scaffold and starter files.
- `status`: shows what is missing, still a placeholder, or ready.
- `build-spec`: checks whether premise, characters, and outline have real content.
- `scene`: creates a scene file for a specific episode and scene number.
- `critique`: creates a critique report placeholder.

## Roadmap
- richer project status reporting
- prompt registry and prompt bundles
- spec drafting helpers
- scene batch generation helpers
- critique aggregation
- export helpers for screenplay and prose workflows
