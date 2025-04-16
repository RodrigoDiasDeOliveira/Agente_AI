from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import VECTORSTORE_PATH
import os

# Lista de caminhos dos PDFs
PDF_FILES = [
    "data/docs/Codigo-de-Conduta-Etica.pdf",
    "data/docs/Guia 4 - PMEs.pdf",
    "data/docs/Comunicado_brinde_assinado.pdf",
    "data/docs/Política Anticorrupção do Sistema FIESC.pdf",
    "data/docs/Politica-de-conflito-de-interesses.pdf",
    "data/docs/Política de Ética e Compliance da FIESC e suas Entidades.pdf",
    "data/docs/Relatório Sintético 2023 - Programa de Compliance_site.pdf"
]

# Carregar todos os PDFs
print("Carregando os PDFs...")
all_documents = []
for pdf_path in PDF_FILES:
    if not os.path.exists(pdf_path):
        print(f"Arquivo não encontrado: {pdf_path}")
        continue
    print(f"Carregando {pdf_path}...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    all_documents.extend(documents)
print(f"Total de documentos carregados: {len(all_documents)}")

# Dividir o texto em trechos
print("Dividindo os documentos em trechos...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.split_documents(all_documents)
print(f"Total de trechos criados: {len(docs)}")

# Criar embeddings
print("Criando embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Criar e salvar o índice FAISS
print("Criando o índice FAISS...")
vectordb = FAISS.from_documents(docs, embeddings)
vectordb.save_local(VECTORSTORE_PATH)
print("Índice FAISS criado e salvo com sucesso.")
