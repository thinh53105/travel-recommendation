FROM python:3.11-slim-buster


COPY . /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000"]