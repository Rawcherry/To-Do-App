import os
import time
from flask import Flask, request, Response
from flasgger import Swagger
from peewee import Model, CharField, BooleanField 
from playhouse.pool import PooledPostgresqlDatabase
from peewee import OperationalError
from peewee_migrate import Router



db = PooledPostgresqlDatabase(
    os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=int(os.environ.get('DB_PORT', 5432)),
    max_connections=3200,
    stale_timeout=300 
)

MAX_ATTEMPTS = 10
for _ in range(MAX_ATTEMPTS):
    try:
        db.connect()
        print("Connected!")
        break
    except Exception as e:
        print("Connect failed:", e)
        time.sleep(2)
else:
    print("Could not connect.")
    exit(1)




app = Flask(__name__)
swagger = Swagger(app)




class BaseModel(Model):
    class Meta:
        database = db

class Task(BaseModel):
    text = CharField()
    description = CharField(null=True)
    done = BooleanField(default=False)




with db:
    db.create_tables([Task])

def json_response(data, status=200):
    import json
    return Response(
        json.dumps(data, ensure_ascii=False),
        status=status,
        content_type='application/json; charset=utf-8'
    )





@app.route('/')
def index():
    """
    Корневой эндпоинт (статус API)
    ---
    get:
      description: Показывает приветствие и отсчет времени до прибытия (на основе переменной окружения COUNTDOWN_TO_WHORES_ARRIVE)
      produces:
        - text/html
      responses:
        200:
          description: Успешный текстовый ответ
          content:
            text/html:
              example: Welcome! API работает, эскортницы приедут через 7 дней :)
    """
    return f"все нормально все запустилось :)"

@app.route('/api/tasks', methods=['GET'])
def get_todos():
    """
    Получить список задач
    ---
    tags:
      - Tasks
    responses:
      200:
        description: Список задач
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              text:
                type: string
              done:
                type: boolean
              description:  # Новое свойство для описания
                type: string
        examples:
          application/json: [
            {"id": 1, "text": "шакила мне в онила", "done": false, "description": "Описание задачи 1"},
            {"id": 2, "text": "булата мне в окуджаву", "done": true, "description": "Описание задачи 2"}
          ]
    """
    tasks = [
        {
            "id": task.id,
            "text": task.text,
            "done": task.done,
            "description": task.description  # добавляем description при выдаче
        }
        for task in Task.select()
    ]
    return json_response(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_todo():
    """
    Добавить задачу
    ---
    tags:
      - Tasks
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
            description:            # Новое поле для описания
              type: string
        description: Тело запроса с текстом задачи и описанием
    responses:
      201:
        description: Задача добавлена
        schema:
          type: object
          properties:
            id:
              type: integer
            text:
              type: string
            done:
              type: boolean
            description:  # Новое поле
              type: string
        examples:
          application/json:
            id: 5
            text: Помыть посуду
            done: false
            description: описание моей задачи
      400:
        description: Ошибка (нет поля text)
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json:
            error: "Поле text обязательно"
    """
    data = request.json
    if not data or "text" not in data:
        return json_response({"error": "Поле text обязательно"}, status=400)
    description = data.get("description")  # получаем description если есть
    task = Task.create(text=data["text"], description=description)
    return json_response({
        "id": task.id,
        "text": task.text,
        "done": task.done,
        "description": task.description  # отдаём description
    }, status=201)

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_todo(id):
    """
    Удалить задачу
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        required: true
        type: integer
        description: ID задачи
    responses:
      204:
        description: Успешно удалено
      404:
        description: Задача не найдена
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json:
            error: Task not found
    """
    deleted = Task.delete_by_id(id)
    if not deleted:
        return json_response({"error": "Task not found"}, status=404)
    return '', 204

@app.route('/api/tasks/<int:id>', methods=['PATCH'])
def update_task(id):
    """
    Обновить задачу
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        required: true
        type: integer
        description: ID задачи
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
            done:
              type: boolean
            description:
              type: string
        описание: Поля для обновления
    responses:
      200:
        description: Обновленная задача
        schema:
          type: object
          properties:
            id:
              type: integer
            text:
              type: string
            done:
              type: boolean
            description:  # Новое свойство
              type: string
        examples:
          application/json:
            id: 1
            text: Новое название
            done: true
            description: Обновленное описание
      400:
        description: Ошибка запроса
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json:
            error: "Нет полей для обновления (text/done/description)"
      404:
        description: Задача не найдена
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json:
            error: Task not found
    """
    data = request.json
    if not data:
        return json_response({"error": "Нужно передать данные"}, status=400)
    try:
        task = Task.get_by_id(id)
    except Task.DoesNotExist:
        return json_response({"error": "Task not found"}, status=404)
    update_data = {}
    if "text" in data:
        update_data['text'] = data["text"]
    if "done" in data:
        update_data['done'] = data["done"]
    if "description" in data:
        update_data['description'] = data["description"]
    if not update_data:
        return json_response({"error": "Нет полей для обновления (text/done/description)"}, status=400)
    Task.update(**update_data).where(Task.id == id).execute()
    task = Task.get_by_id(id)
    return json_response({
        "id": task.id,
        "text": task.text,
        "done": task.done,
        "description": task.description
    })
@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    """
    Получить задачу по id
    ---
    tags:
      - Tasks
    parameters:
      - name: task_id
        in: path
        required: true
        type: integer
        description: ID задачи
    responses:
      200:
        description: Задача
        schema:
          type: object
          properties:
            id:
              type: integer
            text:
              type: string
            done:
              type: boolean
        examples:
          application/json:
            id: 1
            text: "Купить кабачки"
            done: false
      404:
        description: Задача не найдена
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json:
            error: Task not found
    """
    try:
        task = Task.get_by_id(id)
    except Task.DoesNotExist:
        return json_response({"error": "Task not found"}, status=404)
    return json_response({
        "id": task.id, "text": task.text, "done": task.done
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
