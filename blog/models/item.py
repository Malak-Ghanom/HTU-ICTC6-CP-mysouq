from mongoengine import *
# from .user import Reseller


class Item(Document):
    # meta = {'collection': 'items', 'allow_inheritance': True}

    author = StringField()
    title = StringField(max_length=120)
    description = StringField()
    price = StringField()
    category = StringField()
    visibility = BooleanField(default=True)
    quantity = IntField()