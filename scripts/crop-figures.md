# Figure crop recipe (PDF → attachments embed)

For `{{MATH}}`/PDF-heavy courses, crop **figures that are hard to describe in words** (diagrams, plots, phase portraits, circuit diagrams, etc.) out of the source PDF and put them in the wiki.
Tools needed: `pdftoppm` (poppler) · `magick` (ImageMagick). macOS: `brew install poppler imagemagick`.

> Don't include things that text covers fine (formulas, definitions). Only when a figure adds information.

## Flow
```bash
WD=/tmp/crop; mkdir -p "$WD"; cd "$WD"
SRC="/path/to/SOURCE.pdf"

# 1) low-res thumbnails → labeled montage to find 'pages that have figures'
pdftoppm -png -r 50 "$SRC" p
magick montage p-*.png -tile 6x -geometry 230x -pointsize 22 -label '%f' montage.png
#   → view montage.png (with the Read tool) and identify the page number N that has the figure

# 2) render only that page at high resolution
pdftoppm -png -r 200 -f N -l N "$SRC" hi

# 3) crop the region  -crop WIDTHxHEIGHT+X+Y  (px from top-left; at 200dpi, letter ≈ 1700x2200)
magick "hi-NN.png" -crop 1620x900+50+40 +repage fig.png
#   → view fig.png to check for clipping/margins, then adjust the coordinates. Repeat.

# 4) copy into the vault + embed
cp fig.png  <vault>/attachments/<descriptive-name>.png
```
Insert into a note:
```markdown
![[<descriptive-name>.png|520]]
*Caption — what it shows. 〔SOURCE.pdf p.N, Fig x.y〕*
```

## Tips
- **Page identification is the key**: look at the montage first to narrow candidates, then render only that page at high res (saves time and tokens).
- **Keep basenames unique**: prefix with the course/topic, e.g. `ch9_phase_real.png`. (Obsidian resolves embeds by basename.)
- **For handwritten lecture-note diagrams/proofs**, skip cropping — just copy the original scan into `attachments/` as-is and embed with `![[orig.png]]`.
- Crop coordinates **rarely land on the first try** — that's normal; crop, look (2–3 times), adjust.
- Use a width spec `![[img.png|520]]` to keep notes readable.
