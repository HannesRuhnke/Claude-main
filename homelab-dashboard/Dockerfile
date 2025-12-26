# Dockerfile für Homelab Dashboard V3
FROM python:3.11-slim

# Metadaten
LABEL maintainer="Homelab Dashboard"
LABEL description="Homelab Dashboard V3 - Enterprise Edition"
LABEL version="3.0"

# Arbeitsverzeichnis
WORKDIR /app

# System-Dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python-Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendung kopieren
COPY backend-v3.py .
COPY index.html .
COPY login.html .
COPY app-v2.js .
COPY styles.css .

# Verzeichnisse erstellen
RUN mkdir -p backups screenshots

# Umgebungsvariablen
ENV FLASK_APP=backend-v3.py
ENV PYTHONUNBUFFERED=1

# Port freigeben
EXPOSE 5000

# Health Check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/api/auth/check', timeout=5)" || exit 1

# Volumes
VOLUME ["/app/backups", "/app/screenshots", "/app/homelab.db"]

# Standard-User (nicht root)
RUN useradd -m -u 1000 homelab && \
    chown -R homelab:homelab /app

USER homelab

# Start-Command
CMD ["python", "backend-v3.py"]
