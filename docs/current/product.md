# Product — Aquarium

## 한 줄 정의

아쿠아리움은 사용자가 주제를 넣으면 Aquarium 자체 엔진이 조사 seed, 생태계 지도(Ontology/Persona), 단일/멀티버스 해류 시뮬레이션, 관찰 리포트와 대화를 생성하는 standalone local runtime입니다. BettaFish/MiroFish 호출기는 기본 제품 경로가 아니라 legacy migration bridge입니다.

## MVP 목표

1. 주제를 입력하면 Aquarium native research seed가 생성된다.
2. seed는 handoff manifest와 함께 실행 artifact로 고정된다.
3. seed에서 ontology/persona 생태계가 추출된다.
4. 사용자는 single 또는 multiverse simulation을 선택한다.
5. simulation report와 chat answer가 생성된다.
6. UI와 보고서는 `ko`, `zh`, `en` locale을 따른다.
7. Docker Compose로 로컬에서 쉽게 실행된다.

## Non-goals

- BettaFish/MiroFish repo를 runtime dependency로 유지하는 제품화
- 기존 BettaFish/MiroFish 전체 복사
- 장시간 대규모 OASIS simulation
- 실제 미래 예측 확률 주장
- SaaS multi-tenant/계정/결제
- Kubernetes/production cloud deploy

## 성공 순간

처음 쓰는 사용자가 `docker compose up --build` 후 브라우저에서 주제를 입력하고, 별도 sibling repo 설정 없이 1분 내에 “Aquarium native seed → 생태계 지도 → 멀티버스 시뮬레이션 보고서”가 생성되는 것을 보는 순간입니다.

## Product positioning

- **Primary path:** `aquarium_native` standalone runtime.
- **Legacy bridge:** `bettafish_cli` / `mirofish_cli`는 migration, regression, sibling-runtime evidence 검증용.
- **Evidence language:** UI/API는 standalone native, external runner dependency, degraded/failure를 분리한다.
