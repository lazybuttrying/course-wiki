# Course-Wiki Harness 🎓📚

A reusable, course-agnostic template for organizing course material (textbooks, slides, papers, lecture notes) into an **LLM-maintained wiki**.
It follows Andrej Karpathy's [**LLM Wiki**](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern — instead of re-retrieving everything each time like RAG, the LLM **incrementally builds and maintains an interlinked markdown wiki**. The structure was validated on an ODE course, then generalized into a subject-agnostic template. Subject-general by default, with optional math/figure modules.

## What's inside
| File / folder | Role |
| --- | --- |
| **`CLAUDE.template.md`** | ⭐ The core. A self-contained schema — structure, conventions, workflows, recipes, examples. Copy into a new vault as `CLAUDE.md`. |
| **`bootstrap.sh`** | Spin up a new course vault in one command + substitute `{{placeholders}}` + date stamp + `wiki.config.yml`. |
| `template-vault/` | Empty vault skeleton (index · log · Welcome · folders · graph color preset). |
| `template-vault/_templates/` | **Page skeletons** (chapter · concept · topic · cheatsheet). Copy when creating a new page. |
| `scripts/lint.py` | Wiki health-check (broken links · orphans · back-link asymmetry · frontmatter · terms). `--report` emits markdown. |
| `scripts/crop-figures.md` | PDF figure crop → embed recipe (STEM/PDF option). |
| `sources-skeleton/` | Source-material folder skeleton (textbook · readings · slides · transcripts · notes-raw · notes-clean · hw · exams + placement guide). Created next to the vault via `bootstrap.sh -S`. |
| `wiki.config.example.yml` | Example course config. |
| `.github/workflows/lint.yml` | CI — lint + bootstrap smoke test on every push/PR. |

> This repo is a **separate directory from the course content** (default location `~/Desktop/project/course-wiki/`). Run the commands below from the repo root. Set `HARNESS` to this repo's path.

## Quick start (new course)
**Automatic (recommended)** — one command from the repo root:
```bash
./bootstrap.sh -c "Causal Inference" \
               -v ../class/causality/wiki/Causality-wiki \
               -s "../../course_files_export/" \
               -u lecture -m on -e on
#  -c course name  -v vault path  -s source path  -u unit (chapter|week|lecture|module|paper)
#  -m MATH (on|off)  -e English terms (on|off)  -t source types (description)
```
→ vault created + placeholders substituted + `CLAUDE.md` generated. Then:
```bash
# Tell the LLM: "ingest <sources> per the <vault>/CLAUDE.md schema"
python3 scripts/lint.py <vault>           # check
python3 scripts/lint.py <vault> --report lint.md   # markdown report
```

**Manual** (when automatic doesn't fit): copy `template-vault/` → rename `CLAUDE.template.md` to `CLAUDE.md` → substitute `{{PLACEHOLDER}}` → ingest.

> For new **pages**, copy from the vault's `_templates/` (chapter · concept · topic · cheatsheet) and fill them in.

## Folder structure (generated vault)
```
<Course>-wiki/
├── index.md · log.md · Welcome.md · CLAUDE.md   # meta
├── chapters/      # unit (= chapter/week/lecture/paper) pages
├── concepts/      # cross-unit concept hubs
├── topics/        # deep notes on a single topic (with images)
├── summary/       # cheat sheets · checklists
├── attachments/   # figure assets
└── .obsidian/     # graph color preset, etc.
```

## Managing it as a GitHub template
This repo is already `git init`-ed with an initial commit (a standalone repository, separate from course content). To put it on GitHub:
```bash
cd ~/Desktop/project/course-wiki
gh repo create <you>/course-wiki --public --source=. --push   # gh CLI
# or manually: git remote add origin <url> && git push -u origin main
```
Then check **Settings → Template repository** on the GitHub repo. After that:
- Web: **"Use this template"** → create a new course repo.
- CLI: `gh repo create <Course>-wiki --template <you>/course-wiki`

> Pushing / toggling template status requires your own GitHub permissions, so it isn't automated — just run the commands above.

## Scope
- **General courses**: choose source types (PDF · slides · papers · readings) and units (chapter/week/lecture/module). Works for causality, policy, engineering, etc.
- **Math / STEM**: `{{MATH}}=on` enables LaTeX conventions + the figure-crop recipe.

## FAQ
- **Does it have to be Obsidian?** No. It's just a markdown folder. `[[links]]`, `![[embeds]]`, and graph view are simply more convenient in Obsidian.
- **What about humanities/policy courses with no math or figures?** Works fine. `-m off -e off`. Read `chapters/` semantically as `weeks/` or `lectures/` (to rename the folder, also update the graph color query and the lint `--chapters` argument).
- **Do I have to read the source PDFs?** If you have your own cleaned-up notes, it's faster to ingest those as the primary source and cross-check against the PDFs.
- **Does lint skip `_templates/` and HTML comments?** Yes, both are excluded automatically.
- **When should I *not* use this?** If you have only 1–2 sources or it's a one-off, the wiki infrastructure is overkill — a single document is better. (See `CLAUDE.template.md` Appendix D.)

## Sources
- Pattern: Karpathy, *LLM Wiki* (gist).
- Reference implementation: `class/ode/wiki/ODE-wiki/` (the real case this template was extracted from).

## License
[MIT](LICENSE) © 2026 dyk
