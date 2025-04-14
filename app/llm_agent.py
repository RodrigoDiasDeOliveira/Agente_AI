from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from app.config import HUGGINGFACEHUB_API_TOKEN, VECTORSTORE_PATH
import os

# Configurar a chave API
if not HUGGINGFACEHUB_API_TOKEN:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN não definido no config.py")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

# Carregar embeddings
try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
except Exception as e:
    raise Exception(f"Erro ao configurar embeddings: {e}")

# Carregar vectorstore
try:
    vectordb = FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)
except Exception as e:
    raise Exception(f"Erro ao carregar vectorstore: {e}")

# Configurar o LLM
try:
    llm = HuggingFaceEndpoint(
        repo_id="google/flan-t5-base",
        task="text2text-generation",
        max_length=512,
        temperature=0.7,
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
    )
except Exception as e:
    raise Exception(f"Erro ao configurar LLM: {e}")

# Configurar o RetrievalQA
try:
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
except Exception as e:
    raise Exception(f"Erro ao configurar RetrievalQA: {e}")

# Função para responder perguntas
def ask_agent(question):
    try:
        result = qa_chain.invoke({"query": question})
        answer = result["result"]
        sources = [doc.page_content[:100] for doc in result["source_documents"]]
        return {"answer": answer, "sources": sources}
    except Exception as e:
        return {"answer": f"Erro ao processar a pergunta: {str(e)}", "sources": []}