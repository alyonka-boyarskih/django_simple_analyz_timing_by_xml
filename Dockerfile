FROM python:3.8.2-slim

RUN mkdir /app

WORKDIR /app


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/.

ENV PYTHONIOENCODING="UTF-8"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["bash", "/app/docker-entrypoint.sh"]
