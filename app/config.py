from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
VECTORSTORE_PATH = "data/vectorstore"
DOCS_PATH = "data/docs/Relatório Sintético 2023 - Programa de Compliance_site.pdf"

# Verificar se a chave API está definida
if not HUGGINGFACEHUB_API_TOKEN:
    print("Aviso: HUGGINGFACEHUB_API_TOKEN não definido. Usando modelo público.")