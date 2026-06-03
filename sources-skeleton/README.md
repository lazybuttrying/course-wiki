# sources/ — 원자료 (immutable)

수업 원자료를 타입별로 둔다. **위키 밖**(= vault의 sibling, 보통 `<course>/sources/`)에 두고 **절대 수정하지 않는다.** 위키(`wiki/<Course>-wiki/`)는 이걸 종합한 파생물이다.

```
<course>/
├── sources/            ← 여기 (immutable)
│   ├── textbook/        주교재
│   ├── readings/        부교재·보조 리딩
│   ├── slides/          강의자료(슬라이드)
│   ├── transcripts/     강의 속기록(발화 일차기록)
│   ├── notes-raw/       필기자료(원본 스캔·사진)
│   ├── notes-clean/     필기정리본(본인 정리)
│   ├── hw/              과제·문제집
│   └── exams/           족보·기출
└── wiki/<Course>-wiki/ ← LLM 위키 (파생물)
```

## 자료 → 위키 매핑
| 자료 | 폴더 | 위키에서의 역할 |
| --- | --- | --- |
| 주교재 | `textbook/` | chapter 대표 `source:`, 정의·정리의 **authoritative 기준** |
| 부교재·리딩 | `readings/` | 보조 출처(다른 관점·증명), concept/topic 인용 |
| 강의자료(슬라이드) | `slides/` | **단위 구조의 기준** → `chapters/`와 1:1; 도식은 크롭→`attachments/` |
| 강의 속기록 | `transcripts/` | **발화 일차기록** — 슬라이드가 빠뜨린 설명·강조·예시; 강조점→`summary/`, 교수 예시→`topics/` |
| 필기(원본 스캔) | `notes-raw/` | 이미지 `attachments/`로 복사 → `topics/` 임베드 |
| 필기정리본 | `notes-clean/` | **1차 ingest 콘텐츠**(가장 빠름) → 교재로 검증 |
| 과제·문제집 | `hw/` | 연습 문제·풀이 → `topics/`(풀이 유형)·Query |
| 족보·기출 | `exams/` | 콘텐츠 X, **강조점·평가 신호** → `summary/`·`topics/`·Query |

## 규칙
1. **immutable**: 원본은 손대지 않는다. 위키엔 파생 노트 + 임베드용 그림 복사본만.
2. **authority(충돌 시)**: 강의자료(slides·transcript) > 필기정리본 > 주교재 > 족보. (시험이 강의 기준이라 강의자료 최우선) 충돌은 위키에서 `> ⚠️ conflict: …` + log 등록.
3. **인용**: chapter `source:`는 대표 1개, 본문은 `〔부교재 §x〕`·`〔필기 p.y〕`로.
4. 이미 자료가 다른 폴더명으로 있으면(예: `course_files_export/`) 그대로 쓰고, vault `CLAUDE.md`의 `SOURCE_DIRS`만 맞춰라.

> 빈 폴더 유지를 위해 각 폴더에 `.gitkeep`. 실제 파일을 넣으면 지워도 된다.
