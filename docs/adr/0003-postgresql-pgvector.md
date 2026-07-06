# ADR 0003: Uso de PostgreSQL com pgvector

- Status: Aceito
- Data: 2026-07-06

## Contexto
O projeto precisava de um banco preparado para busca semântica com vetores, mas a migração inicial só criava as tabelas sem habilitar a extensão necessária.

## Decisão
Adotar PostgreSQL + pgvector como backend principal e habilitar a extensão vector na inicialização do banco via migração.

## Consequências
- A busca vetorial passa a ser suportada de forma nativa.
- O ambiente de desenvolvimento e produção ganha uma base mais alinhada ao fluxo de recuperação semântica.
- A configuração precisa de um banco compatível com pgvector.
