# Changelog

본 repo는 [Keep a Changelog](https://keepachangelog.com/) 형식을 느슨하게 따른다.

## [1.1.0] — 2026-05-31
### Added
- **페이지 템플릿** `template-vault/_templates/`: chapter · concept · topic · cheatsheet 스켈레톤 (frontmatter + 섹션 구조). 새 페이지를 만들 때 복사해 채운다.
- **부트스트랩 자동화** `bootstrap.sh`: 한 명령으로 새 수업 vault 생성 + `{{placeholder}}` 치환 + 날짜 스탬프 + `wiki.config.yml` 기록.
- `wiki.config.example.yml`: 수업 설정 예시.
- **`sources-skeleton/`**: 원자료 폴더 골격(textbook·readings·slides·notes-raw·notes-clean·hw·exams + 배치 가이드 README). `bootstrap.sh -S <dir>`로 vault 옆에 생성.
- `CLAUDE.template.md` §1.5 **Source 자료 배치**: 주교재/부교재/강의자료/필기/필기정리본/hw/족보 → 위키 역할 매핑 + authority(충돌 우선순위)·인용 규칙.
- **CI** `.github/workflows/lint.yml`: push/PR 시 lint 실행 + `bootstrap.sh` 스모크 테스트 + lint 리포트 아티팩트.
- `LICENSE` (MIT), `CHANGELOG.md`.
- `scripts/lint.py`: `--report <md>` 출력 모드, `_templates/` 자동 제외, check 6 false-positive 완화.
- `CLAUDE.template.md`: BOOTSTRAP 블록 구분자(`<!-- BOOTSTRAP:START/END -->`), 인라인 페이지 예시, Ingest/Query worked example.

### Changed
- repo를 수업 콘텐츠(`class/`)와 분리된 독립 디렉터리로 이동. README를 standalone 사용 기준으로 갱신.

## [1.0.0] — 2026-05-30
### Added
- 최초 버전: `CLAUDE.template.md`(self-contained 스키마), `template-vault/`(빈 vault 스켈레톤 + graph 색상 프리셋), `scripts/lint.py`, `scripts/crop-figures.md`, `README.md`, `.gitignore`.
- `class/ode/wiki/ODE-wiki/`에서 추출한 범용 LLM-Wiki 템플릿.
