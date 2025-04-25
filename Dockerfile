FROM python:3.12

# 1. Создаем пользователя и группу ПЕРВЫМ ДЕЛОМ
RUN groupadd -g 1000 celerygroup && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash celeryuser

# 2. Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 3. Создаем директории и назначаем права
RUN mkdir -p /var/run/celery /app/media && \
    chown -R celeryuser:celerygroup /var/run/celery /app/media

# 4. Копируем файлы проекта с правильными правами
COPY --chown=celeryuser:celerygroup . /app

# 5. Устанавливаем права для скриптов
RUN chmod +x /app/wait-for-db.sh

# 6. Переключаемся на пользователя celeryuser
USER celeryuser
WORKDIR /app

# 7. Настраиваем окружение
ENV PATH="/home/celeryuser/.local/bin:${PATH}"

# 8. Устанавливаем зависимости (

COPY requirements.txt .
RUN pip install -r requirements.txt

# 9. Экспозим порт и запускаем
EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
