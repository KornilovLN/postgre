# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем зависимости для psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc

# Устанавливаем зависимости Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем приложение в контейнер
COPY app.py /app/app.py

# Устанавливаем рабочую директорию
WORKDIR /app

# Указываем команду для запуска приложения
CMD ["python", "app.py"]
