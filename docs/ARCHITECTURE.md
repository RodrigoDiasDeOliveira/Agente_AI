# Architecture Document - Trusted Compliance Agent v2.0

**Date:** May 03, 2026  
**Version:** 2.0  
**Status:** Current

## 1. Introduction

This project evolved from a classic RAG-based agent into a **hybrid Trusted Answer Search** system, inspired by Oracle's Trusted Answer Search concept.

The main goal is to deliver **accurate, secure, and deterministic** answers for Compliance use cases.

## 2. Core Principles

- Prefer **curated targets** over generative answers
- Use **reranking** to improve retrieval quality
- Implement human-in-the-loop through feedback
- Maintain fallback mechanism for edge cases

## 3. High-Level Architecture



## 4. Components
Layer,Component,Technology,Responsibility
Interface,Main + Admin,Gradio,UI/UX
Orchestration,TrustedAnswerSearch,Python + SQLAlchemy,Core Logic
Retrieval,Vector Search,PostgreSQL + pgvector,Initial Search
Reranking,CrossEncoder,sentence-transformers,Ranking Refinement
Knowledge,Search Targets,search_targets table,Curated Knowledge
Feedback,FeedbackHandler,feedback table,Human Learning
Fallback,LLM Agent,LangChain,Generated Answers
Ingestion,PDF Loader,PyPDF,Document Processing


## 5. Data Flow

1. Ingestion → PDF → Targets → PostgreSQL
2. Query → Embedding → Vector Search → Reranking → Decision
3. Feedback → Learning Loop

## 6. Technologies

- PostgreSQL + pgvector
- CrossEncoder Reranker
- Gradio (UI + Admin)
- LangChain (fallback)
- SQLAlchemy + Pydantic

---

**Última atualização:** 03/05/2026