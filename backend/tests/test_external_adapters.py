from __future__ import annotations

import json
import os
from pathlib import Path

from app.domain.contracts import Locale, SimulationMode
from app.domain.pipeline import run_aquarium_pipeline


def _write_executable(path: Path, body: str) -> Path:
    path.write_text(body, encoding="utf-8")
    path.chmod(path.stat().st_mode | 0o111)
    return path


def test_pipeline_uses_configured_bettafish_cli_adapter(tmp_path: Path, monkeypatch):
    script = _write_executable(
        tmp_path / "fake_bettafish.py",
        """
#!/usr/bin/env python3
import json, os, pathlib
run_dir = pathlib.Path(os.environ['AQUARIUM_RUN_DIR'])
report = run_dir / 'real_bettafish_report.md'
report.write_text('# REAL BETTAFISH\\n\\n- 실제 조사 결과\\n- 데이터 갭 보존\\n', encoding='utf-8')
manifest = {
  'handoff_version': 'aquarium.v1',
  'source_product': 'bettafish-localized',
  'target_product': 'aquarium',
  'topic': os.environ['AQUARIUM_TOPIC'],
  'locale': os.environ['AQUARIUM_LOCALE'],
  'final_report_path': str(report),
  'intermediate_outputs': {'final_report': str(report)},
  'sources': [{'title': 'fake real source', 'url': 'local://fake', 'snippet': 'adapter'}],
  'provider': 'bettafish_cli',
  'warnings': [],
  'data_gaps': ['fake adapter gap']
}
(run_dir / 'bettafish_handoff_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')
""".lstrip(),
    )
    monkeypatch.setenv("AQUARIUM_BETTAFISH_COMMAND", f"python3 {script}")

    result = run_aquarium_pipeline("실제 어댑터 연결", Locale.KO, SimulationMode.SINGLE, tmp_path)

    assert result.manifest.provider == "bettafish_cli"
    assert result.manifest.final_report_path.endswith("real_bettafish_report.md")
    assert Path(result.manifest.final_report_path).read_text(encoding="utf-8").startswith("# REAL BETTAFISH")
    assert result.seed.key_points[:2] == ["실제 조사 결과", "데이터 갭 보존"]
    assert result.run.stages[0].provider == "bettafish_cli"
    assert result.run.stages[0].status == "completed"


def test_pipeline_rejects_mismatched_bettafish_provider(tmp_path: Path, monkeypatch):
    script = _write_executable(
        tmp_path / "fake_bettafish_stub_provider.py",
        """
#!/usr/bin/env python3
import json, os, pathlib
run_dir = pathlib.Path(os.environ['AQUARIUM_RUN_DIR'])
report = run_dir / 'stub_report.md'
report.write_text('# Stub report\\n\\n- should not pass as real\\n', encoding='utf-8')
manifest = {
  'handoff_version': 'aquarium.v1',
  'source_product': 'bettafish-localized',
  'target_product': 'aquarium',
  'topic': os.environ['AQUARIUM_TOPIC'],
  'locale': os.environ['AQUARIUM_LOCALE'],
  'final_report_path': str(report),
  'provider': 'local_stub',
  'warnings': [],
  'data_gaps': []
}
(run_dir / 'bettafish_handoff_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')
""".lstrip(),
    )
    monkeypatch.setenv("AQUARIUM_BETTAFISH_COMMAND", f"python3 {script}")

    result = run_aquarium_pipeline("provider mismatch", Locale.KO, SimulationMode.SINGLE, tmp_path)

    assert result.manifest.provider == "local_stub"
    assert result.run.stages[0].provider == "local_stub"
    assert result.run.stages[0].status == "degraded"
    assert any("provider" in warning for warning in result.run.stages[0].warnings)


def test_adapter_env_does_not_leak_unallowlisted_secret(tmp_path: Path, monkeypatch):
    script = _write_executable(
        tmp_path / "fake_bettafish_env_probe.py",
        """
#!/usr/bin/env python3
import json, os, pathlib
run_dir = pathlib.Path(os.environ['AQUARIUM_RUN_DIR'])
probe = run_dir / 'env_probe.json'
probe.write_text(json.dumps({'has_secret': 'SECRET_TOKEN' in os.environ, 'has_topic': os.environ.get('AQUARIUM_TOPIC')}), encoding='utf-8')
report = run_dir / 'real_bettafish_report.md'
report.write_text('# REAL BETTAFISH\\n\\n- env probe\\n', encoding='utf-8')
manifest = {
  'handoff_version': 'aquarium.v1',
  'source_product': 'bettafish-localized',
  'target_product': 'aquarium',
  'topic': os.environ['AQUARIUM_TOPIC'],
  'locale': os.environ['AQUARIUM_LOCALE'],
  'final_report_path': str(report),
  'intermediate_outputs': {'probe': str(probe)},
  'sources': [],
  'provider': 'bettafish_cli',
  'warnings': [],
  'data_gaps': []
}
(run_dir / 'bettafish_handoff_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')
""".lstrip(),
    )
    monkeypatch.setenv("AQUARIUM_BETTAFISH_COMMAND", f"python3 {script}")
    monkeypatch.setenv("SECRET_TOKEN", "do-not-leak")

    result = run_aquarium_pipeline("secret env guard", Locale.KO, SimulationMode.SINGLE, tmp_path)
    probe = json.loads(Path(result.manifest.intermediate_outputs["probe"]).read_text(encoding="utf-8"))

    assert probe == {"has_secret": False, "has_topic": "secret env guard"}


def test_pipeline_uses_configured_mirofish_cli_adapter(tmp_path: Path, monkeypatch):
    script = _write_executable(
        tmp_path / "fake_mirofish.py",
        """
#!/usr/bin/env python3
import json, os, pathlib
run_dir = pathlib.Path(os.environ['AQUARIUM_RUN_DIR'])
report = run_dir / 'real_mirofish_report.md'
report.write_text('# REAL MIROFISH\\n\\n시뮬레이션 완료', encoding='utf-8')
payload = {
  'provider': 'mirofish_cli',
  'ontology': {'entities': [{'name': '실제 엔티티', 'type': 'Signal', 'rationale': 'fake cli'}], 'relations': []},
  'personas': [{'name': '실제 페르소나', 'role': '현장 관찰자', 'stance': '증거 중심'}],
  'simulation': {'mode': os.environ['AQUARIUM_MODE'], 'universes': [{'name': 'Real Universe', 'variation': 'adapter', 'dominant_signal': '실제 조사 결과', 'events': ['external cli event']}]},
  'simulation_report': {'path': str(report), 'body': report.read_text(encoding='utf-8')},
  'warnings': []
}
(run_dir / 'mirofish_result.json').write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
""".lstrip(),
    )
    monkeypatch.setenv("AQUARIUM_MIROFISH_COMMAND", f"python3 {script}")

    result = run_aquarium_pipeline("실제 시뮬레이션 연결", Locale.KO, SimulationMode.MULTIVERSE, tmp_path)

    assert result.ontology.entities[0].name == "실제 엔티티"
    assert result.personas[0].name == "실제 페르소나"
    assert result.simulation.universes[0].name == "Real Universe"
    assert result.simulation_report.path.endswith("real_mirofish_report.md")
    assert result.run.stages[-1].provider == "mirofish_cli"
    assert result.run.stages[-1].status == "completed"


def test_pipeline_rejects_mirofish_completed_result_with_missing_report_path(tmp_path: Path, monkeypatch):
    script = _write_executable(
        tmp_path / "fake_mirofish_missing_report.py",
        """
#!/usr/bin/env python3
import json, os, pathlib
run_dir = pathlib.Path(os.environ['AQUARIUM_RUN_DIR'])
missing = run_dir / 'missing_real_mirofish_report.md'
payload = {
  'provider': 'mirofish_cli',
  'ontology': {'entities': [{'name': '실제 엔티티', 'type': 'Signal', 'rationale': 'fake cli'}], 'relations': []},
  'personas': [{'name': '실제 페르소나', 'role': '현장 관찰자', 'stance': '증거 중심'}],
  'simulation': {'mode': os.environ['AQUARIUM_MODE'], 'universes': [{'name': 'Real Universe', 'variation': 'adapter', 'dominant_signal': '실제 조사 결과', 'events': ['external cli event']}]},
  'simulation_report': {'path': str(missing), 'body': '# FAKE BODY WITHOUT FILE'},
  'warnings': []
}
(run_dir / 'mirofish_result.json').write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
""".lstrip(),
    )
    monkeypatch.setenv("AQUARIUM_MIROFISH_COMMAND", f"python3 {script}")

    result = run_aquarium_pipeline("missing report guard", Locale.KO, SimulationMode.SINGLE, tmp_path)

    assert result.run.stages[-1].provider == "local_stub"
    assert result.run.stages[-1].status == "degraded"
    assert any("report path is not readable" in warning for warning in result.run.stages[-1].warnings)
    assert not result.simulation_report.path.endswith("missing_real_mirofish_report.md")


def test_pipeline_rejects_mirofish_completed_result_with_body_that_does_not_match_report_file(tmp_path: Path, monkeypatch):
    script = _write_executable(
        tmp_path / "fake_mirofish_mismatched_report.py",
        """
#!/usr/bin/env python3
import json, os, pathlib
run_dir = pathlib.Path(os.environ['AQUARIUM_RUN_DIR'])
report = run_dir / 'real_mirofish_report.md'
report.write_text('# REAL MIROFISH\\n\\n파일의 실제 본문', encoding='utf-8')
payload = {
  'provider': 'mirofish_cli',
  'ontology': {'entities': [{'name': '실제 엔티티', 'type': 'Signal', 'rationale': 'fake cli'}], 'relations': []},
  'personas': [{'name': '실제 페르소나', 'role': '현장 관찰자', 'stance': '증거 중심'}],
  'simulation': {'mode': os.environ['AQUARIUM_MODE'], 'universes': [{'name': 'Real Universe', 'variation': 'adapter', 'dominant_signal': '실제 조사 결과', 'events': ['external cli event']}]},
  'simulation_report': {'path': str(report), 'body': '# SYNTHETIC CHAT PREVIEW'},
  'warnings': []
}
(run_dir / 'mirofish_result.json').write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
""".lstrip(),
    )
    monkeypatch.setenv("AQUARIUM_MIROFISH_COMMAND", f"python3 {script}")

    result = run_aquarium_pipeline("mismatched report guard", Locale.KO, SimulationMode.SINGLE, tmp_path)

    assert result.run.stages[-1].provider == "local_stub"
    assert result.run.stages[-1].status == "degraded"
    assert any("report body does not match" in warning for warning in result.run.stages[-1].warnings)


def test_pipeline_rejects_mirofish_report_path_outside_run_dir(tmp_path: Path, monkeypatch):
    outside_dir = tmp_path.parent / f"{tmp_path.name}_outside"
    outside_dir.mkdir()
    outside_report = outside_dir / "outside_report.md"
    outside_report.write_text("# OUTSIDE\n\nnot an Aquarium run artifact", encoding="utf-8")
    script = _write_executable(
        tmp_path / "fake_mirofish_outside_report.py",
        f"""
#!/usr/bin/env python3
import json, os, pathlib
run_dir = pathlib.Path(os.environ['AQUARIUM_RUN_DIR'])
report = pathlib.Path({str(outside_report)!r})
body = report.read_text(encoding='utf-8')
payload = {{
  'provider': 'mirofish_cli',
  'ontology': {{'entities': [{{'name': '실제 엔티티', 'type': 'Signal', 'rationale': 'fake cli'}}], 'relations': []}},
  'personas': [{{'name': '실제 페르소나', 'role': '현장 관찰자', 'stance': '증거 중심'}}],
  'simulation': {{'mode': os.environ['AQUARIUM_MODE'], 'universes': [{{'name': 'Real Universe', 'variation': 'adapter', 'dominant_signal': '실제 조사 결과', 'events': ['external cli event']}}]}},
  'simulation_report': {{'path': str(report), 'body': body}},
  'warnings': []
}}
(run_dir / 'mirofish_result.json').write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
""".lstrip(),
    )
    monkeypatch.setenv("AQUARIUM_MIROFISH_COMMAND", f"python3 {script}")

    result = run_aquarium_pipeline("outside report guard", Locale.KO, SimulationMode.SINGLE, tmp_path)

    assert result.run.stages[-1].provider == "local_stub"
    assert result.run.stages[-1].status == "degraded"
    assert any("outside run directory" in warning for warning in result.run.stages[-1].warnings)
