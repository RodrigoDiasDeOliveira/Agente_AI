from fastapi import FastAPI
from pydantic import BaseModel
from app.llm_agent import ask_question
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir chamadas do Gradio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    answer = ask_question(query.question)
    return {"answer": answer}
