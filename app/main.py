import gradio as gr
from app.llm_agent import setup_agent, ask_agent
from app.data_handler import save_interaction

# Configura o agente
qa_chain = setup_agent()

# Função que processa a entrada do usuário
async def ask_question(question: str):
    if not question.strip():
        return "Erro: A pergunta não pode estar vazia."
    result = ask_agent(question, qa_chain)
    answer = result["answer"]
    sources = result["sources"]
    # Salva a interação
    save_interaction(question, answer)
    return f"**Resposta**: {answer}\n\n**Fontes**: {sources}"

# Configura a interface Gradio
iface = gr.Interface(
    fn=ask_question,
    inputs=gr.Textbox(label="Digite sua pergunta"),
    outputs=gr.Textbox(label="Resposta"),
    title="Agente AI",
    description="Um agente conversacional com RAG para resolver problemas complexos."
)

# Inicia o Gradio
if __name__ == "__main__":
    iface.launch(share=False, server_name="0.0.0.0", server_port=7860)