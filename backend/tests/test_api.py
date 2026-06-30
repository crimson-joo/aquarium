from fastapi.testclient import TestClient

from app.main import create_app


def test_create_run_and_chat(tmp_path, monkeypatch):
    monkeypatch.setenv("AQUARIUM_DATA_DIR", str(tmp_path))
    client = TestClient(create_app())

    response = client.post("/api/runs", json={
        "topic": "로컬 검색엔진 기반 보고서",
        "locale": "ko",
        "mode": "multiverse",
    })

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["mode"] == "multiverse"
    assert body["runtime_claim"]["runtime_level"] == "aquarium_native"
    assert body["runtime_claim"]["standalone_native"] is True
    assert body["runtime_claim"]["external_runner_dependency"] is False
    assert body["runtime_claim"]["long_running_multiverse_verified"] is False
    assert [stage["name"] for stage in body["stages"]] == ["aquarium_research", "aquarium_simulation"]
    assert body["artifacts"]["handoff_manifest"].endswith("handoff_manifest.json")
    run_id = body["run_id"]

    detail = client.get(f"/api/runs/{run_id}")
    assert detail.status_code == 200
    assert detail.json()["manifest"]["handoff_version"] == "aquarium.v1"

    chat = client.post(f"/api/runs/{run_id}/chat", json={"question": "어떤 분기가 중요해?"})
    assert chat.status_code == 200
    assert "시뮬레이션" in chat.json()["answer"]


def test_rejects_unsupported_locale(tmp_path, monkeypatch):
    monkeypatch.setenv("AQUARIUM_DATA_DIR", str(tmp_path))
    client = TestClient(create_app())

    response = client.post("/api/runs", json={
        "topic": "test",
        "locale": "fr",
        "mode": "single",
    })

    assert response.status_code == 422
