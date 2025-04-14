from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
import os

# Configurações
DOCS_PATH = "data/docs/documento.txt"  # Caminho correto para o documento
VECTORSTORE_DIR = "data/vectorstore"  # Diretório onde o index.faiss será salvo

# Verificar se o arquivo existe
if not os.path.exists(DOCS_PATH):
    raise FileNotFoundError(f"O arquivo {DOCS_PATH} não foi encontrado.")

# Criar diretório para o vectorstore, se não existir
if not os.path.exists(VECTORSTORE_DIR):
    os.makedirs(VECTORSTORE_DIR)

# Carregar documentos
try:
    loader = TextLoader(DOCS_PATH)
    documents = loader.load()
    if not documents:
        raise ValueError("Nenhum documento foi carregado.")
except Exception as e:
    raise Exception(f"Erro ao carregar documentos: {e}")

# Carregar os embeddings (usando Hugging Face)
try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
except Exception as e:
    raise Exception(f"Erro ao configurar embeddings: {e}")

# Criar a vectorstore (FAISS) a partir dos documentos
try:
    vectordb = FAISS.from_documents(documents, embeddings)
    print("Índice FAISS criado com sucesso!")
except Exception as e:
    raise Exception(f"Erro ao criar o índice FAISS: {e}")

# Salvar o índice FAISS
try:
    vectordb.save_local(VECTORSTORE_DIR)
    print(f"Índice FAISS salvo em {VECTORSTORE_DIR}/index.faiss")
except Exception as e:
    raise Exception(f"Erro ao salvar o índice FAISS: {e}")