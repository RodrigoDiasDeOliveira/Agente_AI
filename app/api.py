from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .main import ask_question, record_feedback

app = FastAPI(title="Agente AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str
    use_trusted: bool = True


class FeedbackRequest(BaseModel):
    feedback_type: str
    target_id: str | None = None
    similarity: float = 0.0
    question: str = ""


@app.get("/health")
def health():
    return {"status": "ok", "service": "agente-ai"}


@app.post("/api/query")
def query(request: QueryRequest):
    answer, target_id, similarity, question = ask_question(request.question, request.use_trusted)
    return {
        "answer": answer,
        "target_id": target_id,
        "similarity": similarity,
        "question": question,
    }


@app.post("/api/feedback")
def feedback(request: FeedbackRequest):
    message = record_feedback(
        request.feedback_type,
        request.target_id,
        request.similarity,
        request.question,
    )
    return {"message": message}
