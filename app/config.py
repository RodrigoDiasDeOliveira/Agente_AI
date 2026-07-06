from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/appdb",
)
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
MODEL_NAME = os.getenv("MODEL_NAME", "distilgpt2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH", "./data/vectorstore")
DOCS_PATH = os.getenv("DOCS_PATH", "./data/docs")
VITE_API_BASE_URL = os.getenv("VITE_API_BASE_URL", "http://localhost:8000")
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
    if origin.strip()
]
ADMIN_API_TOKEN = os.getenv("ADMIN_API_TOKEN", "changeme")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "huggingface")

if not HUGGINGFACEHUB_API_TOKEN:
    print("Aviso: HUGGINGFACEHUB_API_TOKEN não definido. Usando modelo público.")