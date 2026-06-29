from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _write_executable(path: Path, body: str) -> Path:
    path.write_text(body, encoding="utf-8")
    path.chmod(path.stat().st_mode | 0o111)
    return path


def test_real_integration_canary_passes_with_fake_contract_runners(tmp_path: Path):
    betta = _write_executable(
        tmp_path / "fake_bettafish.py",
        """
#!/usr/bin/env python3
import json, os, pathlib
run_dir = pathlib.Path(os.environ['AQUARIUM_RUN_DIR'])
report = run_dir / 'bettafish_real_report.md'
report.write_text('# BettaFish real fixture\\n\\n- real signal\\n- warning preserved\\n', encoding='utf-8')
manifest = {
  'handoff_version': 'aquarium.v1',
  'source_product': 'bettafish-localized',
  'target_product': 'aquarium',
  'topic': os.environ['AQUARIUM_TOPIC'],
  'locale': os.environ['AQUARIUM_LOCALE'],
  'final_report_path': str(report),
  'intermediate_outputs': {'query': str(report)},
  'sources': [],
  'provider': 'bettafish_cli',
  'warnings': ['fixture warning'],
  'data_gaps': ['fixture source gap']
}
(run_dir / 'bettafish_handoff_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')
""".lstrip(),
    )
    miro = _write_executable(
        tmp_path / "fake_mirofish.py",
        """
#!/usr/bin/env python3
import json, os, pathlib
run_dir = pathlib.Path(os.environ['AQUARIUM_RUN_DIR'])
assert pathlib.Path(os.environ['AQUARIUM_HANDOFF_MANIFEST']).name == 'handoff_manifest.json'
report = run_dir / 'mirofish_real_report.md'
body = '# MiroFish real fixture\\n\\nGraphiti 직접 처리(Native) 여부는 fixture warning으로만 표기합니다.'
report.write_text(body, encoding='utf-8')
payload = {
  'provider': 'mirofish_cli',
  'ontology': {'entities': [{'name': 'real signal', 'type': 'Signal', 'rationale': 'fake runner'}], 'relations': []},
  'personas': [{'name': 'observer', 'role': 'signal watcher', 'stance': 'evidence first'}],
  'simulation': {'mode': os.environ['AQUARIUM_MODE'], 'universes': [{'name': 'Single Current', 'variation': 'real fixture', 'dominant_signal': 'real signal', 'events': ['fixture event']}]},
  'simulation_report': {'path': str(report), 'body': body},
  'warnings': ['graph_memory_native_unverified_fixture']
}
(run_dir / 'mirofish_result.json').write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
""".lstrip(),
    )

    env = os.environ.copy()
    env.update(
        {
            "AQUARIUM_BETTAFISH_COMMAND": f"{sys.executable} {betta}",
            "AQUARIUM_MIROFISH_COMMAND": f"{sys.executable} {miro}",
            "AQUARIUM_CANARY_DATA_DIR": str(tmp_path / "data"),
            "AQUARIUM_CANARY_TOPIC": "실제 러너 계약 검증",
            "AQUARIUM_CANARY_LOCALE": "ko",
            "AQUARIUM_CANARY_MODE": "single",
        }
    )

    completed = subprocess.run(
        ["bash", "scripts/run_real_integration_canary.sh"],
        cwd=Path(__file__).resolve().parents[2],
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    summary = json.loads(completed.stdout)

    assert summary["status"] == "pass"
    assert summary["real_integration"] is True
    assert summary["providers"] == {"bettafish_report": "bettafish_cli", "mirofish_simulation": "mirofish_cli"}
    assert summary["stage_statuses"] == {"bettafish_report": "completed", "mirofish_simulation": "completed"}
    assert summary["warnings"] == ["fixture warning", "graph_memory_native_unverified_fixture"]
    assert Path(summary["result_path"]).exists()


def test_real_integration_canary_fails_when_runner_provider_is_not_real(tmp_path: Path):
    betta = _write_executable(
        tmp_path / "fake_bettafish_stub_provider.py",
        """
#!/usr/bin/env python3
import json, os, pathlib
run_dir = pathlib.Path(os.environ['AQUARIUM_RUN_DIR'])
report = run_dir / 'stub_report.md'
report.write_text('# Stub\\n\\n- fake real\\n', encoding='utf-8')
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
    env = os.environ.copy()
    env.update(
        {
            "AQUARIUM_BETTAFISH_COMMAND": f"{sys.executable} {betta}",
            "AQUARIUM_MIROFISH_COMMAND": "",
            "AQUARIUM_CANARY_DATA_DIR": str(tmp_path / "data"),
        }
    )

    completed = subprocess.run(
        ["bash", "scripts/run_real_integration_canary.sh"],
        cwd=Path(__file__).resolve().parents[2],
        env=env,
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 2
    summary = json.loads(completed.stdout)
    assert summary["real_integration"] is False
    assert summary["providers"]["bettafish_report"] == "local_stub"


def test_real_integration_canary_fails_when_any_stage_is_degraded(tmp_path: Path):
    env = os.environ.copy()
    env.update(
        {
            "AQUARIUM_BETTAFISH_COMMAND": "",
            "AQUARIUM_MIROFISH_COMMAND": "",
            "AQUARIUM_CANARY_DATA_DIR": str(tmp_path / "data"),
        }
    )

    completed = subprocess.run(
        ["bash", "scripts/run_real_integration_canary.sh"],
        cwd=Path(__file__).resolve().parents[2],
        env=env,
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 2
    summary = json.loads(completed.stdout)
    assert summary["status"] == "degraded"
    assert summary["real_integration"] is False
    assert summary["providers"] == {"bettafish_report": "local_stub", "mirofish_simulation": "local_stub"}
