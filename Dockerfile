FROM python:3.10.6

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

ENV PYTHONUNBUFFERED=0

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]