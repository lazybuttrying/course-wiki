# Figure 크롭 레시피 (PDF → attachments 임베드)

`{{MATH}}`/PDF 중심 수업에서 **글로 설명하기 어려운 그림**(다이어그램·plot·phase portrait·회로도 등)을 원본 PDF에서 잘라 위키에 넣는다.
필요 도구: `pdftoppm`(poppler) · `magick`(ImageMagick). macOS: `brew install poppler imagemagick`.

> 텍스트로 충분한 것(공식·정의)은 **넣지 않는다.** 그림이 정보를 더할 때만.

## 흐름
```bash
WD=/tmp/crop; mkdir -p "$WD"; cd "$WD"
SRC="/path/to/SOURCE.pdf"

# 1) 저해상도 썸네일 → 라벨 몽타주로 '그림 있는 페이지' 찾기
pdftoppm -png -r 50 "$SRC" p
magick montage p-*.png -tile 6x -geometry 230x -pointsize 22 -label '%f' montage.png
#   → montage.png 를 (Read 도구로) 보고 그림이 있는 페이지 번호 N 식별

# 2) 그 페이지만 고해상도 렌더
pdftoppm -png -r 200 -f N -l N "$SRC" hi

# 3) 영역 크롭  -crop WIDTHxHEIGHT+X+Y  (좌상단 기준 px; 200dpi에서 letter ≈ 1700x2200)
magick "hi-NN.png" -crop 1620x900+50+40 +repage fig.png
#   → fig.png 를 보고 잘림/여백 확인 후 좌표 보정. 반복.

# 4) vault로 복사 + 임베드
cp fig.png  <vault>/attachments/<descriptive-name>.png
```
노트에 삽입:
```markdown
![[<descriptive-name>.png|520]]
*캡션 — 무엇을 보여주는지. 〔SOURCE.pdf p.N, Fig x.y〕*
```

## 팁
- **페이지 식별이 핵심**: 몽타주를 먼저 보고 후보를 좁힌 뒤 고해상도는 그 페이지만 렌더(시간·토큰 절약).
- **basename 고유**하게: `ch9_phase_real.png`처럼 수업·주제를 접두. (Obsidian은 basename으로 임베드 해석)
- **손글씨 강의노트의 도식·증명**은 크롭 대신 원본 스캔 이미지를 그대로 `attachments/`에 복사해 `![[orig.png]]`로 임베드.
- 크롭 좌표는 **한 번에 안 맞는 게 정상** — 잘라서 보고(2~3회) 보정.
- 폭 지정 `![[img.png|520]]` 으로 노트 가독성 유지.
