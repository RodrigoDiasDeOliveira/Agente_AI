import pytest
import httpx
import os
import pandas as pd
from unittest.mock import AsyncMock, patch
from app.data_handler import analyze_interactions

# URL base da API do Gradio
BASE_URL = "http://localhost:7860"

# Marca os testes como assíncronos
pytestmark = pytest.mark.asyncio

# Teste para a API do Gradio
async def test_gradio_api_success():
    # Mock da função do LangChain/Grok
    with patch("app.main.chain", new=AsyncMock()) as mock_chain:
        mock_chain.invoke.return_value = {"content": "Resposta simulada do Grok"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/api/predict",
                json={"data": ["Qual é 2 + 2?"]}
            )
        assert response.status_code == 200
        assert "Resposta simulada do Grok" in response.json()["data"][0]

# Teste para pergunta vazia
async def test_gradio_api_empty_question():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/predict",
            json={"data": [""]}
        )
    assert response.status_code == 200
    assert "Erro: A pergunta não pode estar vazia" in response.json()["data"][0]

# Teste para entrada inválida
async def test_gradio_api_invalid_input():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/predict",
            json={"data": [None]}
        )
    assert response.status_code == 200
    assert "Erro" in response.json()["data"][0]

# Teste para verificar salvamento de interações
async def test_save_interaction():
    # Remove o arquivo CSV, se existir
    if os.path.isfile("interactions.csv"):
        os.remove("interactions.csv")
    
    # Mock da função do LangChain/Grok
    with patch("app.main.chain", new=AsyncMock()) as mock_chain:
        mock_chain.invoke.return_value = {"content": "Teste salvo"}
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{BASE_URL}/api/predict",
                json={"data": ["Teste de pergunta"]}
            )
    
    # Verifica se o CSV foi criado e contém a interação
    assert os.path.isfile("interactions.csv")
    df = pd.read_csv("interactions.csv")
    assert len(df) == 1
    assert df.iloc[0]["question"] == "Teste de pergunta"
    assert df.iloc[0]["answer"] == "Teste salvo"