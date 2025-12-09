# Базовый образ
FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y gcc libpq-dev

# Создаём рабочую директорию
WORKDIR /app

# Копируем зависимости и ставим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY ./src ./src
COPY ./alembic.ini ./
COPY ./alembic ./alembic

# Переменные окружения
ENV PYTHONUNBUFFERED=1

# Команда по умолчанию
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
