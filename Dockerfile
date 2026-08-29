FROM python:3.11-slim

WORKDIR /app

# Dépendances système pour PyMuPDF et torch CPU
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
# torch CPU-only : évite de télécharger les paquets CUDA (plusieurs Go inutiles, pas de GPU en conteneur)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# src/ doit être copié avant l'install éditable, sinon hatchling ne trouve pas le package
# et pip install -e installe seulement les métadonnées (ModuleNotFoundError au runtime)
COPY src/ src/
RUN pip install --no-cache-dir -e ".[dev]"

CMD ["uvicorn", "coursegraph.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
