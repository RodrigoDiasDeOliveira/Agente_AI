from gradio_client import Client

client = Client("http://localhost:7860/")  # Ou use a URL pública

# Teste 1: Pergunta válida
result = client.predict(
    question="O que diz o Código de Conduta Ética da FIESC?",
    fn_index=0  # Ajustado para usar o índice da função (pode variar dependendo da ordem no Gradio)
)
print("Resposta para pergunta válida:", result)

# Teste 2: Pergunta vazia
result = client.predict(
    question="",
    fn_index=0
)
print("Resposta para pergunta vazia:", result)