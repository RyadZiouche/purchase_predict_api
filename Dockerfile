FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Dépendances système
RUN apt update && apt install -y libgomp1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie de tous les fichiers
COPY . .

# Installation des dépendances
RUN uv sync

# Pas de EXPOSE fixe ici

# Commande de lancement avec port dynamique
# On utilise le port fourni par Cloud Run ($PORT), sinon 8080 par défaut
CMD ["sh", "-c", "uv run gunicorn app:app -b 0.0.0.0:${PORT:-8080} -w 4"]