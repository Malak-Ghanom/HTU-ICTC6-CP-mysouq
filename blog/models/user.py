from mongoengine import *
from .item import Item

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

class Reseller(User):
    meta = {'collection': 'resellers', 'allow_inheritance': True}
    item = ListField(ReferenceField(Item))


class Buyers(User):
    meta = {'collection': 'buyers', 'allow_inheritance': True}
    favorite = ListField()

class Admin(User):
    meta = {'collection': 'admin', 'allow_inheritance': True}
    pass