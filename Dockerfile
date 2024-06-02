FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

#  код проекта
COPY . /app

# порт
EXPOSE 8000

# запуск
CMD ["python", "main.py"]