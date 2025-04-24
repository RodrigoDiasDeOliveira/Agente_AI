import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.main import demo

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)