# app/admin.py
import gradio as gr
import json
from .search_space import SearchSpaceManager
from .models import SearchTargetCreate, MatchDocument
from .trusted_search import TrustedAnswerSearch
from .feedback_handler import FeedbackHandler

manager = SearchSpaceManager()
trusted_search = TrustedAnswerSearch()
feedback_handler = FeedbackHandler()

def create_target(target_id, description, alt_phrases, doc_type, url, title, params):
    try:
        alt_list = [p.strip() for p in alt_phrases.split("\n") if p.strip()]
        match_doc = MatchDocument(
            type=doc_type,
            url=url,
            title=title,
            parameters=json.loads(params) if params.strip() else {}
        )
        
        target = SearchTargetCreate(
            target_id=target_id,
            description=description,
            alternative_phrases=alt_list,
            match_document=match_doc
        )
        manager.add_manual_target(target)
        return "✅ Target criado com sucesso!", gr.update()  # atualiza lista
    except Exception as e:
        return f"❌ Erro: {str(e)}", gr.update()

def load_pdfs():
    count = manager.load_pdfs_to_targets()
    return f"✅ {count} targets criados a partir dos PDFs!", gr.update()

def list_targets():
    """Lista todos os targets cadastrados"""
    session = trusted_search.Session()
    result = session.execute(text("SELECT target_id, description, match_document->>'type' as type FROM search_targets ORDER BY created_at DESC"))
    targets = [f"**{row.target_id}** ({row.type}): {row.description[:100]}..." for row in result]
    session.close()
    return "\n\n".join(targets) if targets else "Nenhum target cadastrado ainda."

def show_feedback_stats():
    stats = feedback_handler.get_feedback_stats()
    recent = feedback_handler.get_recent_feedback(limit=10)
    
    stats_text = "### Estatísticas de Feedback\n\n"
    for ftype, data in stats.items():
        stats_text += f"- **{ftype.capitalize()}**: {data['count']} feedbacks (similaridade média: {data['avg_similarity']:.1%})\n"
    
    recent_text = "\n\n### Últimos Feedbacks\n\n"
    for fb in recent:
        recent_text += f"- **{fb['feedback_type']}** → {fb['query'][:80]}... (sim: {fb['similarity']:.1%})\n"
    
    return stats_text + recent_text

# ===================== INTERFACE ADMIN =====================

with gr.Blocks(title="Admin - Trusted Answer Search") as admin_app:
    gr.Markdown("# 🛠️ Administração - Trusted Answer Search")

    with gr.Tabs():
        with gr.Tab("Cadastrar Target"):
            with gr.Row():
                tid = gr.Textbox(label="Target ID (ex: POL-001)", value="POL-")
                dtype = gr.Dropdown(["policy", "report", "action", "section"], label="Tipo", value="policy")
            
            desc = gr.Textbox(label="Descrição Principal", lines=3)
            alt = gr.Textbox(label="Frases Alternativas (uma por linha)", lines=4)
            
            with gr.Row():
                url_input = gr.Textbox(label="URL / Link")
                title_input = gr.Textbox(label="Título")
            
            params_input = gr.Textbox(label="Parâmetros (JSON)", value='{"categoria": "brindes"}')
            
            btn_create = gr.Button("Criar Novo Target", variant="primary")
            create_output = gr.Textbox(label="Resultado")

            btn_create.click(
                create_target,
                inputs=[tid, desc, alt, dtype, url_input, title_input, params_input],
                outputs=[create_output, gr.State()]  # gr.State() para refresh futuro
            )

        with gr.Tab("Carregar PDFs"):
            gr.Markdown("Carrega automaticamente os PDFs da pasta `data/docs`")
            btn_load = gr.Button("🚀 Carregar todos os PDFs", variant="primary", size="large")
            load_output = gr.Textbox(label="Resultado")
            btn_load.click(load_pdfs, outputs=load_output)

        with gr.Tab("Targets Cadastrados"):
            btn_refresh = gr.Button("Atualizar Lista")
            targets_list = gr.Markdown(label="Lista de Targets")
            btn_refresh.click(list_targets, outputs=targets_list)

        with gr.Tab("Feedback & Estatísticas"):
            btn_stats = gr.Button("Atualizar Estatísticas")
            stats_output = gr.Markdown(label="Estatísticas")
            btn_stats.click(show_feedback_stats, outputs=stats_output)

    gr.Markdown("---")
    gr.Markdown("Volte para o [Agente Principal](../)")

# Para rodar o admin separadamente:
if __name__ == "__main__":
    admin_app.launch(server_name="0.0.0.0", server_port=7861)