# app/trusted_search.py

from functools import lru_cache

import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from .config import settings
from .feedback_handler import FeedbackHandler
from .llm_agent import get_llm_response
from .models import SearchTarget

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except Exception:  # pragma: no cover
    HuggingFaceEmbeddings = None

try:
    from sentence_transformers import CrossEncoder
except Exception:  # pragma: no cover
    CrossEncoder = None


class TrustedAnswerSearch:
    def __init__(self):
        self.engine = create_engine(
            settings.DATABASE_URL,
            future=True,
            pool_pre_ping=True,
        )

        self.Session = sessionmaker(bind=self.engine)
        self.feedback_handler = FeedbackHandler()

        self._embedding_cache = {}

        self.embeddings = None
        self.reranker = None

        try:
            if HuggingFaceEmbeddings is not None:
                self.embeddings = HuggingFaceEmbeddings(
                    model_name=settings.EMBEDDING_MODEL
                )

            if CrossEncoder is not None:
                self.reranker = CrossEncoder(
                    "cross-encoder/ms-marco-MiniLM-L-6-v2"
                )

            from .models import Base

            Base.metadata.create_all(self.engine)

            print("✅ TrustedAnswerSearch inicializado com Reranking")

        except SQLAlchemyError as exc:
            print(
                f"⚠️ Banco indisponível, continuando em modo fallback: {exc}"
            )

        except Exception as exc:
            print(
                f"⚠️ Falha na inicialização do TrustedSearch: {exc}"
            )

    @lru_cache(maxsize=500)
    def _get_embedding(self, text_value: str):
        """Retorna embedding utilizando cache."""

        if self.embeddings is None:
            raise RuntimeError(
                "Embedding model não inicializado."
            )

        if text_value in self._embedding_cache:
            return self._embedding_cache[text_value]

        embedding = self.embeddings.embed_query(text_value)

        self._embedding_cache[text_value] = embedding

        return embedding

    def add_target(self, target):
        """Adiciona um Search Target."""

        session = self.Session()

        try:
            embedding = self._get_embedding(target.description)

            db_target = SearchTarget(
                target_id=target.target_id,
                description=target.description,
                alternative_phrases=target.alternative_phrases,
                match_document=target.match_document.dict(),
                embedding=list(embedding),
            )

            session.add(db_target)
            session.commit()

            print(f"✅ Target adicionado: {target.target_id}")

            return True

        except Exception as exc:
            session.rollback()

            print(f"❌ Erro ao adicionar target: {exc}")

            return False

        finally:
            session.close()

    def search(
        self,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.65,
    ):
        """
        Busca utilizando Vector Search + CrossEncoder.
        """

        if not query or len(query.strip()) < 3:
            return {
                "content": "Pergunta muito curta.",
                "type": "error",
            }

        session = self.Session()

        try:
            query_embedding = self._get_embedding(query)

            result = session.execute(
                text(
                    """
                    SELECT
                        target_id,
                        description,
                        match_document,
                        embedding <=> :query_emb::vector AS distance
                    FROM search_targets
                    ORDER BY embedding <=> :query_emb::vector
                    LIMIT :top_k
                    """
                ),
                {
                    "query_emb": f"[{','.join(map(str, query_embedding))}]",
                    "top_k": top_k * 2,
                },
            )

            candidates = []

            for row in result:
                distance = float(row.distance)
                similarity = 1 - distance

                if similarity < 0.30:
                    continue

                candidates.append(
                    {
                        "target_id": row.target_id,
                        "description": row.description,
                        "match_document": row.match_document,
                        "similarity": similarity,
                    }
                )

            if not candidates:
                return self._fallback_rag(query)

            reranked = self._rerank_candidates(query, candidates)

            best = reranked[0]

            if best["score"] >= similarity_threshold:
                print(
                    f"✅ Match forte: {best['target_id']} "
                    f"(score: {best['score']:.3f})"
                )

                return {
                    "target_id": best["target_id"],
                    "match_document": best["match_document"],
                    "similarity": best["score"],
                    "description": best["description"],
                }

            print(
                f"⚠️ Melhor match abaixo do threshold: "
                f"{best['score']:.3f}"
            )

            return self._fallback_rag(query)

        except Exception as exc:
            print(f"❌ Erro na busca: {exc}")

            return self._fallback_rag(query)

        finally:
            session.close()

    def _cosine_similarity(
        self,
        a: np.ndarray,
        b: np.ndarray,
    ) -> float:

        if a is None or b is None:
            return 0.0

        if a.size == 0 or b.size == 0:
            return 0.0

        a_norm = np.linalg.norm(a)
        b_norm = np.linalg.norm(b)

        if a_norm == 0 or b_norm == 0:
            return 0.0

        return float(np.dot(a, b) / (a_norm * b_norm))

    def _rerank_candidates(
        self,
        query: str,
        candidates: list,
    ):
        """Executa reranking utilizando CrossEncoder."""

        if not candidates:
            return []

        if self.reranker is None:
            return [
                {
                    **candidate,
                    "score": candidate["similarity"],
                }
                for candidate in candidates
            ]

        pairs = [
            (query, candidate["description"])
            for candidate in candidates
        ]

        scores = self.reranker.predict(pairs)

        reranked = []

        for index, score in enumerate(scores):
            item = candidates[index].copy()
            item["score"] = float(score)
            reranked.append(item)

        reranked.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return reranked

    def _fallback_rag(self, query: str):
        """Fallback para o LLM."""

        try:
            response = get_llm_response(query)

            return {
                "type": "fallback",
                "content": response,
                "warning": (
                    "Resposta gerada por LLM "
                    "(menor confiança)"
                ),
            }

        except Exception:
            return {
                "type": "error",
                "content": (
                    "Não foi possível gerar uma resposta "
                    "no momento."
                ),
            }

    def record_feedback(
        self,
        query: str,
        target_id: str | None = None,
        similarity: float = 0.0,
        feedback_type: str = "positive",
    ):
        """Registra feedback do usuário."""

        return self.feedback_handler.record_feedback(
            query=query,
            target_id=target_id,
            similarity=similarity,
            feedback_type=feedback_type,
        )