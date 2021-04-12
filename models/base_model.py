from peewee import Model, DateTimeField
from playhouse.db_url import connect
from khayyam import JalaliDatetime
from datetime import datetime

db = connect('mysql://Mohammad:09101916484@127.0.0.1:3306/Farsroid_Crawl')


class BaseModel(Model):
    created_time = DateTimeField(default=JalaliDatetime(datetime.now()).now())
    modified_time = DateTimeField()

    class Meta:
        database = db
