# app/feedback_handler.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from datetime import datetime
from .config import DATABASE_URL
from .models import Feedback

class FeedbackHandler:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)

    def record_feedback(self, query: str, target_id: str = None, 
                       similarity: float = 0.0, feedback_type: str = "positive", 
                       comment: str = ""):
        """
        Registra feedback do usuário
        feedback_type: "positive", "negative", "ignored"
        """
        session = self.Session()
        
        feedback = Feedback(
            query=query,
            target_id=target_id,
            similarity=similarity,
            feedback_type=feedback_type,
            comment=comment,
            created_at=datetime.utcnow()
        )
        
        session.add(feedback)
        session.commit()
        session.close()
        
        print(f"✅ Feedback registrado: {feedback_type} para '{query[:50]}...'")
        return True

    def get_recent_feedback(self, limit: int = 20):
        """Retorna feedbacks recentes para análise"""
        session = self.Session()
        result = session.execute(text("""
            SELECT id, query, target_id, similarity, feedback_type, comment, created_at
            FROM feedback
            ORDER BY created_at DESC
            LIMIT :limit
        """), {"limit": limit})
        
        feedbacks = [dict(row) for row in result]
        session.close()
        return feedbacks

    def get_feedback_stats(self):
        """Estatísticas de feedback"""
        session = self.Session()
        result = session.execute(text("""
            SELECT 
                feedback_type,
                COUNT(*) as count,
                AVG(similarity) as avg_similarity
            FROM feedback
            GROUP BY feedback_type
        """))
        
        stats = {}
        for row in result:
            stats[row.feedback_type] = {
                "count": row.count,
                "avg_similarity": float(row.avg_similarity) if row.avg_similarity else 0
            }
        session.close()
        return stats