import pytest
import httpx
from fastapi.testclient import TestClient
import pandas as pd
import os

# Usando TestClient do FastAPI (mais adequado)
@pytest.fixture
def client():
    from app.main import app  # ajuste o import conforme sua estrutura
    return TestClient(app)

def test_predict_endpoint_valid_question(client):
    response = client.post(
        "/api/ask",  # ou o endpoint correto que você usa
        json={"question": "O que diz o Código de Conduta Ética da FIESC?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Resposta" in data or "answer" in data
    assert data.get("Resposta") or data.get("answer")

def test_predict_endpoint_empty_question(client):
    response = client.post(
        "/api/ask",
        json={"question": ""}
    )
    assert response.status_code in [400, 422]
    data = response.json()
    assert "Erro" in str(data) or "empty" in str(data).lower()

def test_save_interaction():
    assert os.path.exists("interactions.csv")
    df = pd.read_csv("interactions.csv")
    assert len(df) > 0
    assert "question" in df.columns
    assert "answer" in df.columns
    assert "timestamp" in df.columns

def test_analyze_interactions():
    from app.data_handler import analyze_interactions
    result = analyze_interactions()
    assert result is not None
