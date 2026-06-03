# _templates/ — page skeletons

Copy from here when creating a new page, then fill it in. Replace the `{{...}}` tokens with real values and move the file into the matching folder.

| Template | → Folder | Use for |
| --- | --- | --- |
| `chapter.md` | `chapters/` | Per-unit summary (lecture/chapter/week) |
| `concept.md` | `concepts/` | Cross-unit concept hub |
| `topic.md` | `topics/` | Single-topic deep dive (proofs, examples, figures) |
| `cheatsheet.md` | `summary/` | Exam/review synthesis |

## Rules (summary)
- **Unique basename**: chapter/concept/topic names must not collide. Alias collisions are also forbidden.
- **Bidirectional links**: concept↔chapter link each other in the related-notes section at the bottom of each page (lint catches asymmetry).
- **Frontmatter required**: `type`, `tags`, `updated` (chapters also need `source`).
- For the full conventions, see `CLAUDE.md` at the vault root.

> This folder is prefixed with `_`, so it's excluded from `lint.py` and ordinary search. Set it as the template folder for Obsidian's core **Templates** plugin to insert these with a shortcut.
