---

# Todo API

Flask-приложение для ведения простого списка задач (ToDo), с документацией через Swagger и хранением данных в PostgreSQL (через Peewee ORM).

---
Возможности

- Получение списка задач
- Добавление задачи
- Получение задачи по ID
- Обновление задачи (текст и статус)
- Удаление задачи
- Swagger UI с автогенерируемой документацией по эндпоинтам

---
Переменные окружения

Перед запуском необходимо указать настройки подключения к БД через переменные окружения:

- `DB_NAME` — имя базы данных
- `DB_USER` — пользователь Postgres
- `DB_PASSWORD` — пароль пользователя
- `DB_HOST` — адрес сервера БД
- `DB_PORT` — порт сервера БД (по умолчанию 5432)

Пример (Linux/Mac):
export DB_NAME="todos"
export DB_USER="postgres"
export DB_PASSWORD="your_password"
export DB_HOST="localhost"
export DB_PORT="5432"


---
Запуск

1. Установи зависимости:

pip install flask peewee flasgger psycopg2-binary


2. Запусти приложение:

python app.py


После запуска API будет доступно на `http://localhost:1488`.

---
Документация

Открой Swagger-документацию по адресу:

http://localhost:1488/apidocs/


---
Примеры запросов
Получить все задачи

`GET /tasks`
Добавить задачу

`POST /tasks`  
Тело запроса (JSON):
{
  "text": "Купить хлеб"
}

Получить задачу по ID

`GET /tasks/<id>`
Обновить задачу

`PATCH /tasks/<id>`  
Тело запроса (JSON):
{
  "text": "Купить молоко",
  "done": true
}

Удалить задачу

`DELETE /tasks/<id>`

---
Технологии

- Python 3.7+
- Flask 2+
- Peewee ORM
- Flasgger (Swagger UI)
- PostgreSQL

---
Лицензия

MIT (или укажи свою).

---
Заметки

- Приложение создает таблицу для задач автоматически при первом запуске.
- Остальные детали и примеры смотри в Swagger-документации.

---