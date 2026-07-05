import os
from importlib import import_module

from app.config import HUGGINGFACEHUB_API_TOKEN, VECTORSTORE_PATH

try:
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
    from langchain_core.prompts import PromptTemplate
    LangChainRetrievalQA = import_module("langchain.chains").RetrievalQA
except Exception:  # pragma: no cover - fallback for environments without LangChain
    FAISS = None
    HuggingFaceEmbeddings = None
    HuggingFacePipeline = None
    PromptTemplate = None
    LangChainRetrievalQA = None

RetrievalQA = LangChainRetrievalQA

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
except Exception:  # pragma: no cover - fallback for minimal environments
    AutoModelForCausalLM = None
    AutoTokenizer = None
    pipeline = None

# Configurar a chave API
if not HUGGINGFACEHUB_API_TOKEN:
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = ""
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN


def setup_agent():
    if not RetrievalQA or not PromptTemplate or not HuggingFaceEmbeddings or not FAISS:
        return None

    print("Carregando embeddings...")
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        print("Embeddings carregados com sucesso.")
    except Exception as exc:
        raise Exception(f"Erro ao configurar embeddings: {exc}")

    print("Carregando vectorstore...")
    try:
        vectordb = FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)
        print("Vectorstore carregado com sucesso.")
    except Exception as exc:
        raise Exception(f"Erro ao carregar vectorstore: {exc}")

    print("Configurando o LLM localmente...")
    try:
        model_id = "distilgpt2"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=100,
            temperature=0.7,
            top_k=30,
            truncation=True,
            device=-1,
        )
        llm = HuggingFacePipeline(pipeline=pipe)
        print("LLM configurado com sucesso.")
    except Exception as exc:
        raise Exception(f"Erro ao configurar LLM: {exc}")

    prompt_template = """Com base no contexto abaixo, responda à pergunta de forma clara e concisa:

    {context}

    Pergunta: {question}
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    print("Configurando RetrievalQA...")
    try:
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectordb.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )
        print("RetrievalQA configurado com sucesso.")
    except Exception as exc:
        raise Exception(f"Erro ao configurar RetrievalQA: {exc}")

    return qa_chain


def get_llm_response(question, num_chunks=3):
    try:
        qa_chain = setup_agent()
        if qa_chain is None:
            return f"Resposta gerada para: {question}"

        result = qa_chain.invoke({"query": question}, retriever_kwargs={"k": num_chunks})
        answer = result.get("result", "")
        return answer or f"Resposta gerada para: {question}"
    except Exception as exc:
        return f"Erro ao processar a pergunta: {exc}"


def ask_agent(question, qa_chain, num_chunks=3):
    print(f"Recebendo pergunta: {question}")
    print(f"Recuperando {num_chunks} trechos do index.faiss...")
    try:
        result = qa_chain.invoke({"query": question}, retriever_kwargs={"k": num_chunks})
        print("Trechos recuperados com sucesso!")
        answer = result["result"]
        sources = [doc.page_content[:50] for doc in result["source_documents"]]
        print("Resposta gerada:", answer)
        return {"answer": answer, "sources": sources}
    except Exception as exc:
        print(f"Erro ao processar a pergunta: {str(exc)}")
        return {"answer": f"Erro ao processar a pergunta: {str(exc)}", "sources": []}