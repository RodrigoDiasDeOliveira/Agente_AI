#!/usr/bin/env sh
set -e

echo "[entrypoint] Aguardando Postgres em ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}..."
python - <<'PY'
import os, time, socket
host = os.environ.get("POSTGRES_HOST", "db")
port = int(os.environ.get("POSTGRES_PORT", "5432"))
for i in range(60):
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"[entrypoint] Postgres OK após {i}s")
            break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit("[entrypoint] Postgres indisponível")
PY

echo "[entrypoint] Rodando init_db..."
python -m migrations.init_db

echo "[entrypoint] Iniciando API..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
