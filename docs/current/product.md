# Product — Aquarium

## 한 줄 정의

아쿠아리움은 BettaFish의 로컬 조사/보고서를 MiroFish의 seed simulation으로 연결해, 사용자가 주제를 넣으면 가능한 미래 흐름을 단일/멀티버스 시뮬레이션으로 관찰하고 보고서/대화로 탐색하는 로컬 제품입니다.

## MVP 목표

1. 주제를 입력하면 research report가 생성된다.
2. report는 handoff manifest와 함께 seed document가 된다.
3. seed에서 ontology/persona가 추출된다.
4. 사용자는 single 또는 multiverse simulation을 선택한다.
5. simulation report와 chat answer가 생성된다.
6. UI와 보고서는 `ko`, `zh`, `en` locale을 따른다.
7. Docker Compose로 로컬에서 쉽게 실행된다.

## Non-goals

- 기존 BettaFish/MiroFish 전체 복사
- 장시간 대규모 OASIS simulation
- 실제 미래 예측 확률 주장
- SaaS multi-tenant/계정/결제
- Kubernetes/production cloud deploy

## 성공 순간

처음 쓰는 사용자가 `docker compose up --build` 후 브라우저에서 주제를 입력하고, 1분 내에 “조사 보고서 → 멀티버스 시뮬레이션 보고서”가 생성되는 것을 보는 순간입니다.
