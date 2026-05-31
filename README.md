# Course-Wiki Harness 🎓📚

수업 자료(교재·슬라이드·논문·강의노트)를 **LLM이 유지하는 위키**로 정리하기 위한 범용 템플릿.
Andrej Karpathy의 [**LLM Wiki**](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 패턴을 따른다 — RAG처럼 매번 다시 찾는 대신, LLM이 **상호링크된 markdown 위키를 점진적으로 쌓고 유지**한다. ODE 수업용으로 검증한 구조를 수업 무관 템플릿으로 일반화한 것.

> A reusable, course-agnostic template for building an LLM-maintained course knowledge base (Obsidian vault). Subject-general by default, with optional math/figure modules.

## 무엇이 들어있나
| 파일/폴더 | 역할 |
| --- | --- |
| **`CLAUDE.template.md`** | ⭐ 핵심. self-contained 스키마 — 구조·컨벤션·워크플로우·레시피 전부. 새 vault에 `CLAUDE.md`로 복사. |
| `template-vault/` | 빈 vault 스켈레톤 (index·log·Welcome·폴더·graph 색상 프리셋). 복사해서 바로 시작. |
| `scripts/lint.py` | 위키 health-check (끊긴 링크·orphan·back-link 비대칭·frontmatter·page 없는 용어). |
| `scripts/crop-figures.md` | PDF 그림 크롭→임베드 레시피 (STEM/PDF 옵션). |

## 빠른 시작 (새 수업)
```bash
# 1) 스켈레톤 복사
cp -R wiki-harness/template-vault  <course>/wiki/<Course>-wiki

# 2) 스키마를 vault의 CLAUDE.md로 (template-vault에 stub이 있으면 덮어씀)
cp wiki-harness/CLAUDE.template.md  <course>/wiki/<Course>-wiki/CLAUDE.md

# 3) <Course>-wiki/CLAUDE.md 안의 {{PLACEHOLDER}} 치환  (COURSE, VAULT, SOURCE_DIRS, UNIT, MATH ...)

# 4) LLM에게: "이 CLAUDE.md 스키마대로 <소스>를 ingest 해줘"
```
그 다음부터 LLM이 **Ingest / Query / Lint** 워크플로우로 위키를 키운다. 자세한 규칙은 `CLAUDE.template.md` 본문 참조.

## 폴더 구조 (생성되는 vault)
```
<Course>-wiki/
├── index.md · log.md · Welcome.md · CLAUDE.md   # 메타
├── chapters/      # 단위(=chapter/week/lecture/paper) 페이지
├── concepts/      # 단위 횡단 개념 허브
├── topics/        # 단일 주제 심층 노트(이미지 포함)
├── summary/       # 치트시트·체크리스트
├── attachments/   # 그림 자산
└── .obsidian/     # graph 색상 프리셋 등
```

## GitHub template으로 관리하기
이 폴더(`wiki-harness/`)를 그대로 GitHub template repo로 쓸 수 있다.
```bash
cd wiki-harness
git init && git add -A && git commit -m "Course-wiki harness v1"
gh repo create <you>/course-wiki-harness --public --source=. --push   # gh CLI 사용 시
```
그 다음 GitHub repo **Settings → Template repository** 체크. 이후:
- 웹: **"Use this template"** → 새 수업 repo 생성.
- CLI: `gh repo create <Course>-wiki --template <you>/course-wiki-harness`

> push/template 토글은 본인 GitHub 권한이 필요해 자동화하지 않는다 — 위 명령만 실행하면 된다.

## 범위
- **일반 수업**: 소스 타입(PDF·슬라이드·논문·리딩)·단위(chapter/week/lecture/module) 선택 가능. causality·policy·eng 등.
- **수식/STEM**: `{{MATH}}=on` 으로 LaTeX 컨벤션 + figure 크롭 레시피 활성화.

## 출처
- Pattern: Karpathy, *LLM Wiki* (gist).
- Reference implementation: `class/ode/wiki/ODE-wiki/` (이 템플릿이 추출된 실제 사례).
