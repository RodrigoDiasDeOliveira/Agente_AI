import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    DOCS_PATH = os.getenv("DOCS_PATH", "./data/docs")

settings = Settings()
