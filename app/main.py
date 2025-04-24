import sys
import os
import gradio as gr

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.llm_agent import setup_agent, ask_agent
from app.data_handler import save_interaction

# Configura o agente
qa_chain = setup_agent()

# CSS para estilização
css = """
    .gradio-container {
        font-family: 'Arial', sans-serif;
        background-color: #f5f7fa;
    }
    h1 {
        color: #2c3e50;
        font-size: 2em;
        text-align: center;
        margin-bottom: 10px;
    }
    .description {
        color: #7f8c8d;
        font-size: 1.1em;
        text-align: center;
        margin-bottom: 20px;
    }
    .gr-button-primary {
        background-color: #2980b9;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    .gr-button-secondary {
        background-color: #95a5a6;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    .gr-textbox {
        border-radius: 5px;
        border: 1px solid #dcdcdc;
        padding: 10px;
    }
    .gr-textbox:focus {
        border-color: #2980b9;
        box-shadow: 0 0 5px rgba(41, 128, 185, 0.3);
    }
    .gr-slider {
        width: 50%;
        margin: 0 auto;
    }
    .example-box {
        background-color: #ecf0f1;
        border-radius: 5px;
        padding: 10px;
        margin: 5px 0;
        cursor: pointer;
    }
    .example-box:hover {
        background-color: #dfe6e9;
    }
"""

# Função para processar a pergunta (usada na interface)
async def process_question(question: str, num_chunks: int = 1):
    if not question.strip():
        return "Erro: A pergunta não pode estar vazia.", ""
    result = ask_agent(question, qa_chain, num_chunks=int(num_chunks))
    answer = result["answer"]
    sources = "\n".join(result["sources"])
    # Salva a interação
    save_interaction(question, answer)
    return answer, sources

# Função para atualizar o histórico
def update_history(question: str, answer: str, history: list):
    if question.strip() and answer != "Erro: A pergunta não pode estar vazia.":
        history.append((question, answer))
    history_md = "### Histórico de Perguntas\n---\n"
    for q, a in history:
        history_md += f"**Pergunta**: {q}\n\n**Resposta**: {a}\n\n---\n"
    return history_md

# Função para limpar os campos
def clear_inputs():
    return "", "", "", 1  # Limpa question_input, answer_output, sources_output e reseta num_chunks

# Interface Gradio com melhorias
with gr.Blocks(theme=gr.themes.Soft(), css=css) as demo:
    # Estado para o histórico
    history = gr.State([])

    # Título e descrição
    gr.Markdown(
        """
        # Agente AI - Consultas de Compliance
        Faça perguntas detalhadas sobre o **Relatório Sintético 2023 de Compliance**.  
        Use os exemplos abaixo ou digite sua própria pergunta!
        """
    )

    # Campo de entrada
    with gr.Row():
        with gr.Column(scale=3):
            question_input = gr.Textbox(
                label="Digite sua pergunta",
                placeholder="Ex.: Quais treinamentos de compliance foram realizados em 2023?",
                lines=3,
                show_label=True
            )

    # Slider para ajustar o número de trechos
    with gr.Row():
        num_chunks = gr.Slider(
            minimum=1,
            maximum=5,
            value=1,
            step=1,
            label="Número de trechos recuperados (k)",
            show_label=True
        )

    # Botões
    with gr.Row():
        submit_button = gr.Button("Enviar", variant="primary")
        clear_button = gr.Button("Limpar", variant="secondary")

    # Saídas
    with gr.Row():
        with gr.Column(scale=2):
            answer_output = gr.Textbox(label="Resposta", lines=5, show_label=True)
        with gr.Column(scale=2):
            sources_output = gr.Textbox(label="Fontes", lines=5, show_label=True)

    # Histórico de perguntas
    with gr.Row():
        history_output = gr.Markdown("### Histórico de Perguntas\n---")

    # Exemplos de perguntas
    gr.Examples(
        examples=[
            "Como o Relatório Sintético 2023 descreve o engajamento dos funcionários com o programa de compliance?",
            "Quais treinamentos de compliance foram realizados em 2023, segundo o Relatório Sintético 2023?",
            "Quais riscos de compliance foram identificados no Relatório Sintético 2023?"
        ],
        inputs=question_input,
        label="Exemplos de Perguntas"
    )

    # Conectar os botões às funções
    submit_button.click(
        fn=process_question,
        inputs=[question_input, num_chunks],
        outputs=[answer_output, sources_output]
    ).then(
        fn=update_history,
        inputs=[question_input, answer_output, history],
        outputs=history_output
    )

    clear_button.click(
        fn=clear_inputs,
        inputs=[],
        outputs=[question_input, answer_output, sources_output, num_chunks]
    )

# Lançar a interface
if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)