from mongoengine import *
# from .user import Reseller
from datetime import datetime
from flask import session


class ItemQuerySet(QuerySet):

    def price_ascending(self):
        return self.filter(visibility=True).order_by('+price')

    def price_descending(self):
        return self.filter(visibility=True).order_by('-price')

    def date_ascending(self):
        return self.filter(visibility=True).order_by('+date')

    def date_descending(self):
        return self.filter(visibility=True).order_by('-date')


class Item(Document):
    meta = {'collection': 'items', 'queryset_class': ItemQuerySet, 'allow_inheritance': True, 'indexes':
            [
                {'fields': ['$title', '$description', '$category'],
                'default_language': 'english',
                'weights': {'category': 10, 'title': 8, 'description': 6}
                }
            ]}

    author = StringField()
    title = StringField(max_length=120)
    description = StringField()
    price = IntField()
    category = StringField()
    visibility = BooleanField(default=True)
    quantity = IntField()
    date = DateTimeField(default=datetime.now())
    buyers = ListField(StringField())


class BuyRequestQuerySet(QuerySet):

    def get_buyer_requests(self):
        return self.filter(buyer_id= session['uid']).order_by('-id')

    def get_reseller_pending_requests(self):
        return self.filter(reseller_id= session['uid'], status= 'pending').order_by('-id')



class BuyRequest(Document):

    meta = {'queryset_class': BuyRequestQuerySet}

    buyer_id = StringField()
    item = ReferenceField(Item)
    status = StringField()
    reseller_id = StringField()