import gradio as gr
from langchain_xai import ChatGrok
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.data_handler import save_interaction

# Configuração do Grok e LangChain
grok = ChatGrok(api_key="sua-api-key-aqui")  # Substitua pela sua API key
prompt = PromptTemplate.from_template("Responda: {question}")
chain = LLMChain(llm=grok, prompt=prompt)

# Função que processa a entrada do usuário
async def ask_question(question: str):
    if not question.strip():
        return "Erro: A pergunta não pode estar vazia."
    response = await chain.invoke({"question": question})
    answer = response["content"]
    # Salva a interação
    save_interaction(question, answer)
    return answer

# Configura a interface Gradio
iface = gr.Interface(
    fn=ask_question,
    inputs=gr.Textbox(label="Digite sua pergunta"),
    outputs=gr.Textbox(label="Resposta"),
    title="Agente AI",
    description="Um agente conversacional para resolver problemas complexos."
)

# Inicia o Gradio
if __name__ == "__main__":
    iface.launch(share=False, server_name="0.0.0.0", server_port=7860)