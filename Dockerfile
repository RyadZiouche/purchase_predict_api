FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
RUN apt update && apt install -y libgomp1 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN uv sync
EXPOSE 80
CMD ["uv", "run", "gunicorn", "app:app", "-b", "0.0.0.0:80", "-w", "4"]