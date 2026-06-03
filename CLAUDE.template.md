<!-- BOOTSTRAP:START -->
<!--
  ┌─────────────────────────────────────────────────────────────────────┐
  │  COURSE-WIKI HARNESS  ·  self-contained schema for an LLM-maintained  │
  │  course knowledge base (Andrej Karpathy "LLM Wiki" pattern).         │
  │                                                                       │
  │  HOW TO USE: copy this file into a new vault as `CLAUDE.md`, then     │
  │  replace every {{PLACEHOLDER}} below. After that, an LLM reading      │
  │  this file becomes a disciplined wiki maintainer for the course.     │
  │  This file is course-agnostic; the only course-specific parts are    │
  │  the placeholders.                                                    │
  └─────────────────────────────────────────────────────────────────────┘
-->
<!-- BOOTSTRAP:END -->

# {{COURSE}}-wiki schema (LLM Wiki maintenance rules)

This vault follows Andrej Karpathy's **"LLM Wiki"** pattern. This file is the config that makes the LLM act not as a general chatbot but as a **disciplined wiki maintainer**. Follow the rules below whenever you create or extend the wiki.

<!-- BOOTSTRAP:START — bootstrap.sh removes this block (including the --- below) when it generates an instance vault -->

---

## ⚡ Bootstrap — start a new course wiki

**Automatic (recommended)** — one command from the harness repo:
```bash
./bootstrap.sh -c "Causal Inference" -v ../class/causality/wiki/Causality-wiki \
               -s "../../course_files_export/" -u lecture -m on -e on
```
→ copies `template-vault/` + substitutes `{{placeholder}}`s + stamps the date + records `wiki.config.yml`. After that, you only need to Ingest.

**Manual (4 steps)**:
1. **Create the vault**: make a `<course>/wiki/{{VAULT}}/` folder and copy this file into it as `CLAUDE.md`.
2. **Substitute placeholders**: replace all `{{...}}` in the table below with real values. (Once.)
3. **Connect sources**: put the immutable originals in `{{SOURCE_DIRS}}` (or just point at the path) and never modify them.
4. **Run Ingest**: tell the LLM "ingest <sources> per this schema" → it creates unit pages → updates `index.md`/`log.md`.

> The empty vault skeleton (index/log/Welcome/folders/`.obsidian/graph.json`) is in `template-vault/`. Copy it as-is and you only need steps 2–4.

### Placeholders (substitute just this table)
| placeholder | meaning | example |
| --- | --- | --- |
| `{{COURSE}}` | course name | `Causality`, `ODE`, `Policy` |
| `{{VAULT}}` | vault folder name | `Causality-wiki` |
| `{{SOURCE_DIRS}}` | immutable source location(s) | `../../readings/`, `../../slides/` |
| `{{SOURCE_TYPES}}` | source forms | PDF · slides · papers · readings · lecture notes |
| `{{UNIT}}` | per-source unit (= what `chapters/` holds) | `chapter` · `week` · `lecture` · `module` · `paper` |
| `{{KEEP_ENGLISH_TERMS}}` | keep technical terms as their original English | `on` (recommended for math/STEM) / `off` |
| `{{MATH}}` | LaTeX math module | `on` (STEM) / `off` (humanities, policy, etc.) |

> If `{{UNIT}}` is not `chapter`, rename the `chapters/` folder to that name (e.g. `weeks/`), and update the graph color queries and the lint arguments below to match.

<!-- BOOTSTRAP:END -->

---

## 1. 3-Layer structure (immutable core)
1. **Sources (immutable)** — the `{{SOURCE_TYPES}}` originals (`{{SOURCE_DIRS}}`). **Never modify them.** The wiki is a derivative of these sources.
2. **Wiki (this folder)** — interlinked markdown generated from the sources.
3. **Schema (this file)** — structure, rules, workflow. The LLM follows this file before every task.

### 1.5 Source placement (what goes where)
All raw material is **immutable source** — kept **outside** the vault, usually under `<course>/sources/` (a sibling of the vault), organized by type. The vault holds only derivatives (notes) + **copies** of figures for embedding. Don't make a separate wiki page per material type — **a single chapter page synthesizes multiple sources**.

| material | source location | role in the wiki |
| --- | --- | --- |
| main textbook | `sources/textbook/` | chapter's representative `source:`; the **authoritative basis** for definitions/theorems (the ground truth for cross-checking) |
| supplementary texts / readings | `sources/readings/` | secondary sources (alternate views/proofs); cited from concept/topic pages |
| lecture slides | `sources/slides/` | **the basis for unit (chapter) structure** → 1:1 with `chapters/`; crop diagrams → `attachments/` |
| lecture transcripts | `sources/transcripts/` | **primary record of what was said** — explanations, emphasis, examples, intuition the slides omit. Emphasis → `summary/`, instructor examples → `topics/` |
| handwritten notes (scans) | `sources/notes-raw/` | copy images to `attachments/` → embed in `topics/` with `![[..]]` |
| cleaned-up notes | `sources/notes-clean/` | **primary ingest content** (fastest) → verify against the textbook |
| homework / problem sets | `sources/hw/` | practice problems/solutions → `topics/` (solution patterns), Query; what to practice |
| past exams / question banks | `sources/exams/` | no content; **emphasis & assessment signals** → `summary/`, `topics/`, Query |

- **Authority (priority on conflict)**: lecture material (slides·transcript) > cleaned-up notes > main textbook > past exams. (Since exams/assessment follow the lectures, lecture material wins; transcripts are verbatim, so they're especially useful for catching emphasis/intent.) Flag conflicts with `> ⚠️ conflict: …〔src1〕 vs …〔src2〕` + a `log.md` entry (when contradiction-flagging is ON).
- **Citation**: a chapter's frontmatter `source:` is a single representative (the main textbook or slides); cite the rest in the body as `〔reading §x〕` / `〔notes p.y〕`.
- The folder skeleton is the harness's `sources-skeleton/` (create it next to the vault with `bootstrap.sh -S <dir>`). If the material already exists, you can keep its existing folder name (e.g. `course_files_export/`).

## 2. Folder layout
- Root (meta): `index.md` (catalog/home MOC), `log.md` (append-only), `CLAUDE.md` (this file), `Welcome.md` (→ redirect to index).
- `chapters/` — **unit pages** (= per-source summary). 1 {{UNIT}} = 1 source = 1 page.
- `concepts/` — cross-unit **concept pages** (hubs for key ideas that recur across multiple {{UNIT}}s).
- `topics/` — single-topic **deep notes** (images, proofs, examples, etc.). Linked from the relevant unit/concept page.
- `summary/` — synthesis (cheat sheets, checklists, syntheses).
- `attachments/` — image/figure assets. Notes reference them with an `![[name.png]]` (basename) embed.

**Link rule**: Obsidian `[[link]]` / `![[embed]]` resolve by **basename** → they survive moving a file into a subfolder. So **basenames must be unique within the vault** (no two chapters/concepts with the same name; no alias clashes either).

## 3. Page conventions
- **Frontmatter (YAML) required**:
  ```yaml
  ---
  tags: [{{COURSE}}, <topic>]
  aliases: ["<English name>", "<alias>"]
  type: chapter | concept | topic | synthesis | index | log | schema
  source: "{{SOURCE_DIRS}}<file>"   # chapter pages only (representative source)
  updated: YYYY-MM-DD
  ---
  ```
- **Cross-linking**: when a concept first appears, link it as `[[concept]]`. At the bottom of each page, under `## Related Notes`, add **bidirectional** links (both concept→chapter and chapter→concept). If only one side exists, lint catches it.
- **Citation**: next to a fact/formula, use the `〔<source> §x.y〕` form. Chapter pages cite their representative via the frontmatter `source`.
- **Open question (data gap)**: if the source is uncertain or needs verification, mark it with a `> ❓ **open question**: …` callout and also register it in `log.md`/`index.md`.
- **Terminology** (when `{{KEEP_ENGLISH_TERMS}}=on`): keep technical terms as their **original English** (don't translate). Only the connective prose is in your chosen body language.
- **Math** (when `{{MATH}}=on`): standardize on LaTeX `$...$` (inline) / `$$...$$` (block). KaTeX/MathJax conventions.

## 4. Workflow
- **Ingest** (add a new source): read the source through → write the `chapters/` unit page → update `index.md` → update/create relevant `concepts/` → add bidirectional links → append a `log.md` entry. One source can touch 10–15 pages.
- **Query** (answer a question): search & synthesize relevant pages → answer **with citations**. Reusable answers get filed as a new page so knowledge accumulates.
- **Lint** (health-check): check with the Appendix A checklist (broken links, orphans, back-link asymmetry, missing frontmatter, key terms with no page, open questions). Use `scripts/lint.py`.
- **Contradiction-flagging** (multiple / heterogeneous sources conflict): if a new source **contradicts** an existing claim, don't silently overwrite — record both sources and mark `> ⚠️ **conflict**: A〔src1〕 vs B〔src2〕` → register in `log.md`.
  - ON recommended: courses where **sources are heterogeneous** — papers, multiple authors, multiple semesters (causality, policy, etc.).
  - OFF possible: when conflicts are structurally absent, e.g. **consecutive units of a single textbook** (ODE → OFF; instead track only uncertain handwritten formulas as open questions).

## 5. log.md format
Append-only. Entry prefix: `## [YYYY-MM-DD] ingest|query|lint|refactor|conflict | <title>`. A one-line summary + what you changed.

---

## Appendix A — Lint checklist
`python3 scripts/lint.py .` (or the vault path). Items checked:
1. **broken wikilink / image embed** — does the `[[...]]`/`![[...]]` target actually exist as a file/alias/attachment? (a code-span `` `[[...]]` `` is exempt)
2. **orphan** — pages with 0 inbound links (the landing `Welcome` is exempt). Make them linked from the index.
3. **back-link asymmetry** — a concept→chapter link exists but the chapter→concept back-link is missing → add it under `## Related Notes`.
4. **frontmatter missing** — pages missing `type`/`updated`/`tags`.
5. **key terms without their own page** — concepts mentioned often but with no dedicated page (create a concept/topic if needed, otherwise defer).
6. **open question / conflict** — the list of unresolved data gaps / conflicts.

## Appendix B — Figure crop recipe (`{{MATH}}`/PDF course option)
Crop reference figures (diagrams, plots, portraits) from the source PDF into `attachments/` and embed them. (needs `pdftoppm` · `magick`/ImageMagick)
```bash
WD=/tmp/crop; mkdir -p "$WD"; cd "$WD"
# 1) low-res thumbnails → label montage to find 'pages with figures'
pdftoppm -png -r 50 "SOURCE.pdf" p
magick montage p-*.png -tile 6x -geometry 230x -pointsize 22 -label '%f' montage.png   # read it to identify the page
# 2) render only that page at high res
pdftoppm -png -r 200 -f <N> -l <N> "SOURCE.pdf" hi
# 3) crop the region (WxH+X+Y) → read it to adjust coordinates
magick "hi-<N>.png" -crop 1620x900+50+40 +repage fig.png
# 4) copy into the vault and embed:  attachments/fig.png  →  ![[fig.png|520]]  + caption 〔source p.N〕
```
> For diagrams/proofs in handwritten lecture notes, embed the original image directly in `topics/` (`![[orig.png]]`); for textbook figures, crop with the method above.

## Appendix C — Obsidian graph color preset
The `colorGroups` in `.obsidian/graph.json` (color by folder, priority = top-down). `template-vault/.obsidian/graph.json` ships with the same preset.
```json
"colorGroups": [
  { "query": "path:\"summary/\"",  "color": { "a": 1, "rgb": 16347926 } },
  { "query": "path:concepts/",     "color": { "a": 1, "rgb": 2278750  } },
  { "query": "path:chapters/",     "color": { "a": 1, "rgb": 3900150  } },
  { "query": "path:topics/",       "color": { "a": 1, "rgb": 11032055 } }
]
```
Colors are the decimal of `0xRRGGBB`. To highlight only specific nodes, add a group at the top like `"query": "path:\"summary/Cheat Sheet\""`. To apply changes, in Obsidian run `Cmd+P → Reload app without saving`.

---

## Appendix D — Whether this pattern fits / how to adjust (honest limits)
- **Good fit**: when sources are fixed and structured (textbooks, lectures) and you're accumulating a semester's knowledge over time. The LLM does the bookkeeping (summaries, cross-references, lint) tirelessly.
- **Can be overkill**: if there are only 1–2 sources or it's a one-off write-up, the wiki infrastructure (index/log/concept separation) is overhead — a single document is better.
- **Contradiction flagging** is only valuable with heterogeneous sources (see Appendix 4). For a single textbook, turn it off and just use open questions.

---

## Appendix E — Page examples & Ingest/Query worked example
Page skeletons are in `template-vault/_templates/` (chapter · concept · topic · cheatsheet). Copy and fill them in. Minimal examples:

**chapter** (`chapters/L1 - Association vs Causation.md`)
```markdown
---
tags: [Causal-Inference, lecture, association]
aliases: ["Lecture 1", "Association vs Causation"]
type: chapter
chapter: 1
source: "../../course_files_export/1. Association vs causation.pdf"
updated: 2026-05-31
---
# L1 — Association vs Causation
> source: 〔Lecture 1〕 · synthesis: [[Cheat Sheet]] · concept: [[Exchangeability]]
- RD $=\Pr(Y{=}1\mid A{=}1)-\Pr(Y{=}1\mid A{=}0)$ …
## Related Notes
- concept: [[Exchangeability]] · next: [[L2 - …]] · index: [[index]]
```
**concept** (`concepts/Exchangeability.md`) — back-links the chapter (bidirectional):
```markdown
---
type: concept
tags: [Causal-Inference, concept, exchangeability]
aliases: ["Exchangeability", "ignorability"]
updated: 2026-05-31
---
# Concept — Exchangeability
## Where it's used
- [[L1 - Association vs Causation]]: condition for association = causation.
- [[L2 - …]]: guaranteed by randomization.
```

**Ingest (worked)**: read the source/cleaned notes through → ① write `chapters/L1` → ② add one line to the chapters section of `index.md` → ③ a new concept `Exchangeability` appeared, so create `concepts/Exchangeability` and link L1↔concept bidirectionally → ④ add the matching item to `summary/Cheat Sheet` → ⑤ record `## [date] ingest | L1` in `log.md` → ⑥ check with `lint.py`. (One source touches 5–10 pages.)

**Query (worked)**: "difference between exchangeability and positivity?" → search & synthesize `concepts/Exchangeability` · `chapters/L2-2` → answer **with citations** → if it's a frequent comparison, file it as a new page like `concepts/Identification Conditions` so it accumulates.
