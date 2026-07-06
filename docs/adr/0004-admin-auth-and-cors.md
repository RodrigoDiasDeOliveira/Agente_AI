# ADR 0004: Autenticação mínima do painel administrativo e CORS controlado

- Status: Aceito
- Data: 2026-07-06

## Contexto
As rotas administrativas estavam expostas sem qualquer proteção, e o CORS estava liberado de forma ampla, o que não é adequado para ambientes de produção.

## Decisão
Adicionar autenticação mínima via header X-Admin-Token nas rotas /admin/* e restringir as origens permitidas via variável de ambiente CORS_ORIGINS.

## Consequências
- O painel administrativo fica protegido por padrão.
- A exposição da API para browsers fica mais segura.
- O ambiente pode ser configurado de forma diferente em dev, staging e produção.
