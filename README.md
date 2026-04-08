# Narrative Pipeline

Canon-free naming version. A narrative development and scene-generation workflow for human-AI collaborative writing.

## Positioning
Narrative Pipeline is a repo skeleton for a writing workflow that separates story development, narrative rules, scene generation, critique loops, and revision tracking.

It is not a "one-click masterpiece generator." It is an operating framework for controlled long-form writing.

## Core Layers
1. Development layer: characters, worldbuilding, premise, beats, outline.
2. Writing layer: scene generation and continuation.
3. Infrastructure layer: version control, automation, review, export.

## Core Concepts
- Narrative Spec: the ruleset that constrains generation.
- Scene Writing: goal-driven scene production.
- Critique Loop: structure, pacing, logic, and revision summaries.
- Human Decision Layer: final acceptance, rejection, rewriting, and taste judgment.

## Project Structure
```text
narrative-pipeline/
├─ docs/
├─ templates/
├─ examples/
├─ prompts/
├─ scripts/
├─ src/
├─ tests/
└─ .github/workflows/
```

## Quick Start
```bash
python scripts/init_project.py my_story
python scripts/build_spec.py projects/my_story
python scripts/write_scene.py projects/my_story --episode 1 --scene 1
python scripts/run_critique.py projects/my_story
```

## Recommended File Flow
1. Write premise and project brief.
2. Build character and world files.
3. Draft outline.
4. Build `narrative_spec.md`.
5. Generate scenes.
6. Run critique loop.
7. Merge accepted revisions.
8. Export draft.

## Naming Decision
This repo does not use `Canon` as a system label. It uses `Narrative Spec` instead.

## Roadmap
- CLI entrypoint
- prompt registry
- spec validator
- scene batch generation
- critique aggregation
- screenplay export
- GitHub Actions automation

## License
Apache-2.0 recommended.
