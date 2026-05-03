# app/trusted_search.py
import json
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder
import numpy as np
from functools import lru_cache
from .config import DATABASE_URL
from .models import SearchTarget
from .llm_agent import get_llm_response
from .feedback_handler import FeedbackHandler

class TrustedAnswerSearch:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Reranker (CrossEncoder) - muito mais preciso
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        
        self.feedback_handler = FeedbackHandler()
        
        # Cache simples
        self._embedding_cache = {}
        
        # Criar tabelas
        from .models import Base
        Base.metadata.create_all(self.engine)
        
        print("✅ TrustedAnswerSearch inicializado com Reranking")

    @lru_cache(maxsize=500)
    def _get_embedding(self, text: str):
        """Cache de embeddings"""
        if text in self._embedding_cache:
            return self._embedding_cache[text]
        emb = self.embeddings.embed_query(text)
        self._embedding_cache[text] = emb
        return emb

    def add_target(self, target):
        """Adiciona um Search Target"""
        session = self.Session()
        try:
            embedding = self._get_embedding(target.description)
            
            db_target = SearchTarget(
                target_id=target.target_id,
                description=target.description,
                alternative_phrases=target.alternative_phrases,
                match_document=target.match_document.dict(),
                embedding=list(embedding)
            )
            session.add(db_target)
            session.commit()
            print(f"✅ Target adicionado: {target.target_id}")
            return True
        except Exception as e:
            session.rollback()
            print(f"❌ Erro ao adicionar target: {e}")
            return False
        finally:
            session.close()

    def search(self, query: str, top_k: int = 5, similarity_threshold: float = 0.65):
        """
        Busca com Reranking
        """
        if not query or len(query.strip()) < 3:
            return {"content": "Pergunta muito curta.", "type": "error"}

        session = self.Session()
        try:
            query_embedding = self._get_embedding(query)

            # 1. Recuperação inicial (Vector Search)
            result = session.execute(text("""
                SELECT 
                    target_id,
                    description,
                    match_document,
                    embedding <=> :query_emb::vector as distance
                FROM search_targets
                ORDER BY embedding <=> :query_emb::vector
                LIMIT :top_k
            """), {
                "query_emb": f"[{','.join(map(str, query_embedding))}]",
                "top_k": top_k * 2  # Busca mais resultados para reranking
            })

            candidates = []
            for row in result:
                distance = float(row.distance)
                similarity = 1 - distance
                if similarity < 0.3:  # filtro inicial baixo
                    continue
                    
                candidates.append({
                    "target_id": row.target_id,
                    "description": row.description,
                    "match_document": row.match_document,
                    "similarity": similarity
                })

            if not candidates:
                return self._fallback_rag(query)

            # 2. Reranking com CrossEncoder (mais preciso)
            reranked = self._rerank_candidates(query, candidates)
            
            # Pega o melhor após reranking
            best = reranked[0]
            
            if best["score"] >= similarity_threshold:
                print(f"✅ Match forte: {best['target_id']} (score: {best['score']:.3f})")
                return {
                    "target_id": best["target_id"],
                    "match_document": best["match_document"],
                    "similarity": best["score"],
                    "description": best["description"]
                }
            else:
                print(f"⚠️  Melhor match abaixo do threshold: {best['score']:.3f}")
                return self._fallback_rag(query)

        except Exception as e:
            print(f"❌ Erro na busca: {e}")
            return self._fallback_rag(query)
        finally:
            session.close()

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        if a is None or b is None or a.size == 0 or b.size == 0:
            return 0.0
        a_norm = np.linalg.norm(a)
        b_norm = np.linalg.norm(b)
        if a_norm == 0 or b_norm == 0:
            return 0.0
        return float(np.dot(a, b) / (a_norm * b_norm))

    def _rerank_candidates(self, query: str, candidates: list):
        """Reranking com CrossEncoder"""
        if not candidates:
            return []

        # Prepara pares para reranking (query + document)
        pairs = [(query, cand["description"]) for cand in candidates]
        
        # Calcula scores
        scores = self.reranker.predict(pairs)
        
        # Combina resultados
        reranked = []
        for i, score in enumerate(scores):
            item = candidates[i].copy()
            item["score"] = float(score)
            reranked.append(item)
        
        # Ordena por score do reranker
        reranked.sort(key=lambda x: x["score"], reverse=True)
        return reranked

    def _fallback_rag(self, query: str):
        """Fallback para o sistema RAG antigo"""
        try:
            response = get_llm_response(query)
            return {
                "type": "fallback",
                "content": response,
                "warning": "Resposta gerada por LLM (menor confiança)"
            }
        except Exception:
            return {
                "type": "error",
                "content": "Não foi possível gerar uma resposta no momento."
            }

    def record_feedback(self, query: str, target_id: str = None, 
                       similarity: float = 0.0, feedback_type: str = "positive"):
        """Registra feedback"""
        return self.feedback_handler.record_feedback(
            query=query,
            target_id=target_id,
            similarity=similarity,
            feedback_type=feedback_type
        )