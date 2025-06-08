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

# Создаём пользователя django
RUN useradd -m -d /home/django django

WORKDIR /app

#RUN apt-get update && \
#    apt-get install -y --no-install-recommends libpq5 mc netcat-traditional gettext curl && \
#    rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get install -y --no-install-recommends libpq5 gettext curl netcat-traditional
RUN apt-get install -y --no-install-recommends mc openssh-server
RUN rm -rf /var/lib/apt/lists/*

RUN echo 'django:django' | chpasswd
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN mkdir /run/sshd

# Установка SSH (только для dev окружения)
#ARG INSTALL_SSH=false
#RUN if [ "$INSTALL_SSH" = "true" ] ; then \
#    apt-get update && apt-get install -y openssh-server openssl openssh-client && \
#    rm -rf /var/lib/apt/lists/* ; \
#    fi

# Копируем зависимости Python из builder
COPY --from=builder /root/.local /home/django/.local

# Копируем скрипт и даём права
COPY . /app/
COPY ./entrypoint.sh .

RUN chmod +x /app/entrypoint.sh

# Устанавливаем переменные окружения
ENV PATH=/home/django/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Назначаем владельцем всё в /app и home
RUN chown -R django:django /app /home/django

# Переключаемся на пользователя django
USER django

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["/bin/bash"]
