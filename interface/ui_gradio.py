import gradio as gr
from app.llm_agent import ask_agent

def interface_ask(question):
    result = ask_agent(question)
    return result["answer"], result["sources"]

iface = gr.Interface(
    fn=interface_ask,
    inputs="text",
    outputs=["text", "text"],
    title="Agente de Perguntas sobre PDF",
    description="Faça perguntas sobre o Relatório Sintético 2023."
)

if __name__ == "__main__":
    iface.launch()
    iface.launch()