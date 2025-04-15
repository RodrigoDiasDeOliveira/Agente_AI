from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import UnstructuredPDFLoader  # Alterado de PDFPlumberLoader
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import DOCS_PATH, VECTORSTORE_PATH
import os

# Verificar se o arquivo existe
if not os.path.exists(DOCS_PATH):
    raise FileNotFoundError(f"O arquivo {DOCS_PATH} não foi encontrado.")

# Criar diretório para o vectorstore, se não existir
if not os.path.exists(VECTORSTORE_PATH):
    os.makedirs(VECTORSTORE_PATH)

# Carregar documentos
try:
    loader = UnstructuredPDFLoader(DOCS_PATH, mode="elements", strategy="hi_res")  # Alterado para UnstructuredPDFLoader
    documents = loader.load()
    if not documents:
        raise ValueError("Nenhum documento foi carregado.")
    print(f"Carregadas {len(documents)} páginas do PDF")
    for i, doc in enumerate(documents):
        content_preview = doc.page_content[:200].replace('\n', ' ') if doc.page_content else "Nenhum conteúdo"
        print(f"Página {i+1}: {content_preview}...")
except Exception as e:
    raise Exception(f"Erro ao carregar documentos: {e}")

# Carregar os embeddings
try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
except Exception as e:
    raise Exception(f"Erro ao configurar embeddings: {e}")

# Criar a vectorstore
try:
    vectordb = FAISS.from_documents(documents, embeddings)
    print("Índice FAISS criado com sucesso!")
except Exception as e:
    raise Exception(f"Erro ao criar o índice FAISS: {e}")

# Salvar o índice FAISS
try:
    vectordb.save_local(VECTORSTORE_PATH)
    print(f"Índice FAISS salvo em {VECTORSTORE_PATH}/index.faiss")
except Exception as e:
    raise Exception(f"Erro ao salvar o índice FAISS: {e}")