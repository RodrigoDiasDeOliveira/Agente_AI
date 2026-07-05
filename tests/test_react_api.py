from fastapi.testclient import TestClient

from app.api import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_query_endpoint_with_empty_question():
    response = client.post(
        "/api/query",
        json={"question": "", "use_trusted": True},
    )
    assert response.status_code == 200
    body = response.json()
    assert "answer" in body
    assert "error" in body["answer"].lower() or "pergunta" in body["answer"].lower()
