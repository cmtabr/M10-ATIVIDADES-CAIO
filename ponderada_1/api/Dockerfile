FROM python:3.11-slim-buster 

RUN mkdir app

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000 

CMD ["uvicorn", "api.main:app", "--host=0.0.0.0", "--port=5000"]