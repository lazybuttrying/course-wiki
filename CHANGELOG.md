# Changelog

This repo loosely follows the [Keep a Changelog](https://keepachangelog.com/) format.

## [1.1.0] — 2026-05-31
### Added
- **Page templates** `template-vault/_templates/`: chapter · concept · topic · cheatsheet skeletons (frontmatter + section structure). Copy and fill them in when creating a new page.
- **Bootstrap automation** `bootstrap.sh`: one command to create a new course vault + substitute `{{placeholder}}`s + stamp the date + record `wiki.config.yml`.
- `wiki.config.example.yml`: an example course config.
- **`sources-skeleton/`**: source-material folder skeleton (textbook·readings·slides·transcripts·notes-raw·notes-clean·hw·exams + a placement-guide README). Created next to the vault via `bootstrap.sh -S <dir>`.
- Added the source type **`transcripts/`** (lecture transcripts) — in the lecture-material tier (top authority), the primary source for explanations/emphasis/examples that the slides omit.
- `CLAUDE.template.md` §1.5 **Source placement**: maps main textbook / supplementary texts / lecture material / handwritten notes / cleaned-up notes / hw / past exams → their wiki roles, plus authority (conflict priority) and citation rules.
- **CI** `.github/workflows/lint.yml`: runs lint on push/PR + a `bootstrap.sh` smoke test + a lint report artifact.
- `LICENSE` (MIT), `CHANGELOG.md`.
- `scripts/lint.py`: `--report <md>` output mode, automatic `_templates/` exclusion, reduced check-6 false positives.
- `CLAUDE.template.md`: BOOTSTRAP block delimiters (`<!-- BOOTSTRAP:START/END -->`), inline page examples, Ingest/Query worked examples.

### Changed
- Moved the repo into a standalone directory separate from the course content (`class/`). Updated the README for standalone use.

## [1.0.0] — 2026-05-30
### Added
- First version: `CLAUDE.template.md` (self-contained schema), `template-vault/` (empty vault skeleton + graph color preset), `scripts/lint.py`, `scripts/crop-figures.md`, `README.md`, `.gitignore`.
- A reusable LLM-Wiki template extracted from `class/ode/wiki/ODE-wiki/`.
