FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY src /app/
COPY .gitignore /app/
COPY docker-compose-prod.yml /app/
COPY Dockerfile /app/
COPY package.json /app/
COPY package-lock.json /app/
COPY README.md /app/
COPY tailwind.config.js /app/