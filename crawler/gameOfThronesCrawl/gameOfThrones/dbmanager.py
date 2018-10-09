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


class Pov(BaseModel):
    level = IntegerField()
    name = TextField()
    avator = TextField()
    main_info = TextField()
    appearance = TextField()
    history = TextField()
    event_book = TextField()
    event_detail = TextField()
    # tv_show = TextField()

    class Meta:
        db_table = 'pov'
        order_by = ('level', 'name')


def create_table(table):
    if not table.table_exists():
        table.create_table()

def save_povs(item):
    name_str = item['name'][0]
    avator_str = item['avator'][0]
    main_info_str = format_info(item['main_info'])
    
    if 'appearance' in item:
        appearance = format_info(item['appearance'])
    else:
        appearance = ''

    if 'history' in item:
        history = format_info(item['history'])
    else:
        history = ''

    if 'event_book' in item:
        event_book = '&&'.join(item['event_book'])
    else:
        event_book = ''

    if 'event_detail' in item:
        event_detail = '&&'.join(item['event_detail'])
    else:
        event_detail = ''

    with db.atomic():
        Pov.create(level=item['level'], name=name_str, avator=avator_str, main_info=main_info_str,
            appearance=appearance, history=history, event_book=event_book, event_detail=event_detail)

    #     for i in povs:
    #         Pov.create(**i)
        # for i in range(0, len(povs), 100):
            # .insert_many(povs[i: i+100).execute()

def format_info(info):
    info = ''.join(info)
    # info = re.sub('\s', '', info)
    info = re.sub('\[\d+\]', '', info)

    return info
