---

# Todo API

Flask-приложение для ведения списка задач (ToDo), с документацией через Swagger и хранением данных в PostgreSQL (через Peewee ORM).

---
Возможности

- Получение, добавление, обновление и удаление задач
- Swagger UI с автогенерируемой документацией
- Данные хранятся в PostgreSQL
- Полная сборка и запуск через Docker Compose

---
Быстрый старт
1. Клонируй репозиторий

git clone <ваш-репозиторий>
cd <ваша-папка>

2. Запусти приложение через Docker Compose

docker-compose up --build


Это поднимет две службы:
- db — PostgreSQL (порт 15432 для доступа с хоста)
- app — Flask-приложение (порт 5000 на локальной машине, внутри контейнера работает на 1488)
3. Swagger-документация

- Открой: [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)  
- Все эндпоинты можно исследовать и тестировать напрямую из интерфейса.

---
Переменные окружения

В docker-compose.yaml переменные заданы по умолчанию, но ты можешь их изменить под себя.

Для приложения:
- `DB_HOST=db`
- `DB_PORT=5432`
- `DB_NAME=tododb`
- `DB_USER=todo`
- `DB_PASSWORD=todo`

Для базы данных:
- `POSTGRES_DB=tododb`
- `POSTGRES_USER=todo`
- `POSTGRES_PASSWORD=todo`

---
Примеры запросов
Получить все задачи

GET /tasks

Добавить задачу

POST /tasks
Content-Type: application/json

{
  "text": "Купить хлеб"
}

Получить задачу по ID

GET /tasks/<id>

Обновить задачу

PATCH /tasks/<id>
Content-Type: application/json

{
  "text": "Купить молоко",
  "done": true
}

Удалить задачу

DELETE /tasks/<id>


---
Состав репозитория

- app.py — основной код приложения
- requirements.txt — Python-зависимости
- Dockerfile — сборка приложения
- docker-compose.yaml — многоконтейнерный запуск
- wait-for-it.sh — скрипт ожидания запуска базы
- и др.

---
Остановка и очистка

Остановить сервис:
docker-compose down


Если нужно удалить контейнеры и volume:
docker-compose down -v


---
Технологии

- Python 3.11+
- Flask 2+
- Peewee ORM
- Flasgger (Swagger UI)
- PostgreSQL 15
- Docker, Docker Compose

---
Особенности

- Таблица задач создаётся при первом запуске автоматически.
- Для локального теста API используй [http://localhost:5000](http://localhost:5000).
- Код автоматически мигрирует и подключается к сервису базы через внутреннюю docker-сеть.

---
