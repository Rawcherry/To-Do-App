import os
import time
from flask import Flask, request, Response
from flasgger import Swagger
from peewee import Model, CharField, BooleanField
from playhouse.pool import PooledPostgresqlDatabase
from peewee import OperationalError



db = PooledPostgresqlDatabase(
    os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=int(os.environ.get('DB_PORT', 5432)),
    max_connections=32,
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

@app.route('/tasks', methods=['GET'])
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
        examples:
          application/json: [
            {"id": 1, "text": "шакила мне в онила", "done": false},
            {"id": 2, "text": "булата мне в окуджаву", "done": true}
          ]
    """
    tasks = [{"id": task.id, "text": task.text, "done": task.done} for task in Task.select()]
    return json_response(tasks)

@app.route('/tasks', methods=['POST'])
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
        description: Тело запроса с текстом задачи
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
        examples:
          application/json:
            id: 5
            text: Помыть посуду
            done: false
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
    task = Task.create(text=data["text"])
    return json_response({"id": task.id, "text": task.text, "done": task.done}, status=201)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_todo(task_id):
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
    deleted = Task.delete_by_id(task_id)
    if not deleted:
        return json_response({"error": "Task not found"}, status=404)
    return '', 204

@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
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
        description: Обновляемые поля задачи
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
        examples:
          application/json:
            id: 1
            text: Новое название
            done: true
      400:
        description: Ошибка запроса
        schema:
          type: object
          properties:
            error:
              type: string
        examples:
          application/json:
            error: "Нет полей для обновления (text/done)"
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
        task = Task.get_by_id(task_id)
    except Task.DoesNotExist:
        return json_response({"error": "Task not found"}, status=404)
    update_data = {}
    if "text" in data:
        update_data['text'] = data["text"]
    if "done" in data:
        update_data['done'] = data["done"]
    if not update_data:
        return json_response({"error": "Нет полей для обновления (text/done)"}, status=400)
    Task.update(**update_data).where(Task.id == task_id).execute()
    # Получаем обновленную задачу
    task = Task.get_by_id(task_id)
    return json_response({"id": task.id, "text": task.text, "done": task.done})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
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
        task = Task.get_by_id(task_id)
    except Task.DoesNotExist:
        return json_response({"error": "Task not found"}, status=404)
    return json_response({
        "id": task.id, "text": task.text, "done": task.done
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1488)