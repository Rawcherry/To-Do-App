from peewee_migrate import Router
from app import db, Task  

router = Router(db)

if __name__ == '__main__':
    router.create()
    print("migration has been created")
