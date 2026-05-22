# ── Stage 1: Builder ──────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app
RUN pip install --no-cache-dir uv

COPY requirements.txt .
RUN uv venv /app/.venv && \
    uv pip install --python /app/.venv/bin/python -r requirements.txt --no-cache

# ── Stage 2: Runtime ──────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# Instala dependências de sistema (Chromium)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libxss1 libasound2 libgbm1 libgtk-3-0 && \
    rm -rf /var/lib/apt/lists/*

# Cria usuário não-root (REQUISITO 2.1)
RUN addgroup --system scraper && adduser --system --ingroup scraper scraper

# Copia ambiente do builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Instala Playwright e ajusta permissões
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN /app/.venv/bin/playwright install chromium && \
    chown -R scraper:scraper /ms-playwright

# Copia código e prepara pastas
COPY scraper/ ./scraper/
COPY main.py .
RUN mkdir -p /app/output && chown -R scraper:scraper /app/output

USER scraper
VOLUME ["/app/output"]

# Exposição da porta (Requisito 2.1)
# Embora o scraper não seja um servidor HTTP, se você futuramente quiser
# expor uma API, a porta seria esta:
EXPOSE 8080

ENTRYPOINT ["python", "main.py"]
CMD []