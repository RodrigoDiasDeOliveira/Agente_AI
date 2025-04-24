from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
VECTORSTORE_PATH = "data/vectorstore"
DOCS_PATH = "data/docs/Relatório Sintético 2023 - Programa de Compliance_site.pdf",
"/workspaces/Agente_AI/data/docs/Codigo-de-Conduta-Etica.pdf",
"/workspaces/Agente_AI/data/docs/Comunicado_brinde_assinado.pdf",
"/workspaces/Agente_AI/data/docs/Guia 4 - PMEs.pdf",
"/workspaces/Agente_AI/data/docs/Política Anticorrupção do Sistema FIESC.pdf",
"/workspaces/Agente_AI/data/docs/Política de Ética e Compliance da FIESC e suas Entidades.pdf",
"/workspaces/Agente_AI/data/docs/Politica-de-conflito-de-interesses.pdf"

# Verificar se a chave API está definida
if not HUGGINGFACEHUB_API_TOKEN:
    print("Aviso: HUGGINGFACEHUB_API_TOKEN não definido. Usando modelo público.")