from pathlib import Path

from app.domain.pipeline import run_aquarium_pipeline
from app.domain.contracts import Locale, SimulationMode


def test_pipeline_creates_research_to_simulation_artifacts(tmp_path: Path):
    result = run_aquarium_pipeline(
        topic="AI 검색엔진 시장 변화",
        locale=Locale.KO,
        mode=SimulationMode.MULTIVERSE,
        storage_root=tmp_path,
    )

    assert result.run.topic == "AI 검색엔진 시장 변화"
    assert result.run.locale == Locale.KO
    assert result.run.mode == SimulationMode.MULTIVERSE
    assert result.run.status == "completed"
    assert result.manifest.handoff_version == "aquarium.v1"
    assert result.manifest.final_report_path.endswith("research_report.md")
    assert len(result.seed.key_points) >= 3
    assert len(result.ontology.entities) >= 3
    assert len(result.personas) >= 3
    assert len(result.simulation.universes) == 3
    assert "앙상블 빈도" in result.simulation_report.body
    assert "Ensemble Frequency" not in result.simulation_report.body
    assert Path(result.manifest.final_report_path).exists()
    assert Path(result.simulation_report.path).exists()


def test_pipeline_supports_single_mode_and_english_locale(tmp_path: Path):
    result = run_aquarium_pipeline(
        topic="Local AI agents",
        locale=Locale.EN,
        mode=SimulationMode.SINGLE,
        storage_root=tmp_path,
    )

    assert result.run.locale == Locale.EN
    assert len(result.simulation.universes) == 1
    assert result.simulation.universes[0].name == "Single Current"
    assert "not a prediction" in result.simulation_report.body.lower()
