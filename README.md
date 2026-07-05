# Agente_AI - Trusted Compliance Agent

**Versão 2.1** - Frontend React moderno com API FastAPI e remoção da dependência Gradio.

Uma solução híbrida de alta precisão para perguntas de compliance, combinando:
- Trusted Answer Search (determinístico e sem alucinações)
- Fallback RAG (LangChain + LLM)
- PostgreSQL + pgvector
- Frontend React + FastAPI

## Principais funcionalidades

- Busca semântica confiável baseada em targets curados
- Feedback loop com aprendizado contínuo
- Modo híbrido (Trusted Search + fallback RAG)
- Administração de targets e feedback
- Interface moderna em React

## Tecnologias utilizadas

- Python 3.10+
- PostgreSQL + pgvector
- FastAPI + Uvicorn
- React + Vite
- LangChain + Hugging Face embeddings
- SQLAlchemy + Pydantic

## Como rodar

### Backend

```bash
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse:
- Frontend: http://localhost:3000
- API: http://localhost:8000/docs

## Estrutura

```text
app/
  api.py
  main.py
frontend/
  src/
```

📄 [Ver Documento de Arquitetura](./docs/ARCHITECTURE.md)
