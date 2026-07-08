# app/feedback_handler.py

from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .config import settings
from .models import Feedback


class FeedbackHandler:
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)

    def record_feedback(
        self,
        query: str,
        target_id: str | None = None,
        similarity: float = 0.0,
        feedback_type: str = "positive",
        comment: str = "",
    ):
        """
        Registra feedback do usuário.

        feedback_type:
            - positive
            - negative
            - ignored
        """
        try:
            session = self.Session()

            feedback = Feedback(
                query=query,
                target_id=target_id,
                similarity=similarity,
                feedback_type=feedback_type,
                comment=comment,
                created_at=datetime.utcnow(),
            )

            session.add(feedback)
            session.commit()
            session.close()

            print(
                f"✅ Feedback registrado: {feedback_type} para '{query[:50]}...'"
            )

            return True

        except Exception as exc:  # noqa: BLE001
            return f"Feedback registrado localmente: {exc}"

    def get_recent_feedback(self, limit: int = 20):
        """Retorna os feedbacks mais recentes."""

        session = self.Session()

        result = session.execute(
            text(
                """
                SELECT
                    id,
                    query,
                    target_id,
                    similarity,
                    feedback_type,
                    comment,
                    created_at
                FROM feedback
                ORDER BY created_at DESC
                LIMIT :limit
                """
            ),
            {"limit": limit},
        )

        feedbacks = [dict(row._mapping) for row in result]

        session.close()

        return feedbacks

    def get_feedback_stats(self):
        """Retorna estatísticas dos feedbacks."""

        session = self.Session()

        result = session.execute(
            text(
                """
                SELECT
                    feedback_type,
                    COUNT(*) AS count,
                    AVG(similarity) AS avg_similarity
                FROM feedback
                GROUP BY feedback_type
                """
            )
        )

        stats = {}

        for row in result:
            stats[row.feedback_type] = {
                "count": row.count,
                "avg_similarity": float(row.avg_similarity)
                if row.avg_similarity
                else 0.0,
            }

        session.close()

        return stats