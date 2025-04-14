from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import DOCS_PATH, VECTORSTORE_PATH
import os

def load_and_vectorize():
    if not os.path.exists(DOCS_PATH):
        raise FileNotFoundError(f"O arquivo {DOCS_PATH} não foi encontrado.")
    os.makedirs(VECTORSTORE_PATH, exist_ok=True)
    loader = PDFPlumberLoader(DOCS_PATH)
    documents = loader.load()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(documents, embeddings)
    vectordb.save_local(VECTORSTORE_PATH)
    print(f"Índice salvo em {VECTORSTORE_PATH}/index.faiss")