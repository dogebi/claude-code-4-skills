# Claude Code 스킬 4가지 — 필드 노트

[짐코딩의 글](https://www.gymcoding.co/articles/claude-code-github-skills-website-ai-slop-design)(2026-11-24)을
바탕으로, AI 티 나는 홈페이지를 고치는 커뮤니티 Claude Code 스킬 4가지를 한 장으로 정리한
단일 HTML 페이지입니다.

- 라이브: https://dogebi.github.io/claude-code-4-skills/
- 산출물: `index.html` (약 48 KB, 의존성 0, 런타임 네트워크 요청 0)

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

- 비교 행 → SVG 작업 타임라인 → 스킬별 3단 레이아웃(마커·본문·명령) → 안전 수정 프롬프트
  → 배포 전 체크리스트 → 이 페이지에 적용한 변경 → FAQ
- 명령/프롬프트 블록마다 머리줄에 복사 버튼 (권한이 없으면 블록을 선택해 `Ctrl+C`)
- 배포 전 체크리스트 8항목 + 진행 막대, `localStorage`에 저장 (서버 전송 없음)
- 상단 읽기 진행 막대, 스크롤에 따른 목차 하이라이트
- 라이트/다크 테마 토글 — 첫 방문은 시스템 설정을 따르고, 선택은 `localStorage`에 저장
  (다이어그램·코드 블록도 CSS 변수로 함께 전환)
- 한국어 · 中文 · 日本語 — 상단 `KO / 中文 / 日本語` 전환. 첫 방문은 `navigator.language`,
  선택은 `localStorage`(`cc4.lang`). `<html lang>`도 `ko` / `zh-Hans` / `ja`로 함께 바뀌고,
  중국어·일본어는 `word-break: normal`로 줄바꿈 규칙을 바꿉니다(한국어는 `keep-all` 유지)
- 번역 원본은 `i18n/{ko,zh,ja}.json`, 빌드 스크립트가 `index.html`의
  `/*I18N_START*/ … /*I18N_END*/` 사이에 인라인합니다 — 배포본은 여전히 단일 파일·외부 요청 0
- 한국어 줄바꿈(`word-break: keep-all`)으로 단어 중간이 끊기지 않게 처리
- 본문 크기는 `--t-body`/`--t-dense`/`--t-label` 세 토큰으로만 지정, `prefers-reduced-motion`
  에서 부드러운 스크롤과 진행 막대 애니메이션을 끔
- 390px: 페이지 가로 스크롤 0, 다이어그램만 내부 가로 스크롤(920px 유지로 라벨 판독)
- 외부 요청 없음: 폰트·이미지·CDN 미사용, 링크만 원문과 각 저장소로 연결

## 수정

빌드 단계가 없습니다. `index.html`을 직접 고치고 다시 배포하면 됩니다.

```bash
python3 tools/deploy_pages.py --dry-run
python3 tools/deploy_pages.py
```

문구를 고칠 때는 `i18n/*.json`을 고친 뒤 인라인을 다시 만들어야 합니다
(키 집합·HTML 태그 수·빈 값·비한국어 로케일의 한글 잔여를 검사하고, 실패하면 쓰지 않습니다).

```bash
python3 tools/build_i18n.py
```

`tools/deploy_pages.py`는 `dogebi/dogebi.github.io`의 `master` 브랜치
`claude-code-4-skills/` 아래에 파일을 커밋합니다(Git Data API 사용, 허브 클론 없음).

## 출처와 라이선스

- 원문: 짐코딩, *Claude Code GitHub 스킬 4가지: AI 티 나는 홈페이지 디자인 고치기* (© 짐코딩)
- 이 페이지는 원문의 **요약·해설**이며 본문을 복제하지 않습니다. 설치 명령과 인용한
  프롬프트 예시만 기능 전달을 위해 포함했습니다.
- 페이지 코드: MIT. 각 스킬은 제작자 저장소의 라이선스를 따릅니다.
- 설치 명령과 버전은 작성 시점(2026-11-24) 기준이므로, 사용 전 각 저장소에서 확인하세요.
