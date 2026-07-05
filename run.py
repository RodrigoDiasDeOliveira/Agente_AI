import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    os.system("uvicorn app.api:app --host 0.0.0.0 --port 8000")