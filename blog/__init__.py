import os

from flask import Flask
from mongoengine import *
from blog.models import *
import json


def create_app(test_config=None):
    # create the Flask
    app = Flask(__name__, instance_relative_config=True)

    # configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI="mongodb://root:example@localhost:27017/blog?authSource=admin"
    )

    # connect to MongoDB using mongoengine
    connect(
        db='blog',
        username='root',
        password='example',
        authentication_source='admin'
    )

    @app.route('/dummy')
    def dummy():

        # drop collection before initialization
        User.drop_collection()
        Buyer.drop_collection()
        Admin.drop_collection()
        Reseller.drop_collection()
        Item.drop_collection()
        Category.drop_collection()
        RequestCategory.drop_collection()
        BuyRequest.drop_collection()

        buyer = Buyer(email='malak@gmail.com', first_name='malak',
                      last_name='ghanom', password='0000', birthdate='1996-2-7', role='Buyer').save()
        reseller = Reseller(email='adam@gmail.com', first_name='adam',
                            last_name='ahmad', password='0000', birthdate='1996-3-15', role='Reseller').save()
        admin = Admin(email='ahmad@gmail.com', first_name='ahmad',
                      last_name='alnadi', password='0000', birthdate='1996-6-3', role= 'Admin').save()

        item1 = Item(author='adam@gmail.com', title='laptop', description='dell, 8G RAM, core i7',
                     price=200, category='electrical devices', visibility=True, quantity=2, buyers=['malak@gmail.com']).save()
        item2 = Item(author='adam@gmail.com', title='wedding dress', description='ivory',
                     price=300, category='dresses', visibility=True, quantity=9, buyers=['malak@gmail.com']).save()

        category1 = Category(name='electrical devices').save()
        category2 = Category(name='dresses').save()

        requested_category1 = RequestCategory(
            name='smart things', user='adam@gmail.com').save()
        requested_category1 = RequestCategory(
            name='t-shirts', user='adam@gmail.com').save()

        return "database initialized successfully"

    # register the 'user' blueprint
    from .blueprints.user import user_bp
    app.register_blueprint(user_bp)

    # register the 'login' blueprint
    from .blueprints.login import login_bp
    app.register_blueprint(login_bp)

    # register the 'reseller' blueprint
    from .blueprints.reseller import reseller_bp
    app.register_blueprint(reseller_bp)

    # register the 'admin' blueprint
    from .blueprints.admin import admin_bp
    app.register_blueprint(admin_bp)

    # register the 'buyer' blueprint
    from .blueprints.buyer import buyer_bp
    app.register_blueprint(buyer_bp)

    return app
