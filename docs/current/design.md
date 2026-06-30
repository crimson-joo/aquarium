# 아쿠아리움 Design Slice

## 1. 제품/브랜드 방향

**프로젝트명:** 아쿠아리움(Aquarium)

**한 줄 정의:**
주제와 시드 문서를 하나의 `수조`에 넣으면, Aquarium 자체 엔진이 현실의 단서를 seed로 정리하고 생태계 지도(Ontology/Persona)를 만든 뒤 여러 `해류`와 `물고기`의 상호작용으로 가능한 미래의 `멀티버스`를 탐색하여, 언어에 맞는 관찰 보고서와 대화형 세계를 돌려주는 standalone 시뮬레이션 워크스페이스.

**디자인 원칙:**
- **단계형은 유지, 형태는 재해석:** 기존 sibling product의 검증된 흐름은 참고하되, 화면 copy는 `수조 준비 → 생태계 조성 → 해류 가동 → 멀티버스 관찰 → 리포트/대화`라는 Aquarium 고유 은유를 기본값으로 둔다.
- **중국어 원본 톤 탈피:** 기본 경험은 한국어 중심의 세련된 SaaS 톤. 중국어는 선택 언어 중 하나일 뿐이며, 기본 copy/source-of-truth가 중국어처럼 보이면 안 된다.
- **전문성과 감성의 균형:** “미래 예측”을 과장하지 않고 “가능성 탐색/시뮬레이션/의사결정 보조”로 표현한다. 감성 키워드는 수조, 해류, 관찰, 군집, 분기, 심해, 빛, 파동.
- **보고서 언어 일관성:** UI 언어 선택이 화면 copy뿐 아니라 분석 요청 기본 언어, 중간 상태 메시지, 최종 보고서 생성 언어에 그대로 반영되어야 한다.

---

## 2. 정보 구조 및 핵심 UX 플로우

### 2.1 권장 전역 구조

- **Top nav**
  - 좌측: Aquarium 로고/워드마크
  - 중앙 또는 좌측 하단: 현재 프로젝트/수조 이름
  - 우측: 언어 선택 `한국어 / 中文 / English`, 히스토리, 설정, GitHub/문서 링크
- **Primary workspace**
  - 좌측: 단계형 “해류 지도(Current Map)”
  - 중앙: 현재 단계 작업 영역
  - 우측: 수조 상태 패널(파일, 엔티티, 에이전트 수, 진행률, 비용/라운드 추정)
- **Bottom or floating rail**
  - 다음 액션 CTA, 로그 열기, 중단/재시도, 결과 보기

### 2.2 신규 사용자용 5단계 플로우

1. **수조 열기 — Seed Intake**
   - 파일 업로드: PDF/MD/TXT/CSV/URL/BettaFish report
   - 자연어 질문 입력: “무엇을 알고 싶은가요?”
   - 언어 선택 확인: “이 수조의 UI와 보고서는 한국어로 생성됩니다.”
   - 주요 CTA: `수조 준비하기`

2. **생태계 스캔 — Context Mapping**
   - 문서에서 사건, 인물, 조직, 시간축, 주장/감정, 불확실성을 추출
   - 시각화: 유기적인 노드 네트워크가 수조 안에서 떠다니는 형태
   - 사용자 검토: 핵심 엔티티 수정/제외, 시뮬레이션 범위 지정
   - CTA: `생태계 확정`

3. **해류 설계 — Scenario & Variable Setup**
   - single/multiverse 선택
     - Single current: 하나의 기준 시나리오를 깊게 탐색
     - Multiverse currents: 여러 변수 조합을 병렬 탐색
   - 변수 주입: 정책 변화, 여론 이벤트, 가격 변화, 캐릭터 선택 등
   - 라운드/에이전트 수/온도/비용 프리셋
   - CTA: `해류 가동하기`

4. **멀티버스 관찰 — Simulation Run**
   - 실시간 진행: 라운드, 이벤트, 에이전트 상호작용, 분기점
   - 시각화: 여러 해류가 갈라지는 타임라인/스트림 뷰
   - 상태 메시지: “12번째 라운드에서 새로운 분기가 감지되었습니다.”
   - 안전 액션: 일시정지, 변수 추가, 중단 후 리포트 생성
   - CTA: `결과 해석하기`

5. **리포트와 대화 — Report & Deep Interaction**
   - 보고서: 요약, 핵심 시나리오, 분기별 근거, 리스크, 추천 액션
   - 인터랙션: ReportAgent와 대화, 특정 물고기/에이전트와 대화, 근거 문서로 드릴다운
   - 내보내기: PDF/Markdown/JSON, 언어별 재생성
   - CTA: `보고서 저장`, `새 수조 만들기`

---

## 3. 주요 화면 제안

### 3.1 Home / Landing

**목적:** “무엇을 하는 제품인지”와 “바로 시작”을 10초 안에 이해.

**구성:**
- Hero title: `미래를 예측하지 말고, 여러 가능성을 수조에 띄워보세요.`
- Subtitle: `시드 문서와 질문을 넣으면 아쿠아리움이 현실의 단서를 해류로 바꾸고, 가능한 미래를 단계적으로 시뮬레이션합니다.`
- Primary CTA: `새 수조 만들기`
- Secondary CTA: `샘플 수조 둘러보기`
- Visual: 어두운 딥블루 배경 위 반투명 유리 수조, 얇은 네온 해류, 작은 점/물고기 에이전트가 군집 이동
- Trust note: `Aquarium 자체 엔진으로 실행되며, 외부 runner 연결 여부는 실행 근거에 별도 표시됩니다.`

### 3.2 New Aquarium / Seed Intake

**상태:**
- Empty: 드래그 앤 드롭 영역 + 예시 질문
- File selected: 파일 칩, 파싱 예상, 삭제 버튼
- Parsing: 잔잔한 물결 skeleton
- Error: 파일 형식/용량/언어 불일치 안내

**핵심 copy:**
- `시드 문서를 넣어 수조의 물을 채우세요.`
- Placeholder: `예: 이 이슈가 앞으로 2주 동안 어떤 여론 흐름으로 번질지 시뮬레이션해줘.`
- Language confirmation: `보고서 언어: 한국어`

### 3.3 Current Map / Stepper

**차별화 방향:** MiroFish의 직선형 numbered workflow 대신, 좌측에 수직 “해류 지도”를 제공한다.

- Step item states:
  - 대기: 흐린 점 + `아직 물이 차오르지 않았어요`
  - 진행: 파동 애니메이션 + 현재 작업명
  - 완료: 빛나는 물방울 체크
  - 경고: 산호색 알림 점
- 각 단계는 접을 수 있으며, 완료 후 요약을 보여준다.

### 3.4 Context Mapping

**구성:**
- 중앙: 관계 그래프/타임라인 전환 탭
- 우측: 추출된 엔티티 리스트
- 하단: `수정 제안`, `제외`, `핵심 변수로 고정`

**UX 기준:**
- 자동 추출 결과를 맹신하게 만들지 말고 “검토 가능한 draft”로 표현
- 복잡한 GraphRAG 용어는 내부/고급 모드에서만 노출

### 3.5 Scenario Setup

**구성:**
- Simulation mode cards:
  - `단일 해류` — 빠르고 명확한 기준 전망
  - `멀티버스 해류` — 변수별 분기와 가능성 비교
- Variable chips:
  - `정책 발표`, `가격 인상`, `인플루언서 반응`, `주요 인물 이탈`
- Presets:
  - `빠른 관찰`, `균형`, `심층 탐사`

**톤:** “예측 엔진 시작”보다 “해류를 설계한다”는 느낌. 단, 버튼은 명확해야 한다.

### 3.6 Simulation Run

**구성:**
- Header: 현재 라운드, 남은 예상 시간, 활성 해류 수
- Main visual:
  - Single: 하나의 굵은 luminous stream
  - Multiverse: 여러 stream이 갈라지고 합쳐지는 지도
- Event feed:
  - `분기 감지`, `군집 이동`, `기억 업데이트`, `새 충돌 발생`
- Controls:
  - `일시정지`, `변수 추가`, `로그 보기`, `중단 후 리포트 생성`

### 3.7 Report

**구성:**
- Executive summary card
- Scenario comparison cards
- Evidence drawer: 원문 근거/추론 단계
- Risk radar: 가능성, 영향도, 신뢰도
- Action recommendations
- Export controls

**보고서 언어:** UI 언어와 동일하게 기본 생성. 사용자가 변경하면 화면에 명확히 표시:
`현재 보고서는 English로 다시 생성됩니다. UI 언어도 함께 변경할까요?`

### 3.8 Deep Interaction

**구성:**
- 좌측: ReportAgent / 에이전트 물고기 리스트
- 중앙: 대화
- 우측: 선택된 에이전트의 기억, 성향, 관련 이벤트

**Copy:**
- `이 물고기에게 왜 그렇게 움직였는지 물어보세요.`
- `ReportAgent에게 근거를 더 자세히 요청할 수 있습니다.`

---

## 4. i18n Copy / Tone 기준

### 4.1 언어 정책

- 지원 언어: `ko`, `zh`, `en`
- 기본 언어는 브라우저 언어가 한국어면 `ko`, 그 외는 첫 진입에서 선택 모달. 중국어를 fallback/source처럼 보이게 하지 않는다.
- `locale`은 UI뿐 아니라 API 요청 payload에 포함한다.
  - 예: `{ uiLocale: 'ko', reportLocale: 'ko', userPromptLocale: 'ko' }`
- 보고서 생성 Agent prompt에도 명시:
  - `Generate all headings, summaries, evidence notes, and recommendations in Korean unless user explicitly changes report language.`
- 번역 키는 단계 은유와 기능 명칭을 분리한다.
  - 좋은 예: `step.seed.title`, `simulation.mode.single.label`
  - 나쁜 예: `home.step01Title`에 기능/문학 표현 혼재

### 4.2 한국어 톤

- **톤:** 차분한 전문가 + 친절한 안내자
- **문장 길이:** CTA는 짧게, 설명은 1문장 40자 내외 권장
- **피해야 할 표현:** “무조건 예측”, “정답”, “신탁”, “절대적 미래”
- **권장 표현:** “가능성”, “흐름”, “분기”, “근거”, “관찰”, “시뮬레이션”

### 4.3 핵심 copy 샘플

- Home title: `가능한 미래를 하나의 수조에서 관찰하세요`
- Home subtitle: `문서와 질문을 넣으면, 아쿠아리움이 현실의 단서를 해류로 바꾸고 여러 시나리오를 단계적으로 시뮬레이션합니다.`
- Upload title: `시드 문서를 넣어주세요`
- Prompt placeholder: `무엇을 알고 싶나요? 예: 이 사건이 다음 달 여론에 어떤 영향을 줄지 비교해줘.`
- Start CTA: `수조 준비하기`
- Confirm context CTA: `생태계 확정`
- Run CTA: `해류 가동하기`
- Report CTA: `리포트 생성`
- Empty history: `아직 만든 수조가 없습니다. 첫 번째 시뮬레이션을 시작해보세요.`
- Error generic: `수조를 준비하는 중 문제가 생겼습니다. 입력을 확인한 뒤 다시 시도해주세요.`
- Loading: `문서 속 단서를 수면 위로 끌어올리는 중입니다.`
- Complete: `해류 관찰이 끝났습니다. 이제 결과를 해석할 수 있어요.`

### 4.4 중국어/영어 톤 방향

- 중국어: 과장된 홍보식 문구를 피하고 기능 중심으로 정돈. `预测万物` 같은 표현 대신 `探索多种可能路径` 계열 사용.
- 영어: B2B SaaS tone. “Predict anything”보다 “Explore possible futures from source evidence.”
- 세 언어 모두 은유는 유지하되, 버튼/오류/설정은 기능적으로 번역한다.

---

## 5. Visual Design 기준

### 5.1 색상 토큰 제안

- `bg.deep`: `#06131D` — 메인 배경, 심해색
- `bg.panel`: `#0B1F2A` — 카드/패널
- `bg.glass`: `rgba(16, 42, 56, 0.72)` — 유리 수조 패널
- `primary.aqua`: `#35D4C7` — 주요 CTA/활성 해류
- `primary.blue`: `#4DA3FF` — 링크/정보 상태
- `accent.coral`: `#FF7A6B` — 경고/중요 이벤트
- `accent.plankton`: `#B9F56A` — 성공/완료
- `text.primary`: `#F4FBFF`
- `text.secondary`: `#A7BECA`
- `text.muted`: `#6F8793`
- `border.soft`: `rgba(167, 190, 202, 0.18)`

**사용 원칙:**
- 배경은 어둡게, 데이터/액션은 밝게. “화려한 그라데이션”보다 얇은 빛과 투명도를 활용.
- Coral은 오류와 경고에만 제한해 프리미엄 톤 유지.
- 라이트 모드는 추후 지원 가능하되 MVP는 다크 우선 권장.

### 5.2 타이포그래피

- Korean/UI: `Pretendard Variable` 우선, fallback `Inter`, `Noto Sans KR`, system sans-serif
- English/number: `Inter` 또는 `Geist`
- Monospace/log: `JetBrains Mono`

**스케일:**
- Hero: 56–72px / 700 / -0.03em
- Page title: 32–40px / 700
- Section title: 20–24px / 650
- Body: 15–16px / 400–500
- Caption/meta: 12–13px / 500
- Button: 14–15px / 650

**한국어 기준:** 자간을 과하게 줄이지 말고, line-height 1.45 이상 유지.

### 5.3 레이아웃/모션

- Grid: 12-column, max width 1280–1440px
- Radius: card 20–28px, button 14–16px, chip 999px
- Shadow: 짙은 그림자 대신 inner glow/blur 사용
- Motion:
  - 물결 shimmer: 1.8–2.4s, low opacity
  - 단계 전환: 180–260ms ease-out
  - 그래프/해류 애니메이션은 `prefers-reduced-motion` 준수

---

## 6. Component 기준

### 6.1 Core components

- **AquaButton**
  - variants: `primary`, `secondary`, `ghost`, `danger`
  - states: default, hover, active, disabled, loading
  - primary label은 동사형: `시작하기`, `확정하기`, `생성하기`

- **GlassCard**
  - translucent background + soft border
  - header/title/body/actions 슬롯
  - 복잡한 정보는 접기/펼치기 지원

- **CurrentStepper**
  - 단계명, 상태, 진행률, 요약, 재실행 액션
  - 숫자는 보조 정보로만 사용하고 은유형 아이콘/상태를 우선

- **SeedUploader**
  - drag/drop, file chips, parsing progress, error hint
  - BettaFish report 감지 시 `BettaFish 보고서로 인식했습니다.` 표시

- **LocaleSwitcher**
  - labels: `한국어`, `中文`, `English`
  - 언어 변경 시 UI/보고서 언어 분리 여부를 명확히 묻는다.

- **ScenarioModeCard**
  - single/multiverse 차이를 비전문가도 이해하도록 설명
  - 예상 시간/비용/추천 상황 표기

- **SimulationStreamView**
  - 라운드/분기/에이전트 이벤트를 스트림으로 표현
  - 멀티버스 모드에서는 stream 비교와 focus 선택 지원

- **ReportCard / EvidenceDrawer**
  - 결론과 근거 분리
  - 근거 원문, 추론, 신뢰도 표시

### 6.2 상태 설계

- Empty: “무엇을 하면 되는지”가 명확한 안내 + 예시
- Loading: 현재 수행 중인 내부 작업을 쉬운 언어로 표시
- Partial success: “일부 문서는 처리되지 않았지만 계속 진행 가능” 제공
- Error: 원인/해결/재시도 버튼 포함
- Complete: 다음 단계 CTA를 한 개만 강조
- Long-running: 진행 로그와 중단 옵션을 항상 제공

---

## 7. 접근성/신뢰 기준

- 모든 주요 색상 조합 WCAG AA 대비 확보
- 해류/물고기 애니메이션에 의미를 의존하지 말고 텍스트 상태 병기
- 키보드로 업로드, 단계 이동, 보고서 export 가능
- 결과 화면에 `시뮬레이션 결과는 의사결정 보조 자료이며 확정적 예측이 아닙니다.` 고지
- 비용/시간이 큰 작업 전에는 예상 라운드/에이전트 수/비용 범위를 보여준다.

---

## 8. MiroFish에서 차용/회피할 것

**차용:**
- 초보자도 따라갈 수 있는 단계형 구조
- seed 문서 기반 시작
- single/multiverse simulation 개념
- 보고서 생성 후 deep interaction 제공

**회피:**
- 중국어가 기본처럼 보이는 i18n 구조/fallback
- “Graph Building → Environment Setup → Simulation” 같은 엔지니어링 용어를 전면에 노출
- 동일한 5-step 숫자 리스트와 콘솔 스타일 그대로 복제
- 과장된 “만물 예측” 톤
- 원본 로고/색상/스크린 구성의 직접 복제

---

## 9. MVP 우선순위

1. 한국어 기본 UX와 i18n payload/report locale 연결
2. Seed uploader + prompt + 언어 확인
3. CurrentStepper 기반 5단계 진행
4. Single/Multiverse mode selection
5. Simulation progress stream + resumable 상태
6. 한국어 보고서 템플릿 + Evidence drawer
7. History/previous aquariums

---

## 10. 구현팀 전달 메모

- 이 문서는 `docs/current/design.md`에 그대로 옮겨도 되는 handoff 초안이다.
- 실제 구현 시 기존 MiroFish 컴포넌트를 참조하더라도 이름/카피/레이아웃/색상은 Aquarium 디자인 토큰과 은유 체계로 교체한다.
- i18n은 처음부터 `ko`, `zh`, `en` 3개 locale을 동일한 key 구조로 유지하고, 보고서 생성 API에 `reportLocale`을 필수로 전달한다.
