FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY manage.py /app/manage.py
COPY nginx /app/nginx
COPY media /app/media
COPY dev_forum /app/dev_forum
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
COPY tailwind.config.js /app/tailwind.config.js
COPY apps /app/apps
COPY static_files /app/static_files
COPY templates /app/templates
