from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_query_endpoint_with_empty_question():
    response = client.post(
        "/api/ask",
        json={"question": "", "use_trusted": True},
    )
    assert response.status_code == 200
    body = response.json()
    assert "answer" in body
    assert "error" in body["answer"].lower() or "pergunta" in body["answer"].lower()

def test_feedback_endpoint_contract():
    response = client.post(
        "/api/feedback",
        json={"feedback_type": "positive", "target_id": "target-1", "similarity": 0.9, "question": "teste"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "message" in body


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    body = response.text
    assert "http_requests_total" in body