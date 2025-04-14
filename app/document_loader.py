# app/document_loader.py

from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from pathlib import Path
import os

def load_documents(directory: str = "data/docs"):
    docs = []
    for file_path in Path(directory).glob("*"):
        if file_path.suffix == ".txt":
            loader = TextLoader(str(file_path))
            docs.extend(loader.load())
        elif file_path.suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
            docs.extend(loader.load())
        # Outros formatos podem ser adicionados aqui futuramente
    return docs

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(documents)

def create_vectorstore(documents, persist_directory: str = "data/vectorstore"):
    embeddings = OpenAIEmbeddings()  # Certifique-se de ter sua chave de API
    vectordb = FAISS.from_documents(documents, embeddings)
    vectordb.save_local(persist_directory)
    return vectordb

def load_vectorstore(persist_directory: str = "data/vectorstore"):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(persist_directory, embeddings)
