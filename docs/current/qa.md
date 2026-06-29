# QA — Aquarium

## 현재 검증 상태

MVP vertical slice 기준 검증 완료:

- Backend contract/pipeline tests: 통과
- Backend API tests: 통과
- Frontend i18n test: 통과
- Frontend production build: 통과

실제 runner 통합 canary 기준:

- `scripts/run_real_integration_canary.sh`가 추가되었다.
- fake BettaFish/MiroFish contract runner로 canary PASS 경로를 검증한다.
- runner 미설정 상태는 `local_stub` degraded로 JSON summary를 출력하고 exit code `2`를 반환해야 한다.
- real PASS 조건은 BettaFish=`bettafish_cli completed`, MiroFish=`mirofish_cli completed` 둘 다 만족할 때뿐이다.

## Acceptance criteria

### Product flow

- 주제 입력 → research report → handoff manifest → seed → ontology/persona → simulation → report 순서가 한 run 안에서 완료되어야 한다.
- single mode는 하나의 universe를 생성해야 한다.
- multiverse mode는 3개 universe와 ensemble frequency caveat를 생성해야 한다.

### i18n

- UI copy는 한국어/중국어/영어를 모두 제공해야 한다.
- 보고서와 chat answer는 locale metadata를 따라야 한다.
- 중국어는 지원 언어 중 하나일 뿐 기본 source/tone처럼 보이면 안 된다.

### Fail-closed

- unsupported locale은 API validation error를 반환해야 한다.
- handoff manifest/report path는 명시적으로 저장되어야 한다.
- local_stub provider는 실제 provider가 아니라는 data gap을 남겨야 한다.

### Docker

- `docker compose config --quiet`가 통과해야 한다.
- `docker compose up --build` 후 UI/API가 응답해야 한다.
