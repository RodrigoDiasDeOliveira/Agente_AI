from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/appdb"

    HUGGINGFACEHUB_API_TOKEN: str = ""

    MODEL_NAME: str = "distilgpt2"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    VECTORSTORE_PATH: str = "./data/vectorstore"

    DOCS_PATH: str = "./data/docs"

    VITE_API_BASE_URL: str = "http://localhost:8000"

    ADMIN_API_TOKEN: str = "changeme"

    LLM_PROVIDER: str = "huggingface"

    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()

if not settings.HUGGINGFACEHUB_API_TOKEN:
    print("Aviso: HUGGINGFACEHUB_API_TOKEN não definido. Usando modelo público.")
