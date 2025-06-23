FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpython3-dev \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

# ---------------------------------------------

FROM python:3.13-slim

RUN useradd -m -d /home/django django

WORKDIR /app

ARG DJANGO_USER_PASSWORD

RUN apt-get update
RUN apt-get install -y --no-install-recommends libpq5 gettext curl netcat-traditional
RUN apt-get install -y --no-install-recommends mc openssh-server
RUN echo "django:${DJANGO_USER_PASSWORD}" | chpasswd
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN mkdir /run/sshd

RUN rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /home/django/.local

COPY . /app/
COPY ./entrypoint.sh .

RUN chmod +x /app/entrypoint.sh

ENV PATH=/home/django/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN chown -R django:django /app /home/django

USER django

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["/bin/bash"]
