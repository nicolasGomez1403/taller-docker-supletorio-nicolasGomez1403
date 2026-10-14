# ===== ETAPA 1: CONSTRUCCIÓN =====
FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12.17 /uv /usr/local/bin/uv

WORKDIR /build

COPY pyproject.toml uv.lock ./

# Crear el venv en la MISMA ruta que tendrá en producción
ENV UV_PROJECT_ENVIRONMENT=/srv/reservas/.venv
RUN uv venv /srv/reservas/.venv && \
    uv sync --frozen --no-dev

# ===== ETAPA 2: PRODUCCIÓN =====
FROM python:3.14-slim

RUN useradd --create-home --shell /bin/bash reservas

WORKDIR /srv/reservas

# Copiar el venv desde la misma ruta
COPY --from=builder /srv/reservas/.venv /srv/reservas/.venv

COPY reservas/ ./reservas/

RUN chown -R reservas:reservas /srv/reservas

ENV PATH="/srv/reservas/.venv/bin:$PATH"

USER reservas

EXPOSE 8500

HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8500/estado')" || exit 1

CMD ["uvicorn", "reservas.api:app", "--host", "0.0.0.0", "--port", "8500"]