FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpython3-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 mc netcat-traditional gettext && \
    rm -rf /var/lib/apt/lists/*


COPY --from=builder /root/.local /root/.local

# COPY src/ /app/
COPY ./entrypoint.sh .

RUN chmod +x /app/entrypoint.sh

ENV PATH=/root/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
