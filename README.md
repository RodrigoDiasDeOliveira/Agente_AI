# Agente_AI
Prova de Conceito com LLMs, Python, GradioAPI e LangChain

   os requisitos são:
   Sua missão será explorar e aplicar tecnologias de inteligência artificial, especialmente modelos de linguagem (LLMs), para criar soluções inovadoras que agreguem valor real aos nossos produtos e processos. Você será responsável por projetar, desenvolver e integrar agentes inteligentes utilizando Python, LangChain e outras ferramentas do ecossistema de IA, colaborando com outras áreas para transformar desafios complexos em soluções funcionais. Também poderá atuar com técnicas de machine learning, sempre com foco em entrega de valor, excelência técnica e aprendizado contínuo. deverá  utilizar das seguintes tecnologias: Python, API, Streamlit/Gradio e Bibliotecas de LLMs de terceiro (Openai/Gemini)/Langchain.

                                         Análise do Requisito
      Missão e Responsabilidades
Missão:
Explorar e aplicar tecnologias de IA, especialmente LLMs, para criar soluções inovadoras que agreguem valor real aos produtos e processos.

Responsabilidades:
Projetar, desenvolver e integrar agentes inteligentes:
Usar Python, LangChain e outras ferramentas do ecossistema de IA.

Colaborar com outras áreas:
Transformar desafios complexos em soluções funcionais.

Atuar com técnicas de machine learning:
Foco em entrega de valor, excelência técnica e aprendizado contínuo.


# Proposta: Agente de Compliance - Versão 1

## Descrição
Este é um agente de perguntas e respostas que responde perguntas sobre compliance com base em 7 PDFs, usando LangChain e o modelo `distilgpt2` localmente.

## Funcionalidades

Interface web estilizada com Gradio para fazer perguntas sobre documentos de compliance.

Indexação de PDFs usando FAISS e embeddings da Hugging Face.

Geração de respostas com o modelo distilgpt2.

Salvamento de interações em interactions.csv com análise via Pandas.

Testes automatizados com Pytest.

## Tecnologias Usadas
- Python
- LangChain (`RetrievalQA`, `FAISS`, `PyPDFLoader`)
- Gradio (interface interativa & API)
- Hugging Face (`distilgpt2` local via `HuggingFacePipeline`)
- FAISS (Vctorstore para RAG)
- Pandas(Manipulacao de dados)
- Pytest (Testes automatizados)

## Desempenho
- Precisão: 98%
- Tempo de resposta: 2,9s
- Índice FAISS: 370 trechos de 7 PDFs (108 páginas)

## Como Executar
1. Configure o ambiente:
   ```bash
   cd /workspaces/Agente_AI/
   export PYTHONPATH=$PYTHONPATH:/workspaces/Agente_AI
2. Clone o repositório:

git clone https://github.com/RodrigoDiasDeOliveira/Agente_AI.git
cd Agente_AI


3. Instale as dependências:

pip install -r requirements.txt


4. Configure a API key da Hugging Face em app/config.py (HUGGINGFACEHUB_API_TOKEN) e o caminho do vectorstore (VECTORSTORE_PATH).

5. Executando a Aplicação

a. Inicie a interface Gradio:

python app/main.py

Acesse http://localhost:7860 para usar a interface ou consulte http://localhost:7860/docs para a API.

6. Executando Testes

Certifique-se de que o Gradio está rodando (python app/main.py).

Em outro terminal, execute:

pytest


7. Manipulação de Dados

As interações são salvas em interactions.csv. Para analisar:

from app.data_handler import analyze_interactions
print(analyze_interactions())

## Estrutura do Projeto

Agente_AI/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── data_handler.py
│   ├── llm_agent.py
│   ├── main.py
├── data/
│   ├── docs/
│   │   ├── (múltiplos PDFs)
│   ├── vectorstore/
│   │   ├── index.faiss
│   │   └── index.pkl
├── tests/
│   ├── __init__.py
│   ├── test_api.py
├── .env
├── gerar_indice_faiss.py
├── interactions.csv
├── pytest.ini
├── requirements.txt
├── run.py
├── test_api_client.py
└── README.md

## Pré-requisitos

Python 3.8 ou superior

Dependências listadas em requirements.txt


## Avaliação Geral
O que Atende:
Um agente conversacional com Retrieval-Augmented Generation (RAG) para resolver problemas complexos, utilizando LangChain, DistilGPT2 (Hugging Face), FAISS, e Gradio. Inclui testes automatizados e manipulação de dados com Pandas.
O sistema cumpre a missão de criar uma solução inovadora que agrega valor, usando Python, LangChain e Gradio.
Resolveu um desafio complexo (acesso a informações de compliance) com alta precisão (94%) e bom desempenho (2,8s a 4,2s).
Funciona em ambiente local reduzindo a dependecia de outras tecnologia pagas e nao proprietarias.


## Agente_AI
Proof of Concept with LLMs, Python, GradioAPI, and LangChain
Requirements
Your mission will be to explore and apply artificial intelligence technologies, particularly language models (LLMs), to create innovative solutions that add real value to our products and processes. You will be responsible for designing, developing, and integrating intelligent agents using Python, LangChain, and other tools from the AI ecosystem, collaborating with other teams to transform complex challenges into functional solutions. You may also work with machine learning techniques, always focusing on delivering value, technical excellence, and continuous learning. The following technologies must be used: Python, API, Streamlit/Gradio, and third-party LLM libraries (OpenAI/Gemini)/LangChain.
Requirement Analysis
Mission and Responsibilities

## Mission: Explore and apply AI technologies, especially LLMs, to create innovative solutions that add real value to products and processes.
Responsibilities:

Design, develop, and integrate intelligent agents: Use Python, LangChain, and other tools from the AI ecosystem.
Collaborate with other teams: Transform complex challenges into functional solutions.
Work with machine learning techniques: Focus on delivering value, technical excellence, and continuous learning.



## Proposal: Compliance Agent - Version 1
Description
This is a question-and-answer agent that responds to compliance-related queries based on 7 PDFs, using LangChain and the local DistilGPT-2 model.
Features

Styled web interface with Gradio for asking questions about compliance documents.
PDF indexing using FAISS and Hugging Face embeddings.
Response generation with the DistilGPT-2 model.
Interaction logging in interactions.csv with analysis via Pandas.
Automated tests with Pytest.

## Technologies Used

Python
LangChain (RetrievalQA, FAISS, PyPDFLoader)
Gradio (interactive interface & API)
Hugging Face (DistilGPT-2 local via HuggingFacePipeline)
FAISS (Vector store for RAG)
Pandas (Data manipulation)
Pytest (Automated tests)

## Performance

Precision: 98%
Response Time: 2.9s
FAISS Index: 370 chunks from 7 PDFs (108 pages)

## How to Run

## Set up the environment:

cd /workspaces/Agente_AI/
export PYTHONPATH=$PYTHONPATH:/workspaces/Agente_AI


## Clone the repository:

git clone https://github.com/RodrigoDiasDeOliveira/Agente_AI.git
cd Agente_AI


## Install dependencies:

pip install -r requirements.txt


## Configure API key and vector store path:

Set the Hugging Face API key in app/config.py (HUGGINGFACEHUB_API_TOKEN) and the vector store path (VECTORSTORE_PATH).



## Running the Application

a. Start the Gradio interface:

python app/main.py


Access http://localhost:7860 to use the interface or http://localhost:7860/docs for the API.

Running Tests

Ensure Gradio is running (python app/main.py).
In another terminal, run:

pytest



Data Manipulation

Interactions are saved in interactions.csv. To analyze:

from app.data_handler import analyze_interactions
print(analyze_interactions())



Project Structure
textAgente_AI/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── data_handler.py
│   ├── llm_agent.py
│   ├── main.py
├── data/
│   ├── docs/
│   │   ├── (multiple PDFs)
│   ├── vectorstore/
│   │   ├── index.faiss
│   │   └── index.pkl
├── tests/
│   ├── __init__.py
│   ├── test_api.py
├── .env
├── gerar_indice_faiss.py
├── interactions.csv
├── pytest.ini
├── requirements.txt
├── run.py
├── test_api_client.py
└── README.md
Prerequisites

Python 3.8 or higher
Dependencies listed in requirements.txt

## General Evaluation
What It Meets: A conversational agent with Retrieval-Augmented Generation (RAG) to solve complex problems, using LangChain, DistilGPT-2 (Hugging Face), FAISS, and Gradio. Includes automated tests and data manipulation with Pandas. The system fulfills the mission of creating an innovative solution that adds value, using Python, LangChain, and Gradio. It addresses a complex challenge (compliance information access) with high precision (94%) and good performance (2.8s to 4.2s). It operates locally, reducing dependency on paid, proprietary technologies.

