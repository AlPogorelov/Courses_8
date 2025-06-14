# Courses_8
Курсовая работу по теме "Трекер привычек" 
WEB приложение для отслеживания привычек.

# IP ВМ 158.160.27.100
## Локальная установка и запуск

### Требования
- Docker 20.10+
- docker-compose 1.29+

### Запуск проекта
1. Клонируйте репозиторий:
```
git clone https://github.com/AlPogorelov/Courses_8.git
cd Courses_8 
```

### Заполните значения в файле .env:

```
SECRET_KEY =
DEBUG = True
POSTGRES_DB =
POSTGRES_USER =
POSTGRES_PASSWORD =
HOST =
PORT =
STRIPE_API_KEY =
STRIPE_PUBLISHABLE_KEY =
TELEGRAM_API_KEY=
CELERY_BROKER_URL =
CELERY_RESULT_BACKEND =
```
### Запустите проект:
```docker-compose up --build```

Проект будет доступен по адресу: http://localhost:8000

# Настройка CI/CD
## Требования
Сервер с Docker

SSH доступ к серверу

Аккаунт на Docker Hub

## Инструкция
### Добавьте секреты в GitHub (Settings → Secrets):
SECRET_KEY - секретный ключ Django

POSTGRES_* - данные PostgreSQL

DOCKER_HUB_USERNAME - логин Docker Hub

DOCKER_HUB_ACCESS_TOKEN - токен Docker Hub

SSH_KEY - приватный SSH-ключ

SSH_USER - пользователь сервера

SERVER_IP - IP сервера

## Настройте сервер:
Установите Docker

```sudo apt-get update && sudo apt-get install docker.io docker-compose```

Добавьте пользователя в группу docker
```
sudo usermod -aG docker $USER
newgrp docker
```
## При пуше произойдет:

Линтинг кода

Запуск тестов

Сборка Docker-образов

Пуш образов в Docker Hub

Автоматический деплой на сервер
