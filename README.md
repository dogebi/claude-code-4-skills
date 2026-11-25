# Claude Code 스킬 4가지 — 필드 노트

[짐코딩의 글](https://www.gymcoding.co/articles/claude-code-github-skills-website-ai-slop-design)(2026-11-24)을
바탕으로, AI 티 나는 홈페이지를 고치는 커뮤니티 Claude Code 스킬 4가지를 한 장으로 정리한
단일 HTML 페이지입니다.

- 라이브: https://dogebi.github.io/claude-code-4-skills/
- 산출물: `index.html` (약 36 KB, 의존성 0, 런타임 네트워크 요청 0)

## 정리한 4가지

| 스킬 | 역할 | 설치 |
| --- | --- | --- |
| Unslop | 이미 만든 화면의 AI 디자인 패턴 진단 | `claude plugin install unslop --marketplace heydamir/unslop` |
| UI UX Pro Max | 업종·제품에 맞는 디자인 방향과 피할 패턴 | `npx ui-ux-pro-max-cli init --ai claude` |
| Diagram Design | 구조·흐름을 인라인 SVG HTML 한 장으로 | `/plugin install diagram-design@diagram-design` |
| Humanizer | AI 문장의 반복 패턴 교정 | `/plugin install humanizer@humanizer` |

각 카드에 실전 프롬프트(복사 버튼), 설치·업데이트 명령, 문서에 잘 안 적힌 한계
(운영 사이트 자동 수정 아님, 릴리스별 카탈로그 숫자 불일치, Google Fonts 요청,
AI 감지기 통과용이 아님 등)를 함께 적었습니다.

## 페이지 기능

- 스킬 비교표 · 사용 순서(6단계) · 스킬별 카드 · 안전한 수정 프롬프트 · FAQ
- 명령/프롬프트 블록마다 복사 버튼 (클립보드 권한이 없으면 블록을 선택해 `Ctrl+C`)
- 배포 전 체크리스트 8항목, `localStorage`에 저장 (서버 전송 없음)
- 스크롤에 따라 목차 하이라이트, 390px까지 가로 스크롤 없음
- 외부 요청 없음: 폰트·이미지·CDN 미사용, 링크만 원문과 각 저장소로 연결

## 수정

빌드 단계가 없습니다. `index.html`을 직접 고치고 다시 배포하면 됩니다.

```bash
python3 tools/deploy_pages.py --dry-run
python3 tools/deploy_pages.py
```

`tools/deploy_pages.py`는 `dogebi/dogebi.github.io`의 `master` 브랜치
`claude-code-4-skills/` 아래에 파일을 커밋합니다(Git Data API 사용, 허브 클론 없음).

## 출처와 라이선스

- 원문: 짐코딩, *Claude Code GitHub 스킬 4가지: AI 티 나는 홈페이지 디자인 고치기* (© 짐코딩)
- 이 페이지는 원문의 **요약·해설**이며 본문을 복제하지 않습니다. 설치 명령과 인용한
  프롬프트 예시만 기능 전달을 위해 포함했습니다.
- 페이지 코드: MIT. 각 스킬은 제작자 저장소의 라이선스를 따릅니다.
- 설치 명령과 버전은 작성 시점(2026-11-24) 기준이므로, 사용 전 각 저장소에서 확인하세요.
