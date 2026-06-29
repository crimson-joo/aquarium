# Release — Aquarium

## 현재 release 수준

초기 MVP scaffold입니다. Public production release가 아니라, Docker Compose로 실행 가능한 local demo/research simulator 기준입니다.

## Local release gate

```bash
cd backend && uv run pytest -q
cd ../frontend && npm test && npm run build
cd .. && docker compose config --quiet
```

## Docker endpoints

- Frontend: `http://localhost:3008`
- Backend: `http://localhost:8008`
- Health: `http://localhost:8008/api/health`

## Release caveat

현재 provider는 `local_stub`입니다. 실제 BettaFish/SearXNG/Graphiti provider adapter가 연결되기 전에는 “제품 흐름 검증용 vertical slice”로 표기해야 합니다.
