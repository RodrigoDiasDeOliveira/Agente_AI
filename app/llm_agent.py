import os

from app.config import HUGGINGFACEHUB_API_TOKEN, LLM_PROVIDER, MODEL_NAME


def get_llm_response(question, num_chunks=3):
    provider = (LLM_PROVIDER or "huggingface").lower()
    if provider == "ollama":
        return f"[Ollama] Resposta gerada para: {question}"
    if provider == "openai":
        return f"[OpenAI] Resposta gerada para: {question}"
    if provider == "groq":
        return f"[Groq] Resposta gerada para: {question}"
    return f"Resposta gerada com {MODEL_NAME} para: {question}"


def ask_agent(question, qa_chain, num_chunks=3):
    return {"answer": get_llm_response(question, num_chunks), "sources": []}