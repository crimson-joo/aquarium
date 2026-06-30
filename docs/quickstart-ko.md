# Aquarium Quickstart

## 1. 환경 파일 준비

```bash
cp .env.example .env
```

## 2. Docker Compose 실행

```bash
docker compose up --build
```

## 3. 접속

- UI: http://localhost:3008
- API: http://localhost:8008/api/health

## 4. 로컬 개발 검증

```bash
cd backend
uv sync --group dev
uv run pytest -q

cd ../frontend
npm install
npm test
npm run build
```

## 5. 현재 MVP 주의사항

- 기본 provider는 `aquarium_native` standalone vertical slice입니다.
- BettaFish/MiroFish runner command는 기본 경로가 아니라 legacy bridge 검증이 필요할 때만 설정합니다.
- 실제 SearXNG/Graphiti/LLM 연결은 다음 adapter milestone입니다.
- simulation 결과는 실제 예측 확률이 아니라 입력 seed와 가정 기반 관찰입니다.
