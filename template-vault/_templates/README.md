# _templates/ — 페이지 스켈레톤

새 페이지를 만들 때 여기서 복사해 채운다. `{{...}}` 토큰을 실제 값으로 바꾸고, 파일을 해당 폴더로 옮긴다.

| 템플릿 | → 폴더 | 용도 |
| --- | --- | --- |
| `chapter.md` | `chapters/` | 단위(lecture/chapter/week)별 요약 |
| `concept.md` | `concepts/` | 단위 횡단 개념 허브 |
| `topic.md` | `topics/` | 단일 주제 심층(증명·예제·그림) |
| `cheatsheet.md` | `summary/` | 시험/복습 종합 |

## 규칙 (요약)
- **basename 고유**: chapter/concept/topic 이름이 겹치면 안 됨. alias 충돌도 금지.
- **양방향 링크**: concept↔chapter 는 서로 `## 관련 노트`에서 링크 (lint가 비대칭을 잡음).
- **frontmatter 필수**: `type`·`tags`·`updated` (chapter는 `source`도).
- 자세한 규약은 vault 루트의 `CLAUDE.md`.

> 이 폴더는 `_` 접두로 `lint.py`와 일반 검색에서 제외된다. Obsidian core **Templates** 플러그인의 template 폴더로 지정하면 단축키로 삽입할 수 있다.
