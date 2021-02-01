from mongoengine import *
from .items import Item, BuyRequest
# from .category import RequestedCategory, Category

maintenance = False

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
    notifications = ListField(StringField(default=None))


class Reseller(User):

    item = ListField(ReferenceField(Item))

class Buyer(User):

    favorites_list = ListField(StringField(default=None))


class Admin(User):

    under_maintenance= BooleanField(default=False)