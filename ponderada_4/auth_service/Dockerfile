FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .
COPY . user_service

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt