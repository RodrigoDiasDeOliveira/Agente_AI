import pandas as pd
import os

def save_interaction(question: str, answer: str):
    # Salva a interação em um CSV
    data = {"question": [question], "answer": [answer], "timestamp": [pd.Timestamp.now()]}
    df = pd.DataFrame(data)
    file_exists = os.path.isfile("interactions.csv")
    df.to_csv("interactions.csv", mode="a", index=False, header=not file_exists)

def analyze_interactions():
    # Lê e analisa interações
    if not os.path.isfile("interactions.csv"):
        return "Nenhuma interação registrada."
    df = pd.read_csv("interactions.csv")
    return df.describe(include="all")