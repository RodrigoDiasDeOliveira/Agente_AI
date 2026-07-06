# ADR 0006: Observabilidade, rate limiting e logging básico

- Status: Aceito
- Data: 2026-07-06

## Contexto
A API precisava de visibilidade operacional para debugar requisições e proteger os endpoints contra abuso, sem depender de dependências externas complexas.

## Decisão
Adicionar logging simples de requisições, contadores de métricas expostos em /metrics e proteção básica por rate limiting por IP para os endpoints principais.

## Consequências
- A operação da API fica mais observável.
- O sistema se torna mais resiliente a picos e uso abusivo.
- A base está pronta para evoluir para uma solução de observabilidade mais completa.
