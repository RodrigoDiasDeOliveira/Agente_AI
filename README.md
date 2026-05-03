# Agente_AI - Trusted Compliance Agent

**Versão 2.0** - Evolução com conceitos do Oracle Trusted Answer Search

Uma solução híbrida de alta precisão para perguntas de **Compliance**, combinando:
- **Trusted Answer Search** (determinístico e sem alucinações)
- Fallback RAG (LangChain + LLM)
- PostgreSQL + pgvector
- Interface Gradio + Painel Administrativo

---

## ✨ Principais Funcionalidades

- Busca semântica confiável baseada em **Targets curados**
- Feedback loop (👍 / 👎) com aprendizado contínuo
- Modo híbrido (Trusted Search + Fallback RAG)
- Administração completa de Targets
- Carregamento automático de PDFs
- Histórico e estatísticas de uso

---

## Tecnologias Utilizadas

- **Python 3.10+**
- **PostgreSQL + pgvector** (Vector Search)
- LangChain + FAISS (legado)
- Hugging Face Embeddings (`all-MiniLM-L6-v2`)
- Gradio (Interface + Admin)
- SQLAlchemy + Pydantic
- Feedback System

---

## Como Instalar e Rodar

### 1. Clone o repositório

```bash
git clone https://github.com/RodrigoDiasDeOliveira/Agente_AI.git
cd Agente_AI

2. Crie o ambiente virtual
Bashpython -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
3. Instale as dependências
Bashpip install -r requirements.txt
4. Configure o .env
envDATABASE_URL=postgresql://usuario:senha@localhost:5432/agente_ai
HUGGINGFACEHUB_API_TOKEN=seu_token_aqui
Crie o banco agente_ai no PostgreSQL antes.
5. Inicialize o Banco de Dados
Bashpython migrations/init_db.py
6. Rode a Aplicação
Modo Principal (Usuário):
Bashpython app/main.py
Modo Administração (em outra aba):
Bashpython app/admin.py
Acesse:

Agente: http://localhost:7860
Admin: http://localhost:7861


Como Usar
Usuário Final

Digite sua pergunta sobre compliance
Ative "Usar Trusted Answer Search"
Avalie a resposta com 👍 ou 👎 (importante para melhoria contínua)

Administração

Cadastrar Target: Crie regras manuais
Carregar PDFs: Importe automaticamente documentos da pasta data/docs
Targets Cadastrados: Visualize todos os itens
Feedback: Acompanhe estatísticas e respostas dos usuários


Estrutura de Pastas (Atualizada)
BashAgente_AI/
├── app/
│   ├── main.py                 # Interface principal
│   ├── admin.py                # Painel administrativo
│   ├── trusted_search.py       # Core do Trusted Search
│   ├── feedback_handler.py     # Sistema de feedback
│   ├── search_space.py         # Gerenciamento de targets
│   ├── models.py               # Modelos SQLAlchemy + Pydantic
│   ├── config.py
│   ├── llm_agent.py            # Fallback RAG
│   └── ...
├── data/
│   └── docs/                   # Coloque seus PDFs aqui
├── migrations/
│   └── init_db.py
├── .env
└── README.md
