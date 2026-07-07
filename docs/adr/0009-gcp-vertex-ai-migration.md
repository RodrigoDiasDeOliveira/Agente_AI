# ADR-009: Migration to Vertex AI and Gemini Models

- Status: Accepted
- Date: 2026-07-07

## Context
The project initially used local Hugging Face models or generic LLM providers, which limited scalability, performance in production, and integration with enterprise-grade observability and security features.

## Decision
Migrate the main LLM layer to **Google Vertex AI** using **Gemini models** (Gemini 1.5 Pro/Flash), combined with Vertex AI Vector Search for embeddings and retrieval.

## Consequences
- Better performance, lower latency, and native multimodal support.
- Improved integration with GCP services (monitoring, IAM, security settings).
- Easier cost control and automatic scaling.
- Foundation laid for advanced features such as Agent Engine, grounding, and evaluation pipelines.
- Slight increase in operational complexity (requires GCP project and proper IAM configuration).