# Используем официальный базовый образ Python 3.12
FROM python:3.12-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt /app/

# Устанавливаем Python-зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . /app

# Указываем рабочую директорию для приложения
WORKDIR /app

# Команда по умолчанию для запуска контейнера
CMD ["scrapy", "crawl", "xenforo"]