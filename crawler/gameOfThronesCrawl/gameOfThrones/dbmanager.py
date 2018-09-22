from peewee import Model
from peewee import SqliteDatabase
from peewee import CharField
from peewee import TextField
from peewee import IntegerField
import re

db = SqliteDatabase('gameOfThrones.db')

class BaseModel(Model):
    class Meta:
        database = db


class Role(BaseModel):
    level = IntegerField()
    name = TextField()
    avator = TextField()
    main_info = TextField()

    class Meta:
        db_table = 'role'
        order_by = ('role_id', 'name')


def create_table(table):
    if not table.table_exists():
        table.create_table()

def save_roles(item):
    print('save_roles ===== ' + str(item))
    name_str = item['name'][0]
    avator_str = item['avator'][0]
    main_info_str = ''.join(item['main_info'])
    main_info_str = re.sub('\s', '', main_info_str) 
    main_info_str = re.sub('\[\d+\]', '', main_info_str)

    with db.atomic():
        Role.create(level=item['level'], name=name_str, avator=avator_str, main_info=main_info_str)

    #     for i in roles:
    #         Role.create(**i)
        # for i in range(0, len(roles), 100):
            # Role.insert_many(roles[i: i+100).execute()

