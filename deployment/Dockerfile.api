FROM python:3.12-slim

# Evitar .pyc y buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar deps del sistema si hiciera falta (ej. psycopg con libpq)
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY dependencies.txt .
RUN pip install --no-cache-dir -r dependencies.txt

# Copiamos el código
COPY . .

# Puerto de la API
EXPOSE 8000

# Comando por defecto (prod). En dev lo sobreescribimos con compose.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]