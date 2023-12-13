FROM python:3.12-slim-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN apt update && apt install -y netcat \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /tmp/*

COPY entrypoint.sh .
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
