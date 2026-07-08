# Terraform infrastructure

Esta pasta contém a estrutura inicial do Terraform para provisionar a infraestrutura do projeto em Google Cloud.

## Estrutura

- envs/dev: configuração do ambiente de desenvolvimento
- envs/prod: configuração do ambiente de produção
- modules: módulos reutilizáveis para cada componente da plataforma

## Próximos passos

1. Execute:
   - terraform -chdir=envs/dev init
   - terraform -chdir=envs/dev plan
