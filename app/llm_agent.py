from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.prompts import PromptTemplate
from langchain.schema import BaseRetriever

from app.config import settings

# Inicializar modelo de embeddings
embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

# Caminho do vectorstore
VECTORSTORE_PATH = settings.DOCS_PATH + "/../vectorstore"



# Carregar o FAISS vectorstore
vectordb = FAISS.load_local(VECTORSTORE_PATH, embeddings, allow_dangerous_deserialization=True)

# Criar o retriever (quem faz a busca nos documentos)
retriever: BaseRetriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Modelo de linguagem
llm = ChatOpenAI(temperature=0, openai_api_key=settings.OPENAI_API_KEY, model_name=settings.MODEL_NAME)

# (Opcional) Custom prompt
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Você é um assistente de IA treinado com base nos documentos da empresa.
Com base no conteúdo abaixo, responda à pergunta de forma clara e objetiva.

Contexto:
{context}

Pergunta:
{question}

Resposta:"""
)

# Criar a cadeia QA com recuperação + LLM
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=True
)

def ask_agent(question: str) -> str:
    """
    Recebe uma pergunta e retorna a resposta gerada pela IA com base nos documentos.
    """
    result = qa_chain({"query": question})
    answer = result["result"]
    return answer
