# app/main.py
import gradio as gr
import json
from .trusted_search import TrustedAnswerSearch
from .feedback_handler import FeedbackHandler
from .search_space import SearchSpaceManager

# Inicialização
trusted_search = TrustedAnswerSearch()
feedback_handler = FeedbackHandler()
search_manager = SearchSpaceManager()

def ask_question(question: str, use_trusted: bool):
    """Função principal de consulta"""
    if not question or question.strip() == "":
        return "Por favor, digite uma pergunta.", None, 0.0, ""

    if use_trusted:
        result = trusted_search.search(question)
        
        if isinstance(result, dict) and "match_document" in result:
            doc = result["match_document"]
            similarity = result.get("similarity", 0.0)
            target_id = result.get("target_id")
            
            response_text = f"""
**✅ Match Encontrado** ({similarity:.1%} de similaridade)

**Tipo:** {doc.get('type', 'N/A')}
**Título:** {doc.get('title', 'N/A')}
**Link/URL:** {doc.get('url', 'N/A')}

**Parâmetros:** {json.dumps(doc.get('parameters', {}), ensure_ascii=False)}
            """
            return response_text, target_id, similarity, question
        else:
            # Fallback
            fallback_text = result.get("content", "Não foi possível encontrar uma resposta confiável.")
            return fallback_text, None, 0.0, question
    else:
        # Modo antigo (RAG puro)
        from .llm_agent import get_llm_response
        response = get_llm_response(question)
        return response, None, 0.0, question


def record_feedback(feedback_type: str, target_id, similarity, question):
    """Registra feedback do usuário"""
    if target_id and question:
        feedback_handler.record_feedback(
            query=question,
            target_id=target_id,
            similarity=similarity,
            feedback_type=feedback_type,
            comment=""
        )
        return f"✅ Feedback **{feedback_type}** registrado com sucesso!"
    return "Nenhum match para registrar feedback."


# ===================== INTERFACE GRADIO =====================

with gr.Blocks(title="Agente AI - Trusted Compliance", theme=gr.themes.Soft()) as main_app:
    gr.Markdown("# 🤖 Agente de Compliance - **Trusted Answer Search**")
    gr.Markdown("Respostas precisas, seguras e determinísticas baseadas em documentos oficiais.")

    with gr.Row():
        use_trusted = gr.Checkbox(
            value=True, 
            label="🔒 Usar Trusted Answer Search (Recomendado)",
            info="Mais preciso e sem alucinações"
        )

    question_input = gr.Textbox(
        label="Faça sua pergunta sobre Compliance",
        placeholder="Ex: Qual é a política de brindes para diretores?",
        lines=2
    )

    with gr.Row():
        submit_btn = gr.Button("🔎 Consultar", variant="primary", size="large")

    output = gr.Markdown(label="Resposta", value="Aguardando consulta...")

    # Estados ocultos
    target_id_state = gr.State()
    similarity_state = gr.State()
    current_question_state = gr.State()

    # Feedback buttons
    with gr.Row(visible=True) as feedback_row:
        gr.Markdown("**Esta resposta foi útil?**")
        btn_positive = gr.Button("👍 Sim, foi boa", variant="primary")
        btn_negative = gr.Button("👎 Não foi boa")
        btn_ignore = gr.Button("Ignorar")

    status = gr.Textbox(label="Status", interactive=False)

    # ===================== EVENTOS =====================

    def on_submit(question, use_trusted):
        response, target_id, similarity, q = ask_question(question, use_trusted)
        return (
            response, 
            target_id, 
            similarity, 
            q,
            gr.update(visible=bool(target_id))  # mostra feedback só se tiver match
        )

    submit_btn.click(
        fn=on_submit,
        inputs=[question_input, use_trusted],
        outputs=[output, target_id_state, similarity_state, current_question_state, feedback_row]
    )

    # Feedback handlers
    btn_positive.click(
        fn=lambda tid, sim, q: record_feedback("positive", tid, sim, q),
        inputs=[target_id_state, similarity_state, current_question_state],
        outputs=status
    )

    btn_negative.click(
        fn=lambda tid, sim, q: record_feedback("negative", tid, sim, q),
        inputs=[target_id_state, similarity_state, current_question_state],
        outputs=status
    )

    btn_ignore.click(
        fn=lambda tid, sim, q: record_feedback("ignored", tid, sim, q),
        inputs=[target_id_state, similarity_state, current_question_state],
        outputs=status
    )

    # Link para Admin
    gr.Markdown("---")
    gr.Markdown("[🛠️ Ir para Administração de Targets](./admin)")

# Para rodar diretamente
if __name__ == "__main__":
    main_app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )