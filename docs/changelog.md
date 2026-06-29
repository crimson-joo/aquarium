# Changelog — Aquarium

## 2026-06-29 — Real runner release

- Merged Aquarium release PR #1 to `main`.
- Merged BettaFish-localized release PR #16 to `main` for Aquarium BettaFish runner support.
- Merged MiroFish-localized release PR #48 to `main` for Aquarium MiroFish runner support.
- Synced `develop` branches back from `main` after release.
- Verified Aquarium and MiroFish GitHub Actions success; BettaFish had no remote checks configured/reported, with local focused runner tests passing before merge.
- Captured release QA caveat: live native Graphiti/OASIS execution remains separate from contract-level runner proof.
- Reconciled current docs so the real integration path now points at sibling repo runner commands instead of stale feature-worktree examples.

## 2026-06-29 — Real runner canary and state visibility

- Added `scripts/run_real_integration_canary.sh` so local integration canaries fail unless both BettaFish and MiroFish stages are real completed runners.
- Added fake-runner contract tests for canary PASS and local_stub degraded paths.
- Passed runner warnings from BettaFish/MiroFish payloads into Aquarium stage warnings so UI/API can expose partial/native/degraded state honestly.
- Validated runner provider labels at the adapter boundary so `local_stub` or malformed runner output cannot be counted as real integration.
- Restricted runner subprocess environment by default and added explicit `AQUARIUM_RUNNER_ENV_ALLOWLIST` for intentional extra env forwarding.
- Added `.env.example` sibling runner command examples and Docker Compose adapter env passthrough.
- Polished frontend provider/status/warning/artifact copy across Korean, Chinese, and English.

## 2026-06-29 — Initial MVP scaffold

- Created Aquarium project under `/Users/crimson/Projects/aquarium`.
- Added FastAPI backend with deterministic research→seed→ontology→simulation→report pipeline.
- Added Vite React frontend with aquarium-themed multilingual UI.
- Added Docker Compose local runtime with backend, frontend, and PostgreSQL.
- Added current product/design/architecture/QA/release docs.
- Added handoff manifest v1 documentation.
- Added external CLI adapter contract for real BettaFish report generation and MiroFish simulation ingestion.
- Added run stage/provider/status/warning visibility in API and UI so `local_stub` is explicit rather than hidden.
- Added concrete execution plan for moving from stub MVP to real BettaFish→MiroFish integration.
