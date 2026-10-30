import app as report_app


def test_homepage_loads():
    client = report_app.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Simple Report Generator" in response.data


def test_health_endpoint():
    client = report_app.app.test_client()
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_generate_rejects_missing_topic():
    client = report_app.app.test_client()
    response = client.post("/api/generate", json={"topic": "  "})
    assert response.status_code == 400
    assert "topic" in response.get_json()["error"].lower()


def test_generate_rejects_long_topic():
    client = report_app.app.test_client()
    response = client.post("/api/generate", json={"topic": "x" * 201})
    assert response.status_code == 400


def test_generate_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = report_app.app.test_client()
    response = client.post("/api/generate", json={"topic": "Renewable energy"})
    assert response.status_code == 503
    assert "OPENAI_API_KEY" in response.get_json()["error"]


def test_generate_returns_report(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(report_app, "generate_report", lambda topic: f"Report about {topic}")
    client = report_app.app.test_client()
    response = client.post("/api/generate", json={"topic": "Renewable energy"})
    assert response.status_code == 200
    assert response.get_json() == {
        "topic": "Renewable energy",
        "report": "Report about Renewable energy",
    }
