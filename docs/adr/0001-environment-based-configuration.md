# ADR 0001: Configuração baseada em variáveis de ambiente

- Status: Aceito
- Data: 2026-07-06

## Contexto
O projeto dependia de paths absolutos hardcoded e de valores fixos no código, o que quebrava a execução em ambientes diferentes do Codespaces original.

## Decisão
Centralizar a configuração em variáveis de ambiente com defaults seguros. O módulo de configuração passou a ler valores como DATABASE_URL, DOCS_PATH, CORS_ORIGINS, ADMIN_API_TOKEN e LLM_PROVIDER.

## Consequências
- O projeto passa a ser mais portátil.
- O onboarding fica mais simples em ambientes locais, Docker e CI.
- A configuração do runtime fica explícita e documentada no arquivo de exemplo de env.
