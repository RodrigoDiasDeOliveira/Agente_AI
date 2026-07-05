# app/admin.py
import json

from sqlalchemy import text

from .feedback_handler import FeedbackHandler
from .models import MatchDocument, SearchTargetCreate
from .search_space import SearchSpaceManager
from .trusted_search import TrustedAnswerSearch

manager = SearchSpaceManager()
trusted_search = TrustedAnswerSearch()
feedback_handler = FeedbackHandler()


def create_target(target_id, description, alt_phrases, doc_type, url, title, params):
    try:
        alt_list = [p.strip() for p in alt_phrases.split("\n") if p.strip()]
        match_doc = MatchDocument(
            type=doc_type,
            url=url,
            title=title,
            parameters=json.loads(params) if params.strip() else {},
        )

        target = SearchTargetCreate(
            target_id=target_id,
            description=description,
            alternative_phrases=alt_list,
            match_document=match_doc,
        )
        manager.add_manual_target(target)
        return "✅ Target criado com sucesso!"
    except Exception as exc:  # noqa: BLE001
        return f"❌ Erro: {exc}"


def load_pdfs():
    count = manager.load_pdfs_to_targets()
    return f"✅ {count} targets criados a partir dos PDFs!"


def list_targets():
    """Lista todos os targets cadastrados."""
    session = trusted_search.Session()
    result = session.execute(
        text(
            "SELECT target_id, description, match_document->>'type' as type "
            "FROM search_targets ORDER BY created_at DESC"
        )
    )
    targets = [f"**{row.target_id}** ({row.type}): {row.description[:100]}..." for row in result]
    session.close()
    return "\n\n".join(targets) if targets else "Nenhum target cadastrado ainda."


def show_feedback_stats():
    stats = feedback_handler.get_feedback_stats()
    recent = feedback_handler.get_recent_feedback(limit=10)

    stats_text = "### Estatísticas de Feedback\n\n"
    for ftype, data in stats.items():
        stats_text += f"- **{ftype.capitalize()}**: {data['count']} feedbacks (similaridade média: {data['avg_similarity']:.1%})\n"

    recent_text = "\n\n### Últimos Feedbacks\n\n"
    for fb in recent:
        recent_text += f"- **{fb['feedback_type']}** → {fb['query'][:80]}... (sim: {fb['similarity']:.1%})\n"

    return stats_text + recent_text