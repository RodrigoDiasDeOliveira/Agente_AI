import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
from app.llm_agent import ask_agent

def respond_to_user(question):
    answer = ask_agent(question)
    return answer

# Título e descrição
title = "Agente IA com LangChain e FAISS"
description = "Digite sua pergunta baseada nos documentos carregados. O agente usará IA para buscar e responder com contexto."

# Interface Gradio
demo = gr.Interface(
    fn=respond_to_user,
    inputs=gr.Textbox(label="Sua pergunta", placeholder="Ex: O que a política de segurança diz sobre backups?"),
    outputs=gr.Textbox(label="Resposta da IA"),
    title=title,
    description=description,
)

if __name__ == "__main__":
    demo.launch()
