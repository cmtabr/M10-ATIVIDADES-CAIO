FROM python:3.11-slim-buster

RUN mkdir app

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FROM python:3.11-slim-buster 

# WORKDIR /app

# COPY --from=builder /app /app

EXPOSE 5000

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=5000"]