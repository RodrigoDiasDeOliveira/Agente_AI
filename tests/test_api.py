import pytest
from gradio_client import Client
import pandas as pd
import os

@pytest.fixture
def client():
    return Client("http://localhost:7860/")

@pytest.mark.asyncio
async def test_predict_endpoint_valid_question(client):
    response = await client.predict(
        question="O que diz o Código de Conduta Ética da FIESC?",
        fn_index=0
    )
    assert response is not None
    assert "Resposta" in response
    assert "Fontes" in response

@pytest.mark.asyncio
async def test_predict_endpoint_empty_question(client):
    response = await client.predict(
        question="",
        fn_index=0
    )
    assert "Erro: A pergunta não pode estar vazia." in response

@pytest.mark.asyncio
async def test_save_interaction():
    # Verifica se interactions.csv existe e contém dados
    assert os.path.exists("interactions.csv")
    df = pd.read_csv("interactions.csv")
    assert len(df) > 0
    assert "question" in df.columns
    assert "answer" in df.columns
    assert "timestamp" in df.columns

@pytest.mark.asyncio
async def test_analyze_interactions():
    # Verifica se a análise retorna algo
    from app.data_handler import analyze_interactions
    result = analyze_interactions()
    assert result is not None