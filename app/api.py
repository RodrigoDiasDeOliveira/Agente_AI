import logging
import time
from collections import Counter

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text

from .admin_api import app as admin_app
from .config import CORS_ORIGINS, DATABASE_URL
from .main import ask_question, record_feedback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agente_ai")

app = FastAPI(
    title="Agente AI API",
    version="1.0.0",
    description="API para consulta de políticas e feedback de compliance.",
)
app.mount("/admin", admin_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(DATABASE_URL)
request_counter = Counter()
latency_histogram = Counter()
rate_limit_hits = Counter()
request_timestamps: dict[str, list[float]] = {}


class QueryRequest(BaseModel):
    question: str
    use_trusted: bool = True


class FeedbackRequest(BaseModel):
    feedback_type: str
    target_id: str | None = None
    similarity: float = 0.0
    question: str = ""


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    request_counter[request.url.path] += 1
    latency_histogram[request.url.path] += int(elapsed_ms)
    logger.info(
        "request_completed",
        extra={"path": request.url.path, "method": request.method, "elapsed_ms": elapsed_ms},
    )
    return response


def check_rate_limit(request: Request, limit: int, window_seconds: int = 60):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    timestamps = request_timestamps.setdefault(client_ip, [])
    timestamps[:] = [ts for ts in timestamps if now - ts < window_seconds]
    if len(timestamps) >= limit:
        rate_limit_hits[request.url.path] += 1
        return False
    timestamps.append(now)
    return True


@app.get("/health", summary="Health check", description="Retorna o estado do serviço e da conexão com o banco.")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            if "postgres" in DATABASE_URL.lower():
                vector_enabled = connection.execute(
                    text("SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector')")
                ).scalar()
            else:
                vector_enabled = True
            return {
                "status": "ok",
                "service": "agente-ai",
                "database": {
                    "ok": True,
                    "vector_extension": bool(vector_enabled),
                },
            }
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "ok",
            "service": "agente-ai",
            "database": {
                "ok": False,
                "error": str(exc),
            },
        }


@app.post(
    "/api/query",
    summary="Consulta de resposta",
    description="Consulta uma resposta confiável para uma pergunta usando o mecanismo de busca ou o fallback LLM.",
)
@app.post(
    "/api/ask",
    summary="Consulta de resposta",
    description="Consulta uma resposta confiável para uma pergunta usando o mecanismo de busca ou o fallback LLM.",
)
def query(request: Request, payload: QueryRequest):
    if not check_rate_limit(request, 10, 60):
        return {"error": "rate_limit", "message": "Limite de requisições atingido."}
    answer, target_id, similarity, question = ask_question(payload.question, payload.use_trusted)
    return {
        "answer": answer,
        "target_id": target_id,
        "similarity": similarity,
        "question": question,
    }


@app.post(
    "/api/feedback",
    summary="Registrar feedback",
    description="Registra o feedback do usuário sobre a resposta recebida.",
)
def feedback(request: Request, payload: FeedbackRequest):
    if not check_rate_limit(request, 20, 60):
        return {"error": "rate_limit", "message": "Limite de requisições atingido."}
    message = record_feedback(
        payload.feedback_type,
        payload.target_id,
        payload.similarity,
        payload.question,
    )
    return {"message": message}


@app.get("/metrics", summary="Métricas Prometheus", description="Expõe métricas simples em formato Prometheus para observabilidade.")
def metrics():
    lines = ["# HELP http_requests_total Total de requisições recebidas", "# TYPE http_requests_total counter"]
    for path, count in request_counter.items():
        lines.append(f'http_requests_total{{path="{path}"}} {count}')
    lines.extend(["# HELP http_request_latency_ms Total de latência acumulada", "# TYPE http_request_latency_ms counter"])
    for path, total_ms in latency_histogram.items():
        lines.append(f'http_request_latency_ms{{path="{path}"}} {total_ms}')
    lines.extend(["# HELP http_rate_limit_hits_total Total de bloqueios por rate limit", "# TYPE http_rate_limit_hits_total counter"])
    for path, hits in rate_limit_hits.items():
        lines.append(f'http_rate_limit_hits_total{{path="{path}"}} {hits}')
    return "\n".join(lines)
