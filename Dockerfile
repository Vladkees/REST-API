# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Копіюємо залежності
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копіюємо весь код
COPY . .

CMD ["python", "run.py"]
