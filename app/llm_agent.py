from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.config import HUGGINGFACEHUB_API_TOKEN, VECTORSTORE_PATH
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import os

# Configurar a chave API
if not HUGGINGFACEHUB_API_TOKEN:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN não definido no config.py")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

print("Carregando embeddings...")
try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("Embeddings carregados com sucesso.")
except Exception as e:
    raise Exception(f"Erro ao configurar embeddings: {e}")

print("Carregando vectorstore...")
try:
    vectordb = FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)
    print("Vectorstore carregado com sucesso.")
except Exception as e:
    raise Exception(f"Erro ao carregar vectorstore: {e}")

print("Configurando o LLM localmente...")
try:
    model_id = "distilgpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=32,  # Aumentado de 16 para 32
        temperature=0.7,
        top_k=30,
        truncation=True,
        device=-1
    )
    llm = HuggingFacePipeline(pipeline=pipe)
    print("LLM configurado com sucesso.")
except Exception as e:
    raise Exception(f"Erro ao configurar LLM: {e}")

# Criar um PromptTemplate personalizado
prompt_template = """Com base no contexto abaixo, responda à pergunta de forma clara e concisa:

{context}

Pergunta: {question}
"""
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

print("Configurando RetrievalQA...")
try:
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    print("RetrievalQA configurado com sucesso.")
except Exception as e:
    raise Exception(f"Erro ao configurar RetrievalQA: {e}")

def ask_agent(question, num_chunks=3):
    print(f"Recebendo pergunta: {question}")
    print(f"Recuperando {num_chunks} trechos do index.faiss...")
    try:
        result = qa_chain.invoke({"query": question}, retriever_kwargs={"k": num_chunks})
        print("Trechos recuperados com sucesso!")
        answer = result["result"]
        sources = [doc.page_content[:50] for doc in result["source_documents"]]
        print("Resposta gerada:", answer)
        return {"answer": answer, "sources": sources}
    except Exception as e:
        print(f"Erro ao processar a pergunta: {str(e)}")
        return {"answer": f"Erro ao processar a pergunta: {str(e)}", "sources": []}