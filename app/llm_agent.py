from app.config import settings


def get_llm_response(question: str, num_chunks: int = 3) -> str:
    """
    Gera uma resposta utilizando o provedor configurado.
    """

    provider = settings.LLM_PROVIDER.lower()

    if provider == "ollama":
        return f"[Ollama] Resposta gerada para: {question}"

    if provider == "openai":
        return f"[OpenAI] Resposta gerada para: {question}"

    if provider == "groq":
        return f"[Groq] Resposta gerada para: {question}"

    if provider == "vertex":
        return (
            f"[Google Vertex AI - {settings.MODEL_NAME}] "
            f"Resposta gerada para: {question}"
        )

    if provider == "huggingface":
        return (
            f"[Hugging Face - {settings.MODEL_NAME}] "
            f"Resposta gerada para: {question}"
        )

    return (
        f"[LLM desconhecido: {provider}] "
        f"Resposta gerada para: {question}"
    )


def ask_agent(question: str, qa_chain=None, num_chunks: int = 3):
    return {
        "answer": get_llm_response(question, num_chunks),
        "sources": [],
    }