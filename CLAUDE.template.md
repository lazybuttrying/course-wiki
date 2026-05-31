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

# {{COURSE}}-wiki 스키마 (LLM Wiki 유지 규칙)

이 볼트는 Andrej Karpathy의 **"LLM Wiki"** 패턴을 따른다. 이 파일은 LLM이 일반 챗봇이 아니라 **규율 있는 위키 관리자**로 동작하게 하는 설정 파일이다. 위키를 만들거나 확장할 때 아래 규칙을 따른다.

<!-- BOOTSTRAP:START — bootstrap.sh 가 인스턴스 vault 생성 시 이 블록(아래 --- 포함)을 제거한다 -->

---

## ⚡ Bootstrap — 새 수업 위키 시작

**자동 (권장)** — harness repo에서 한 명령:
```bash
./bootstrap.sh -c "Causal Inference" -v ../class/causality/wiki/Causality-wiki \
               -s "../../course_files_export/" -u lecture -m on -e on
```
→ `template-vault/` 복사 + `{{placeholder}}` 치환 + 날짜 스탬프 + `wiki.config.yml` 기록. 이후 Ingest만 하면 된다.

**수동 (4단계)**:
1. **vault 생성**: `<course>/wiki/{{VAULT}}/` 폴더를 만들고 이 파일을 그 안에 `CLAUDE.md` 로 복사.
2. **placeholder 치환**: 아래 표의 `{{...}}` 를 모두 실제 값으로 바꾼다. (한 번만)
3. **소스 연결**: immutable 원본을 `{{SOURCE_DIRS}}` 에 두고(또는 경로만 가리키고) 절대 수정하지 않는다.
4. **Ingest 실행**: LLM에게 "이 스키마대로 <소스>를 ingest 해줘" → 단위 페이지 생성 → `index.md`·`log.md` 갱신.

> 빈 vault 스켈레톤(index/log/Welcome/폴더/`.obsidian/graph.json`)은 `template-vault/` 에 있다. 그대로 복사하면 2~4단계만 하면 된다.

### Placeholders (이 표만 치환하면 됨)
| placeholder | 의미 | 예시 |
| --- | --- | --- |
| `{{COURSE}}` | 수업 이름 | `Causality`, `ODE`, `Policy` |
| `{{VAULT}}` | vault 폴더명 | `Causality-wiki` |
| `{{SOURCE_DIRS}}` | immutable 소스 위치(들) | `../../readings/`, `../../slides/` |
| `{{SOURCE_TYPES}}` | 소스 형태 | PDF · slides · papers · readings · 강의노트 |
| `{{UNIT}}` | per-source 단위(= `chapters/` 폴더가 담는 것) | `chapter` · `week` · `lecture` · `module` · `paper` |
| `{{KEEP_ENGLISH_TERMS}}` | 기술 용어 영어 원단어 유지 | `on` (수식/이공계 권장) / `off` |
| `{{MATH}}` | LaTeX 수식 모듈 | `on` (STEM) / `off` (인문·정책 등) |

> `{{UNIT}}` 이 `chapter` 가 아니면 `chapters/` 폴더를 그 이름(예 `weeks/`)으로 바꾸고, 아래 graph 색상 쿼리·lint 인자도 같이 바꾼다.

<!-- BOOTSTRAP:END -->

---

## 1. 3-Layer 구조 (불변 핵심)
1. **Sources (immutable)** — `{{SOURCE_TYPES}}` 원본(`{{SOURCE_DIRS}}`). **절대 수정하지 않는다.** 위키는 이 소스의 파생물이다.
2. **Wiki (이 폴더)** — 소스에서 생성한 상호링크 markdown.
3. **Schema (이 파일)** — 구조·규칙·워크플로우. LLM은 매 작업 전 이 파일을 따른다.

### 1.5 Source 자료 배치 (어디에 무엇을)
원자료는 전부 **immutable source** — vault **밖**, 보통 `<course>/sources/` 아래(= vault의 sibling)에 타입별로 둔다. vault에는 파생물(노트) + 임베드용 그림 **복사본**만 들어간다. 자료 타입마다 위키 페이지를 따로 만들지 말 것 — **한 chapter 페이지가 여러 소스를 종합**한다.

| 자료 | source 위치 | 위키에서의 역할 |
| --- | --- | --- |
| 주교재 (main text) | `sources/textbook/` | chapter 대표 `source:`, 정의·정리의 **authoritative 기준**(교차검증의 진실값) |
| 부교재·리딩 | `sources/readings/` | 보조 출처(다른 관점·증명); concept/topic에서 인용 |
| 강의자료 (slides) | `sources/slides/` | **단위(chapter) 구조의 기준** → `chapters/`와 1:1; 도식은 크롭→`attachments/` |
| 필기 (원본 스캔) | `sources/notes-raw/` | 이미지 `attachments/`로 복사 → `topics/`에 `![[..]]` 임베드 |
| 필기정리본 | `sources/notes-clean/` | **1차 ingest 콘텐츠**(가장 빠름) → 교재로 검증 |
| 과제·문제집 (hw) | `sources/hw/` | 연습 문제·풀이 → `topics/`(풀이 유형)·Query; 무엇을 연습할지 |
| 족보·기출 | `sources/exams/` | 콘텐츠 X, **강조점·평가 신호** → `summary/`·`topics/`·Query |

- **authority(충돌 시 우선)**: 강의자료 > 필기정리본 > 주교재 > 족보. (시험·평가가 강의 기준이라 강의자료가 최우선) 충돌은 `> ⚠️ conflict: …〔src1〕 vs …〔src2〕`로 표시 + `log.md` 등록 (contradiction-flagging ON일 때).
- **인용**: chapter frontmatter `source:`는 대표 1개(주교재 또는 slides), 본문은 `〔부교재 §x〕`·`〔필기 p.y〕`로 나머지.
- 폴더 골격은 harness `sources-skeleton/` (`bootstrap.sh -S <dir>`로 vault 옆에 생성). 이미 자료가 있으면 기존 폴더명을 그대로 써도 됨(예: `course_files_export/`).

## 2. 폴더 구성
- 루트(메타): `index.md`(카탈로그/홈 MOC), `log.md`(append-only), `CLAUDE.md`(이 파일), `Welcome.md`(→ index 리다이렉트).
- `chapters/` — **단위 페이지**(= source별 요약). 1 {{UNIT}} = 1 source = 1 page.
- `concepts/` — 단위 횡단 **개념 페이지**(여러 {{UNIT}}에서 재등장하는 핵심 아이디어 허브).
- `topics/` — 단일 주제 **심층 노트**(이미지·증명·예제 등). 해당 단위/개념 페이지에서 링크.
- `summary/` — synthesis(치트시트·체크리스트·종합).
- `attachments/` — 이미지/그림 자산. 노트는 `![[name.png]]`(basename) 임베드로 참조.

**링크 규칙**: Obsidian `[[링크]]`·`![[임베드]]`는 **basename**으로 해석 → 하위폴더로 옮겨도 유지된다. 따라서 **basename은 vault 내에서 고유**해야 한다(같은 이름의 chapter/concept 충돌 금지, alias 충돌도 금지).

## 3. 페이지 컨벤션
- **Frontmatter(YAML) 필수**:
  ```yaml
  ---
  tags: [{{COURSE}}, <topic>]
  aliases: ["<영문명>", "<별칭>"]
  type: chapter | concept | topic | synthesis | index | log | schema
  source: "{{SOURCE_DIRS}}<file>"   # chapter 페이지만 (대표 출처)
  updated: YYYY-MM-DD
  ---
  ```
- **상호링크**: 개념이 처음 등장하면 해당 `[[개념]]`으로 링크. 각 페이지 하단 `## 관련 노트` 에 **양방향** 링크(concept→chapter 와 chapter→concept 둘 다). 한쪽만 있으면 lint가 잡는다.
- **출처 인용**: 사실/공식 옆에 `〔<source> §x.y〕` 형식. chapter 페이지는 frontmatter `source` 로 대표 인용.
- **Open question (data gap)**: 원본이 불확실하거나 검증이 필요하면 `> ❓ **open question**: …` 콜아웃으로 명시하고 `log.md`·`index.md`에도 등록.
- **용어** (`{{KEEP_ENGLISH_TERMS}}=on` 일 때): 기술 용어는 **English 원단어** 그대로(번역 금지). 설명 연결문장만 본문 언어로.
- **수식** (`{{MATH}}=on` 일 때): LaTeX `$...$`(인라인) / `$$...$$`(블록)로 통일. KaTeX/MathJax 기준.

## 4. 워크플로우
- **Ingest** (새 소스 추가): 소스 통독 → `chapters/` 단위 페이지 작성 → `index.md` 갱신 → 관련 `concepts/` 갱신·생성 → 양방향 링크 → `log.md` 항목 추가. 한 소스가 10~15개 페이지를 건드릴 수 있다.
- **Query** (질문 응답): 관련 페이지 검색·종합 → **출처 인용**과 함께 답변. 재사용할 만한 답은 새 페이지로 적재해 누적시킨다.
- **Lint** (건강검진): 부록 A 체크리스트로 점검(끊긴 링크·orphan·back-link 비대칭·frontmatter 누락·페이지 없는 핵심 용어·open question). `scripts/lint.py` 사용.
- **Contradiction-flagging** (다중·이질 소스 충돌): 새 소스가 기존 주장과 **모순**되면 임의로 덮어쓰지 말고 두 출처를 함께 적고 `> ⚠️ **conflict**: A〔src1〕 vs B〔src2〕` 로 표시 → `log.md` 등록.
  - ON 권장: 논문·여러 저자·여러 학기 등 **소스가 이질적**인 수업(causality·policy 등).
  - OFF 가능: **단일 교재의 연속 단위**처럼 충돌이 구조적으로 없을 때(예: ODE는 OFF, 대신 손글씨 불확실 공식만 open question으로 추적).

## 5. log.md 형식
append-only. 항목 접두사: `## [YYYY-MM-DD] ingest|query|lint|refactor|conflict | <제목>`. 한 줄 요약 + 무엇을 바꿨는지.

---

## 부록 A — Lint 체크리스트
`python3 scripts/lint.py .` (또는 vault 경로). 점검 항목:
1. **broken wikilink / image embed** — `[[...]]`·`![[...]]` 타깃이 실제 파일/alias/attachments에 존재하는가. (코드스팬 `` `[[...]]` `` 은 예외)
2. **orphan** — inbound 링크 0인 페이지(랜딩 `Welcome` 제외). index에서 링크되게 한다.
3. **back-link 비대칭** — concept→chapter 링크는 있는데 chapter→concept 역링크가 없는 경우 → `## 관련 노트`에 보강.
4. **frontmatter 누락** — `type`·`updated`·`tags` 빠진 페이지.
5. **페이지 없는 핵심 용어** — 자주 언급되나 전용 페이지 없는 개념(필요하면 concept/topic 생성, 아니면 보류).
6. **open question / conflict** — 미해결 data gap·충돌 목록.

## 부록 B — Figure 크롭 레시피 (`{{MATH}}`/PDF 수업 옵션)
원본 PDF에서 참고 그림(다이어그램·plot·portrait)을 잘라 `attachments/`에 넣고 임베드. (`pdftoppm`·`magick`/ImageMagick 필요)
```bash
WD=/tmp/crop; mkdir -p "$WD"; cd "$WD"
# 1) 저해상도 썸네일 → 라벨 몽타주로 '그림 있는 페이지' 탐색
pdftoppm -png -r 50 "SOURCE.pdf" p
magick montage p-*.png -tile 6x -geometry 230x -pointsize 22 -label '%f' montage.png   # 읽어서 페이지 식별
# 2) 해당 페이지만 고해상도 렌더
pdftoppm -png -r 200 -f <N> -l <N> "SOURCE.pdf" hi
# 3) 영역 크롭 (WxH+X+Y) → 읽어서 좌표 보정
magick "hi-<N>.png" -crop 1620x900+50+40 +repage fig.png
# 4) vault로 복사 후 임베드:  attachments/fig.png  →  ![[fig.png|520]]  + 캡션 〔source p.N〕
```
> 손글씨 강의노트의 도식·증명은 원본 이미지를 그대로 `topics/`에 임베드(`![[orig.png]]`)하고, 교재 도식은 위 방법으로 크롭한다.

## 부록 C — Obsidian graph 색상 프리셋
`.obsidian/graph.json` 의 `colorGroups` (폴더별 색 분류, 우선순위 = 위에서부터). `template-vault/.obsidian/graph.json` 에 동일 프리셋이 들어 있다.
```json
"colorGroups": [
  { "query": "path:\"summary/\"",  "color": { "a": 1, "rgb": 16347926 } },
  { "query": "path:concepts/",     "color": { "a": 1, "rgb": 2278750  } },
  { "query": "path:chapters/",     "color": { "a": 1, "rgb": 3900150  } },
  { "query": "path:topics/",       "color": { "a": 1, "rgb": 11032055 } }
]
```
색은 `0xRRGGBB`의 10진수. 특정 노드만 강조하려면 맨 위에 `"query": "path:\"summary/Cheat Sheet\""` 같은 그룹을 추가. 변경 반영은 Obsidian `Cmd+P → Reload app without saving`.

---

## 부록 D — 이 패턴이 잘 맞는지 / 조정 (정직한 한계)
- **잘 맞음**: 소스가 고정·구조적이고(교재·강의), 누적적으로 한 학기 지식을 쌓을 때. LLM이 bookkeeping(요약·상호참조·lint)을 지치지 않고 해준다.
- **과할 수 있음**: 소스가 단 1~2개거나 일회성 정리면 위키 인프라(index/log/concept 분리)는 오버헤드 — 그냥 단일 문서가 낫다.
- **모순 플래그**는 이질 소스에서만 가치 있음(부록 4 참고). 단일 교재면 끄고 open question만 써라.

---

## 부록 E — 페이지 예시 & Ingest/Query worked example
페이지 스켈레톤은 `template-vault/_templates/`(chapter·concept·topic·cheatsheet)에 있다. 복사해 채운다. 최소 예시:

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
> source: 〔Lecture 1〕 · 종합: [[Cheat Sheet]] · 개념: [[Exchangeability]]
- RD $=\Pr(Y{=}1\mid A{=}1)-\Pr(Y{=}1\mid A{=}0)$ …
## 관련 노트
- 개념: [[Exchangeability]] · 다음: [[L2 - …]] · 목차: [[index]]
```
**concept** (`concepts/Exchangeability.md`) — chapter를 역으로 링크(양방향):
```markdown
---
type: concept
tags: [Causal-Inference, concept, exchangeability]
aliases: ["Exchangeability", "ignorability"]
updated: 2026-05-31
---
# Concept — Exchangeability
## 어디서 쓰이나
- [[L1 - Association vs Causation]]: association=causation 조건.
- [[L2 - …]]: randomization이 보장.
```

**Ingest (worked)**: 소스/정리노트 통독 → ① `chapters/L1` 작성 → ② `index.md` 의 chapters 섹션에 한 줄 추가 → ③ 새 개념 `Exchangeability`가 나왔으니 `concepts/Exchangeability` 생성하고 L1↔concept 양방향 링크 → ④ `summary/Cheat Sheet` 해당 항목 추가 → ⑤ `log.md` 에 `## [날짜] ingest | L1` 기록 → ⑥ `lint.py` 로 점검. (한 소스가 5~10개 페이지를 건드린다.)

**Query (worked)**: "exchangeability랑 positivity 차이?" → `concepts/Exchangeability`·`chapters/L2-2` 검색·종합 → **출처 인용**과 함께 답 → 자주 묻는 비교면 `concepts/Identification Conditions` 같은 새 페이지로 적재해 누적.
