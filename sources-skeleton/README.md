# sources/ — raw material (immutable)

Keep course raw material here, organized by type. Place it **outside the wiki** (a sibling of the vault, typically `<course>/sources/`) and **never modify it.** The wiki (`wiki/<Course>-wiki/`) is a derivative that synthesizes these sources.

```
<course>/
├── sources/            ← here (immutable)
│   ├── textbook/        main textbook
│   ├── readings/        supplementary texts / extra readings
│   ├── slides/          lecture slides
│   ├── transcripts/     lecture transcripts (primary record of what was said)
│   ├── notes-raw/       handwritten notes (original scans/photos)
│   ├── notes-clean/     cleaned-up notes (your own write-up)
│   ├── hw/              homework / problem sets
│   └── exams/           past exams / question banks
└── wiki/<Course>-wiki/ ← LLM wiki (derivative)
```

## Material → wiki mapping
| Material | Folder | Role in the wiki |
| --- | --- | --- |
| Main textbook | `textbook/` | Chapter's representative `source:`; the **authoritative basis** for definitions/theorems |
| Supplementary texts / readings | `readings/` | Secondary sources (alternate views/proofs); cited from concept/topic pages |
| Lecture slides | `slides/` | **The basis for unit structure** → 1:1 with `chapters/`; crop diagrams → `attachments/` |
| Lecture transcripts | `transcripts/` | **Primary record of what was said** — explanations/emphasis/examples slides omit; emphasis → `summary/`, instructor examples → `topics/` |
| Handwritten notes (scans) | `notes-raw/` | Copy images to `attachments/` → embed in `topics/` |
| Cleaned-up notes | `notes-clean/` | **Primary ingest content** (fastest) → verify against the textbook |
| Homework / problem sets | `hw/` | Practice problems/solutions → `topics/` (solution patterns), Query |
| Past exams / question banks | `exams/` | No content; **emphasis & assessment signals** → `summary/`, `topics/`, Query |

## Rules
1. **Immutable**: never touch the originals. The wiki holds only derived notes + copies of figures for embedding.
2. **Authority (on conflict)**: lecture material (slides·transcript) > cleaned-up notes > main textbook > past exams. (Since exams follow the lectures, lecture material wins.) Flag conflicts in the wiki with `> ⚠️ conflict: …` and log them.
3. **Citation**: a chapter's `source:` is a single representative source; in the body cite the rest as `〔reading §x〕` / `〔notes p.y〕`.
4. If the material already lives under a different folder name (e.g. `course_files_export/`), use it as-is and just point the vault `CLAUDE.md`'s `SOURCE_DIRS` at it.

> Each folder keeps a `.gitkeep` so the empty folder is tracked. Once you add real files you can delete it.
