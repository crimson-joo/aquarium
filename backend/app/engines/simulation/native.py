from __future__ import annotations

from app.domain.contracts import Persona, SeedDocument, SimulationMode, SimulationResult, UniverseResult


def run_simulation(mode: SimulationMode, seed: SeedDocument, personas: list[Persona]) -> SimulationResult:
    if mode == SimulationMode.SINGLE:
        universes = [UniverseResult(
            name="Single Current",
            variation="baseline",
            dominant_signal=seed.key_points[0],
            events=[f"{persona.name}: {persona.stance}" for persona in personas],
        )]
    else:
        variations = ["baseline current", "optimistic branch", "constraint branch"]
        universes = [
            UniverseResult(
                name=f"Universe {index + 1}",
                variation=variation,
                dominant_signal=seed.key_points[index % len(seed.key_points)],
                events=[f"round {round_no}: {personas[(round_no + index) % len(personas)].name} shifted around {variation}" for round_no in range(1, 4)],
            )
            for index, variation in enumerate(variations)
        ]
    return SimulationResult(mode=mode, universes=universes)
