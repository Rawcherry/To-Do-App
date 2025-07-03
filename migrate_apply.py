from peewee_migrate import Router
from app import db

router = Router(db)

if __name__ == '__main__':
    router.run()
    print("migration has been applyed")
