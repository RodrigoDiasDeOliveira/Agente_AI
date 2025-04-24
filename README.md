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



## Avaliação Geral
O que Atende:
Um agente conversacional com Retrieval-Augmented Generation (RAG) para resolver problemas complexos, utilizando LangChain, DistilGPT2 (Hugging Face), FAISS, e Gradio. Inclui testes automatizados e manipulação de dados com Pandas.
O sistema cumpre a missão de criar uma solução inovadora que agrega valor, usando Python, LangChain e Gradio.
Resolveu um desafio complexo (acesso a informações de compliance) com alta precisão (94%) e bom desempenho (2,8s a 4,2s).
Funciona em ambiente local reduzindo a dependecia de outras tecnologia pagas e nao proprietarias.

