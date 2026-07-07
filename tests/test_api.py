import pytest
import pandas as pd
import os
from fastapi.testclient import TestClient

# Import the main FastAPI app
from app.main import app   # ← Ajuste se o arquivo principal for app/api.py

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

# ====================== Testes Básicos ======================

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"


def test_predict_endpoint_valid_question(client):
    response = client.post(
        "/api/ask",
        json={"question": "O que diz o Código de Conduta Ética da FIESC?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Resposta" in data or "answer" in data


def test_predict_endpoint_empty_question(client):
    response = client.post(
        "/api/ask",
        json={"question": ""}
    )
    assert response.status_code in [400, 422]
    data = response.json()
    assert "Erro" in str(data) or "empty" in str(data).lower() or "pergunta" in str(data).lower()


# ====================== Testes de Dados ======================

def test_save_interaction():
    assert os.path.exists("interactions.csv"), "Arquivo interactions.csv não encontrado"
    df = pd.read_csv("interactions.csv")
    assert len(df) > 0
    assert all(col in df.columns for col in ["question", "answer", "timestamp"])


def test_analyze_interactions():
    from app.data_handler import analyze_interactions
    result = analyze_interactions()
    assert result is not None


# ====================== Outros Endpoints ======================

def test_feedback_endpoint(client):
    response = client.post(
        "/api/feedback",
        json={
            "feedback_type": "positive",
            "target_id": "target-1",
            "similarity": 0.9,
            "question": "teste"
        }
    )
    assert response.status_code == 200


def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
