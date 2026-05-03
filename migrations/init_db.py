# migrations/init_db.py
from sqlalchemy import create_engine
from app.config import DATABASE_URL
from app.models import Base

def init_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("✅ Banco de dados e tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_database()
