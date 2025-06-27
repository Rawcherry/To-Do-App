---

To-Do List App 

Flask-app to write down your tasks.
---
(see testing.mp4 and testing.png to see app itself)
---
---
With this app you can:

- Getting, adding, updating, and deleting tasks
- Swagger UI with auto-generated documentation
- Data is stored in PostgreSQL
- Full build and launch via Docker Compose

---
FS - Fast Start
1. Clone repo

```
git clone https://github.com/Rawcherry/To-Do-App
```
```
cd To-Do-App/
```

2. Launch app using next command
```
docker-compose up --build
```
P.S: other time start it with just using ``` docker compose up ```
P.S.S: if it`s not working just use ``` sudo ``` before composing
---
Environment variables

It`s default variables in docker-compose.yaml. You can change them to fit your needs a guess idk.

For APP:
- `DB_HOST=db`
- `DB_PORT=5432`
- `DB_NAME=tododb`
- `DB_USER=todo`
- `DB_PASSWORD=todo`

For DB:
- `POSTGRES_DB=tododb`
- `POSTGRES_USER=todo`
- `POSTGRES_PASSWORD=todo`

---
Requests examples:

Get a list of tasks

GET /tasks
curl -X GET "http://localhost:5000/api/tasks" -H "accept: application/json" 
                                                                           #it will show you 

Post a task

POST /tasks
curl -X POST "http://localhost:5000/api/tasks" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"text\": \"string\"}"                            #change string line


Patch task 

PATCH /tasks/<id>
curl -X PATCH "http://localhost:5000/api/tasks/{id}" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"done\": true, \"text\": \"string\"}"           #change id of the task and it`s states


Deleting task

DELETE /tasks/<id>
curl -X DELETE "http://localhost:5000/api/tasks/{id}" -H "accept: application/json"


---
Repo consists of:

- app.py — main code of the app
- requirements.txt — python requirements so your app works
- Dockerfile — container to start main file
- docker-compose.yaml — to start several containers at once
- wait-for-it.sh — help-script that helps with DB initialization
- frontend/ - frontend part of the app


---
Stopping container

Stopping service:
```
docker-compose down
```

Deleting containers:
```
docker-compose down -v
```

---
Technologies I used to create this ThInG

- Python 
- Flask 
- Peewee ORM
- Flasgger (Swagger UI)
- PostgreSQL 15
- Docker, Docker Compose
- React and JS on frontend


---
Features

- DB creates ONE time at building stage
- For local API test use  (http://localhost:5000) - API part
- For frontend use (http://localhost:3000) - Frontend part
- Code automatically connects to it`s docker network.


---
Creating migrations
```
docker-compose run --rm app python migrate_create.py
```.
Applying migrations
```
docker-compose run --rm app python migrate_apply.py
```
---
