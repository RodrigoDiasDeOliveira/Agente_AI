# ADR 0002: Aplicação FastAPI unificada com endpoint padronizado

- Status: Aceito
- Data: 2026-07-06

## Contexto
O repositório mantinha duas apps FastAPI separadas e o frontend esperava um endpoint diferente do backend, causando inconsistência de integração.

## Decisão
Unificar a API principal montando o admin sob o mesmo app e padronizar a consulta no endpoint /api/ask, mantendo /api/query como alias compatível.

## Consequências
- O backend expõe uma interface mais consistente para frontend e clientes.
- As rotas administrativas passam a ficar disponíveis sob /admin.
- A compatibilidade com integrações antigas é preservada.
