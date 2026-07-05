# app/main.py
import json

from .feedback_handler import FeedbackHandler
from .search_space import SearchSpaceManager
from .trusted_search import TrustedAnswerSearch

trusted_search = TrustedAnswerSearch()
feedback_handler = FeedbackHandler()
search_manager = SearchSpaceManager()


def ask_question(question: str, use_trusted: bool):
    """Função principal de consulta."""
    if not question or question.strip() == "":
        return "Por favor, digite uma pergunta.", None, 0.0, ""

    if use_trusted:
        result = trusted_search.search(question)

        if isinstance(result, dict) and "match_document" in result:
            doc = result["match_document"]
            similarity = result.get("similarity", 0.0)
            target_id = result.get("target_id")

            response_text = f"""
**✅ Match Encontrado** ({similarity:.1%} de similaridade)

**Tipo:** {doc.get('type', 'N/A')}
**Título:** {doc.get('title', 'N/A')}
**Link/URL:** {doc.get('url', 'N/A')}

**Parâmetros:** {json.dumps(doc.get('parameters', {}), ensure_ascii=False)}
            """
            return response_text, target_id, similarity, question

        fallback_text = result.get("content", "Não foi possível encontrar uma resposta confiável.")
        return fallback_text, None, 0.0, question

    from .llm_agent import get_llm_response

    response = get_llm_response(question)
    return response, None, 0.0, question


def record_feedback(feedback_type: str, target_id, similarity, question):
    """Registra feedback do usuário."""
    if target_id and question:
        feedback_handler.record_feedback(
            query=question,
            target_id=target_id,
            similarity=similarity,
            feedback_type=feedback_type,
            comment="",
        )
        return f"✅ Feedback **{feedback_type}** registrado com sucesso!"
    return "Nenhum match para registrar feedback."