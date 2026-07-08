from sqlalchemy import create_engine, text

from app.config import settings
from app.models import Base


def init_database():
    engine = create_engine(settings.DATABASE_URL)

    with engine.begin() as connection:
        if settings.DATABASE_URL.lower().startswith(
            ("postgresql", "postgres")
        ):
            connection.execute(
                text("CREATE EXTENSION IF NOT EXISTS vector")
            )

    Base.metadata.create_all(engine)

    print("✅ Banco de dados e tabelas criadas com sucesso!")


if __name__ == "__main__":
    init_database()
