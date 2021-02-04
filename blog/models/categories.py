from mongoengine import *


class Category(Document):

    meta = {'collection': 'Category'}

    name = StringField()


class RequestCategory(Document):

    meta = {'collection': 'Requested Category'}

    name= StringField()
    user= StringField()
    time= DateTimeField()


