"""Peewee migrations -- 001_auto.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""
from contextlib import suppress
from peewee import Model, CharField, BooleanField
import peewee as pw
from peewee_migrate import Migrator

import sys
sys.path.insert(0, '.')

import app
database = app.db

with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext                         #there were problems with value errors
                                                                     #so i fixed it like this by directly importing database
class Task(Model):
    text = CharField()
    done = BooleanField()
    description = pw.TextField(null=True)

    class Meta:
        database = database

def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.add_fields(Task, description=pw.TextField(null=True))                  #here you write your migration
    
def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    migrator.remove_fields(Task, 'description')             
