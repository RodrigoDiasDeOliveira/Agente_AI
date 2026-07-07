# ADR-010: Hybrid Search Architecture (Trusted + RAG)

- Status: Accepted
- Date: 2026-07-07

## Context
Pure RAG solutions often suffer from hallucinations, while purely deterministic search lacks flexibility for semantic queries. The compliance domain requires high accuracy and auditability.

## Decision
Implement a **Hybrid Search** approach:
- Primary: Trusted Answer Search (deterministic, curated targets)
- Fallback: RAG with LangChain + Vector Search
- Confidence scoring to decide which path to use
- Feedback loop for continuous improvement

## Consequences
- Significantly reduced hallucinations in critical compliance responses.
- High precision for known questions and good coverage for new ones.
- Easier auditing and traceability (trusted answers are explicit).
- Increased complexity in query routing logic, mitigated by clear confidence thresholds.
- Strong alignment with enterprise requirements for reliable AI systems.