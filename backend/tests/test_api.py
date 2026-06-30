import time

from fastapi.testclient import TestClient

from app.main import create_app


def _wait_for_job(client: TestClient, job_id: str, timeout: float = 5.0):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        response = client.get(f"/api/jobs/{job_id}")
        assert response.status_code == 200
        last = response.json()
        if last["status"] in {"succeeded", "failed", "cancelled"}:
            return last
        time.sleep(0.05)
    raise AssertionError(f"job did not finish: {last}")


def test_create_run_job_lifecycle_and_chat(tmp_path, monkeypatch):
    monkeypatch.setenv("AQUARIUM_DATA_DIR", str(tmp_path))
    client = TestClient(create_app())

    response = client.post("/api/runs", json={
        "topic": "로컬 검색엔진 기반 보고서",
        "locale": "ko",
        "mode": "multiverse",
    })

    assert response.status_code == 202
    queued = response.json()
    assert queued["status"] in {"queued", "running", "succeeded"}
    assert queued["progress"] >= 0
    assert queued["links"]["job"].endswith(queued["job_id"])
    job = _wait_for_job(client, queued["job_id"])
    assert job["status"] == "succeeded"
    assert job["progress"] == 100
    assert job["stage"] == "completed"
    assert job["attempts"] == 1
    body = job["result"]
    assert body["status"] == "completed"
    assert body["mode"] == "multiverse"
    assert body["runtime_claim"]["runtime_level"] == "aquarium_native"
    assert body["runtime_claim"]["standalone_native"] is True
    assert body["runtime_claim"]["external_runner_dependency"] is False
    assert body["runtime_claim"]["graph_engine_status"] == "aquarium_native"
    assert body["runtime_claim"]["graph_memory_status"] == "not_configured"
    assert body["runtime_claim"]["long_running_multiverse_verified"] is False
    assert [stage["name"] for stage in body["stages"]] == ["aquarium_research", "aquarium_simulation"]
    assert [entity["name"] for entity in body["ecosystem"]["entities"]]
    assert [persona["name"] for persona in body["ecosystem"]["personas"]]
    assert len(body["simulation"]["universes"]) == 3
    assert body["report"]["preview"]
    assert body["artifacts"]["handoff_manifest"].endswith("handoff_manifest.json")
    run_id = body["run_id"]

    detail = client.get(f"/api/runs/{run_id}")
    assert detail.status_code == 200
    assert detail.json()["run_id"] == run_id

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


def test_can_cancel_queued_job_and_resume(tmp_path, monkeypatch):
    monkeypatch.setenv("AQUARIUM_DATA_DIR", str(tmp_path))
    app = create_app()
    client = TestClient(app)

    job = app.state.lifecycle_store.create_job("취소 후 재개", "ko", "single")
    cancel = client.post(f"/api/jobs/{job['job_id']}/cancel")
    assert cancel.status_code == 200
    assert cancel.json()["status"] == "cancelled"
    assert client.get(f"/api/runs/{job['run_id']}").status_code == 404

    resume = client.post(f"/api/jobs/{job['job_id']}/resume")
    assert resume.status_code == 200
    resumed = _wait_for_job(client, job["job_id"])
    assert resumed["status"] == "succeeded"
    assert resumed["attempts"] == 1
    assert resumed["result"]["mode"] == "single"


def test_retry_rejects_non_terminal_job(tmp_path, monkeypatch):
    monkeypatch.setenv("AQUARIUM_DATA_DIR", str(tmp_path))
    app = create_app()
    client = TestClient(app)
    job = app.state.lifecycle_store.create_job("아직 대기", "ko", "single")

    response = client.post(f"/api/jobs/{job['job_id']}/retry")
    assert response.status_code == 409

    missing = client.post("/api/jobs/job_missing/retry")
    assert missing.status_code == 404


def test_startup_marks_interrupted_running_jobs_failed(tmp_path, monkeypatch):
    monkeypatch.setenv("AQUARIUM_DATA_DIR", str(tmp_path))
    app = create_app()
    job = app.state.lifecycle_store.create_job("재시작 복구", "ko", "single")
    app.state.lifecycle_store.mark_running(job["job_id"], "simulation")
    app.state.job_worker.shutdown(wait=False)
    app.state.lifecycle_store.close()

    recovered = create_app()
    client = TestClient(recovered)
    response = client.get(f"/api/jobs/{job['job_id']}")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "failed"
    assert body["stage"] == "interrupted"
    assert body["error"] == "Worker interrupted before completion"
