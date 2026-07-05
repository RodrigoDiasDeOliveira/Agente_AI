from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import text

from .feedback_handler import FeedbackHandler
from .models import MatchDocument, SearchTargetCreate
from .search_space import SearchSpaceManager
from .trusted_search import TrustedAnswerSearch

app = FastAPI(title="Agente AI Admin API", version="1.0.0")

manager = SearchSpaceManager()
trusted_search = TrustedAnswerSearch()
feedback_handler = FeedbackHandler()


class TargetPayload(BaseModel):
    target_id: str
    description: str
    alternative_phrases: list[str] = []
    doc_type: str = "policy"
    url: str = ""
    title: str = ""
    params: dict = {}


@app.post("/admin/targets")
def create_target(payload: TargetPayload):
    try:
        match_doc = MatchDocument(
            type=payload.doc_type,
            url=payload.url,
            title=payload.title,
            parameters=payload.params,
        )
        target = SearchTargetCreate(
            target_id=payload.target_id,
            description=payload.description,
            alternative_phrases=payload.alternative_phrases,
            match_document=match_doc,
        )
        manager.add_manual_target(target)
        return {"message": "Target criado com sucesso!"}
    except Exception as exc:  # noqa: BLE001
        return {"message": f"Erro ao criar target: {exc}"}


@app.post("/admin/load-pdfs")
def load_pdfs():
    count = manager.load_pdfs_to_targets()
    return {"message": f"{count} targets criados a partir dos PDFs!"}


@app.get("/admin/targets")
def list_targets():
    session = trusted_search.Session()
    result = session.execute(
        text(
            "SELECT target_id, description, match_document->>'type' as type "
            "FROM search_targets ORDER BY created_at DESC"
        )
    )
    targets = [
        {"target_id": row.target_id, "type": row.type, "description": row.description}
        for row in result
    ]
    session.close()
    return {"targets": targets}


@app.get("/admin/feedback")
def feedback_stats():
    stats = feedback_handler.get_feedback_stats()
    recent = feedback_handler.get_recent_feedback(limit=10)
    return {"stats": stats, "recent": recent}
