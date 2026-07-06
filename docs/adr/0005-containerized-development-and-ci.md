# ADR 0005: Stack containerizada com Docker Compose e CI

- Status: Aceito
- Data: 2026-07-06

## Contexto
O projeto não possuía um fluxo de onboarding consistente para desenvolvimento local nem automação de validação em CI.

## Decisão
Adicionar Dockerfile, Docker Compose com serviços para banco, API e frontend, além de um workflow GitHub Actions para rodar testes e build do frontend.

## Consequências
- O setup do projeto fica mais simples e reproduzível.
- O onboarding melhora para novos desenvolvedores.
- Mudanças passam por validação automática em cada push ou pull request.
