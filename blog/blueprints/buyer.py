from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from blog.models import Item, Buyer, Admin, BuyRequest, User, UpgradeToReseller
from ..forms import EditUserForm, ChangePasswordForm, TextSearchForm

buyer_bp = Blueprint('buyer', __name__)

@buyer_bp.route('/buyer')
def check_mode():

    admin = Admin.objects.first()
    if admin.under_maintenance == True:
        return 'the system is under maintenance'
    else:
        return redirect(url_for('buyer.buyer_index'))

#buyer home page contains all of the available items
@buyer_bp.route('/buyer/index')
def buyer_index():

    buy_requests = BuyRequest.objects.get_buyer_requests()
    buy_requests_number = len(buy_requests)

    items = Item.objects
    buyer = Buyer.objects(email=session['uid']).first()
    session['upgraded'] = buyer.upgraded_to_reseller

    notifications_number = len(buyer.notifications)
    # print(favorite_items.favorite)
    return render_template('buyer/index.html', items=items,notifications_number=notifications_number, notifications= buyer.notifications, buy_requests_number=buy_requests_number)

@buyer_bp.route('/price/ascending')
def price_ascending():

    items = Item.objects.price_ascending()
    buyer = Buyer.objects(email=session['uid']).first()
    # print(favorite_items.favorite)
    return render_template('buyer/index.html', items=items, favorite_items= buyer.favorites_list)

@buyer_bp.route('/price/descending')
def price_descending():

    items = Item.objects.price_descending()
    buyer = Buyer.objects(email=session['uid']).first()
    # print(favorite_items.favorite)
    return render_template('buyer/index.html', items=items, favorite_items= buyer.favorites_list)

@buyer_bp.route('/date/ascending')
def date_ascending():

    items = Item.objects.date_ascending()
    buyer = Buyer.objects(email=session['uid']).first()
    # print(favorite_items.favorite)
    return render_template('buyer/index.html', items=items, favorite_items= buyer.favorites_list)

@buyer_bp.route('/date/descending')
def date_descending():

    items = Item.objects.date_descending()
    buyer = Buyer.objects(email=session['uid']).first()
    # print(favorite_items.favorite)
    return render_template('buyer/index.html', items=items, favorite_items= buyer.favorites_list)


@buyer_bp.route('/add/fav/<item_id>')
def add_to_favorite(item_id):
    
    buyer = Buyer.objects(email= session['uid']).first()

    if item_id not in buyer.favorites_list:
            
        buyer.favorites_list.append(item_id)
        buyer.save()


    # list_id= Buyer.objects(email=session['uid']).first()
    favorite_items=[]

    for item_id in buyer.favorites_list:
        item = Item.objects(id=item_id).first()
        favorite_items.append(item)

    # return redirect(url_for('buyer.buyer_index'))
    return render_template('buyer/favorite-list.html', favorite_items = favorite_items)


@buyer_bp.route('/buy/item/<item_id>')
def buy_item(item_id):

    
    item = Item.objects(id=item_id).first()
    item.buyers.append(session['uid'])
    item.save()

    buy_request = BuyRequest(buyer_id= session['uid'], item=item, status='pending', reseller_id= item.author).save()

    buy_requests = BuyRequest.objects.get_buyer_requests()
    reseller = User.objects(email= item.author).first()

    notification = session['uid'] +" request to buy item '"+ item.title + "' from you"
    reseller.notifications.append(notification)
    reseller.save()


    return redirect(url_for('buyer.buyer_requests'))

@buyer_bp.route('/buyer/requests')
def buyer_requests():

    buy_requests = BuyRequest.objects.get_buyer_requests()


    return render_template('buyer/buyer-requests.html', buy_requests = buy_requests)


@buyer_bp.route('/search', methods=['GET', 'POST'])
def search_item():

    search_form = TextSearchForm()
    buyer = Buyer.objects(email=session['uid']).first()

    if search_form.validate_on_submit():
        keyword = search_form.keyword.data
        results = Item.objects.search_text(keyword).order_by('$text_score')


        return render_template('buyer/search-result.html', items=results, favorite_items= buyer.favorites_list)

    return render_template('buyer/search.html', form=search_form, title="Search", icon="fas fa-search")


@buyer_bp.route('/upgrade/<buyer_id>')
def reseller_upgrade(buyer_id):
    
    request = UpgradeToReseller()
    request.buyer_id= buyer_id
    request.first_name= session['first_name']
    request.last_name= session['last_name']
    request.save()

    flash("Your Request sent successfuly")

    return redirect(url_for('buyer.view_buyer', buyer_id=buyer_id))