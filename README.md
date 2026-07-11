#  Trusted Compliance Agent

<img width="1280" height="853" alt="1777839409525" src="https://github.com/user-attachments/assets/39a6bc41-60fd-4922-afc7-5d28386edc21" />

**Version 2.1** - Modern React Frontend with FastAPI backend. Removed Gradio dependency.

A high-precision hybrid solution for compliance questions, combining deterministic and semantic search.

## Key Features

- **Trusted Answer Search** — Deterministic, high-accuracy responses with zero hallucinations
- **Hybrid RAG** — Fallback using LangChain + Vector Search when trusted answers are not found
- **Feedback Loop** — Continuous learning from user interactions
- **Admin Panel** — Management of targets, feedback, and system monitoring
- **Modern UI** — Clean and responsive React interface

## Technologies

- **Backend**: Python 3.12, FastAPI, Uvicorn
- **Database**: PostgreSQL + pgvector
- **AI/ML**: LangChain, Hugging Face embeddings (migrating to Vertex AI + Gemini)
- **Frontend**: React + Vite
- **Infrastructure**: Terraform (GCP ready)
- **ORM**: SQLAlchemy + Pydantic

## Quick Start

### Local Development

**Backend**

uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
Frontend
Bashcd frontend
npm install
npm run dev
Access:

Frontend: http://localhost:3000
API Docs: http://localhost:8000/docs

Production Deployment (GCP)
See DEPLOYMENT-GCP.md for full Terraform-based deployment on Google Cloud.
Project Structure
textAgente_AI/
├── app/                    # FastAPI backend + business logic
├── frontend/               # React + Vite frontend
├── infrastructure/         # Terraform IaC for GCP
├── docs/                   # Architecture + ADRs
├── tests/                  # Test suite
├── interactions.csv        # Interaction history
└── README.md
Architecture Decision Records (ADRs)

View all ADRs in WIKI

an TrimindsLabs initiative 2025

