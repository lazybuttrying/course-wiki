# Course-Wiki Harness 🎓📚

수업 자료(교재·슬라이드·논문·강의노트)를 **LLM이 유지하는 위키**로 정리하기 위한 범용 템플릿.
Andrej Karpathy의 [**LLM Wiki**](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 패턴을 따른다 — RAG처럼 매번 다시 찾는 대신, LLM이 **상호링크된 markdown 위키를 점진적으로 쌓고 유지**한다. ODE 수업용으로 검증한 구조를 수업 무관 템플릿으로 일반화한 것.

> A reusable, course-agnostic template for building an LLM-maintained course knowledge base (Obsidian vault). Subject-general by default, with optional math/figure modules.

## 무엇이 들어있나
| 파일/폴더 | 역할 |
| --- | --- |
| **`CLAUDE.template.md`** | ⭐ 핵심. self-contained 스키마 — 구조·컨벤션·워크플로우·레시피·예시 전부. 새 vault에 `CLAUDE.md`로. |
| **`bootstrap.sh`** | 한 명령으로 새 수업 vault 생성 + `{{placeholder}}` 치환 + 날짜 + `wiki.config.yml`. |
| `template-vault/` | 빈 vault 스켈레톤 (index·log·Welcome·폴더·graph 색상 프리셋). |
| `template-vault/_templates/` | **페이지 스켈레톤** (chapter·concept·topic·cheatsheet). 새 페이지 만들 때 복사. |
| `scripts/lint.py` | 위키 health-check (끊긴 링크·orphan·back-link 비대칭·frontmatter·용어). `--report`로 md 출력. |
| `scripts/crop-figures.md` | PDF 그림 크롭→임베드 레시피 (STEM/PDF 옵션). |
| `sources-skeleton/` | 원자료 폴더 골격 (textbook·readings·slides·notes-raw·notes-clean·hw·exams + 배치 가이드). `bootstrap.sh -S`로 vault 옆에 생성. |
| `wiki.config.example.yml` | 수업 설정 예시. |
| `.github/workflows/lint.yml` | CI — push/PR마다 lint + bootstrap 스모크 테스트. |

> 이 repo는 수업 콘텐츠와 **분리된 별도 디렉터리**다 (기본 위치 `~/Desktop/project/course-wiki-harness/`). 아래 명령은 repo 루트에서 실행한다. `HARNESS` 를 이 repo 경로로 둔다.

## 빠른 시작 (새 수업)
**자동 (권장)** — repo 루트에서 한 명령:
```bash
./bootstrap.sh -c "Causal Inference" \
               -v ../class/causality/wiki/Causality-wiki \
               -s "../../course_files_export/" \
               -u lecture -m on -e on
#  -c 수업명  -v vault경로  -s 소스경로  -u 단위(chapter|week|lecture|module|paper)
#  -m MATH(on|off)  -e English용어(on|off)  -t 소스타입(설명)
```
→ vault 생성 + placeholder 치환 + `CLAUDE.md` 생성 완료. 이제:
```bash
# LLM에게: "<vault>/CLAUDE.md 스키마대로 <소스>를 ingest 해줘"
python3 scripts/lint.py <vault>           # 점검
python3 scripts/lint.py <vault> --report lint.md   # md 리포트
```

**수동** (자동이 안 맞을 때): `template-vault/`를 복사 → `CLAUDE.template.md`를 `CLAUDE.md`로 → `{{PLACEHOLDER}}` 치환 → ingest.

> 새 **페이지**는 vault의 `_templates/`(chapter·concept·topic·cheatsheet)를 복사해 채운다.

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
이 repo는 이미 `git init` + 초기 커밋이 되어 있다(수업 콘텐츠와 분리된 독립 저장소). GitHub에 올리려면:
```bash
cd ~/Desktop/project/course-wiki-harness
gh repo create <you>/course-wiki-harness --public --source=. --push   # gh CLI
# 또는 수동: git remote add origin <url> && git push -u origin main
```
그 다음 GitHub repo **Settings → Template repository** 체크. 이후:
- 웹: **"Use this template"** → 새 수업 repo 생성.
- CLI: `gh repo create <Course>-wiki --template <you>/course-wiki-harness`

> push/template 토글은 본인 GitHub 권한이 필요해 자동화하지 않는다 — 위 명령만 실행하면 된다.

## 범위
- **일반 수업**: 소스 타입(PDF·슬라이드·논문·리딩)·단위(chapter/week/lecture/module) 선택 가능. causality·policy·eng 등.
- **수식/STEM**: `{{MATH}}=on` 으로 LaTeX 컨벤션 + figure 크롭 레시피 활성화.

## FAQ
- **꼭 Obsidian이어야 하나?** 아니다. 그냥 markdown 폴더다. `[[링크]]`·`![[임베드]]`·graph view는 Obsidian이 편할 뿐.
- **수식/그림 없는 인문·정책 수업도?** 된다. `-m off -e off`. `chapters/`는 `weeks/`나 `lectures/`로 의미상 읽으면 된다(폴더명 바꾸려면 graph 색상 쿼리·lint `--chapters` 인자도 같이).
- **소스 PDF를 꼭 읽어야?** 본인 정리노트가 있으면 그걸 1차 소스로 ingest하고 PDF로 교차검증하는 게 빠르다.
- **lint가 `_templates/`·HTML 주석을 안 잡나?** 둘 다 자동 제외한다.
- **언제 쓰지 말까?** 소스가 1~2개거나 일회성이면 위키 인프라가 과하다 — 단일 문서가 낫다. (`CLAUDE.template.md` 부록 D)

## 출처
- Pattern: Karpathy, *LLM Wiki* (gist).
- Reference implementation: `class/ode/wiki/ODE-wiki/` (이 템플릿이 추출된 실제 사례).
