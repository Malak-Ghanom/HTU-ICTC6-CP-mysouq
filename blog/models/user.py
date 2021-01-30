from mongoengine import *
from .item import Item
# from .category import RequestedCategory, Category

class User(Document):
    # define class metadata
    meta = {'collection': 'users', 'allow_inheritance': True}

    # define class fields
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    email = EmailField(required=True, primary_key=True)
    password = StringField(required=True)
    birthdate = DateField(max_length=50)
    picture_url = StringField()
    role = StringField()
    active = BooleanField(default=True)

class Reseller(User):
    meta = {'collection': 'resellers'}
    item = ListField(ReferenceField(Item))

class Buyer(User):
    # meta = {'collection': 'buyers'}
    favorites_list = ListField(StringField(default=None))
    buy_requests = ListField(StringField(default=None))


class Admin(User):
    meta = {'collection': 'admin'}

    # categories = ListField(ReferenceField(Category))
    # requested_categories = ListField(ReferenceField(RequestedCategory))

    pass