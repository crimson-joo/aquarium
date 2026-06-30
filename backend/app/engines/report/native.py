from __future__ import annotations

from pathlib import Path

from app.core.i18n import msg
from app.domain.contracts import Locale, SimulationMode, SimulationReport, SimulationResult


def build_simulation_report(locale: Locale, simulation: SimulationResult, path: Path) -> SimulationReport:
    heading = msg(locale, "simulation_heading")
    lines = [heading, "", msg(locale, "caveat"), ""]
    if simulation.mode == SimulationMode.MULTIVERSE:
        lines.append(msg(locale, "ensemble_heading"))
        lines.append(msg(locale, "ensemble_note"))
    else:
        lines.append(msg(locale, "single_heading"))
        lines.append(msg(locale, "single_note"))
    for universe in simulation.universes:
        lines.extend(["", f"### {universe.name}", f"- variation: {universe.variation}", f"- dominant signal: {universe.dominant_signal}"])
        lines.extend(f"- {event}" for event in universe.events)
    body = "\n".join(lines)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return SimulationReport(path=str(path), body=body)
