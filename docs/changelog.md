# Changelog — Aquarium

## 2026-06-30 — Standalone Aquarium native pivot

- Promoted the default no-runner path from `local_stub` degraded output to `aquarium_native` standalone vertical slice.
- Added API `runtime_claim` fields for `standalone_native` and `external_runner_dependency` so UI can distinguish Aquarium-native execution from legacy sibling-runner integration.
- Updated UI copy to present Aquarium as a standalone research × ecosystem × simulation runtime, not a BettaFish/MiroFish bridge.
- Updated product, design, architecture, QA, release, and README docs so BettaFish/MiroFish runner commands are described as legacy bridge/migration evidence rather than the primary product path.
- Verified backend tests, frontend i18n tests, and frontend production build after the pivot.

## 2026-06-30 — Runtime evidence labeling and multiverse expansion

- Added API/UI `runtime_claim` labeling so Aquarium distinguishes `local_stub` degraded output, real provider wiring, bounded native smoke, Graphiti native status, and long-running multiverse verification status.
- Re-verified Aquarium focused backend tests and frontend production build after runtime-label changes.
- Preserved and fast-forwarded the MiroFish canonical checkout: pre-existing dirty changes were stashed with a patch artifact before syncing `develop` to `origin/develop`.
- Ran MiroFish live-local multiverse expansion canary: `mv_4ef846551b2d`, 4 universes, 24 configured rounds, graph memory preflight healthy, 3 outcome clusters, 4 sensitivity axes.
- Caveat: the multiverse expansion canary proves live endpoint preflight + bounded real-backend comparison, not a long durable OASIS action-stream production run.

## 2026-06-30 — Native MiroFish runtime canary

- Ran Aquarium real integration canary with BettaFish `bettafish_cli` and MiroFish `mirofish_cli` providers, without the previous fake bridge.
- Verified live MiroFish backend + Graphiti graph build + OASIS bounded single simulation + Korean report generation.
- Evidence: run `aq_25badceb79ca`, graph `local_mirofish_3660f13154484f5b`, simulation `sim_3c7675d86e46`, report `report_d385e3807800`, 16 meaningful actions, CJK leakage 0.
- Updated QA/release docs to replace the prior fake-bridge caveat with the narrower remaining caveat: long-running multiverse/native production run remains unverified.

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
