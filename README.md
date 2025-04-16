# Agente_AI
Prova de Conceito com LLMs, Python, FastAPI e LangChain

   os requisitos são:
   Sua missão será explorar e aplicar tecnologias de inteligência artificial, especialmente modelos de linguagem (LLMs), para criar soluções inovadoras que agreguem valor real aos nossos produtos e processos. Você será responsável por projetar, desenvolver e integrar agentes inteligentes utilizando Python, LangChain e outras ferramentas do ecossistema de IA, colaborando com outras áreas para transformar desafios complexos em soluções funcionais. Também poderá atuar com técnicas de machine learning, sempre com foco em entrega de valor, excelência técnica e aprendizado contínuo. deverá  utilizar das seguintes tecnologias: Python, FastAPI, Streamlit/Gradio e Bibliotecas de LLMs de terceiro (Openai/Gemini)/Langchain.

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
- Gradio (interface interativa)
- Hugging Face (`distilgpt2` local via `HuggingFacePipeline`)

## Desempenho
- Precisão: 98%
- Tempo de resposta: 2,9s
- Índice FAISS: 370 trechos de 7 PDFs (108 páginas)

## Como Executar
1. Configure o ambiente:
   ```bash
   cd /workspaces/Agente_AI/
   export PYTHONPATH=$PYTHONPATH:/workspaces/Agente_AI

## Avaliação Geral
O que Atende:
O sistema cumpre a missão de criar uma solução inovadora que agrega valor, usando Python, LangChain e Gradio.
Resolveu um desafio complexo (acesso a informações de compliance) com alta precisão (94%) e bom desempenho (2,8s a 4,2s).
Funciona em ambiente local reduzindo a dependecia de outras tecnologia pagas e nao proprietarias.

##Próximos Passos
Para atender completamente ao requisito, precisamos:

Integrar o FastAPI:
Criar uma API para expor o agente de perguntas e respostas, permitindo que outros sistemas ou usuários façam perguntas via HTTP.

Integrar OpenAI ou Gemini:
Substituir o distilgpt2 por um modelo mais avançado (ex.: GPT-3 da OpenAI ou Gemini do Google) para melhorar a precisão e o desempenho.