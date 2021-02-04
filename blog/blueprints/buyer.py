from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from blog.models import Item, Buyer, Admin, BuyRequest, User, UpgradeToReseller
from ..forms import EditUserForm, ChangePasswordForm, TextSearchForm

# define buyer blueprint
buyer_bp = Blueprint('buyer', __name__)

# check mode if it is under maintenance or not
@buyer_bp.route('/buyer')
def check_mode():

    # get admin to check if the web app is in maintenance mode
    admin = Admin.objects.first()

    if admin.under_maintenance == True:
        return render_template('admin/maintenance-mode.html')
    else:
        return redirect(url_for('buyer.buyer_index'))


#buyer home page contains all of the available items
@buyer_bp.route('/buyer/index')
def buyer_index():

    # get buyer requests and calculate number of requests (buyer cart)
    buy_requests = BuyRequest.objects.get_buyer_requests()
    buy_requests_number = len(buy_requests)

    # get souq items
    items = Item.objects
    buyer = Buyer.objects(email=session['uid']).first()
    session['upgraded'] = buyer.upgraded_to_reseller

    # get notifications number
    notifications_number = len(buyer.notifications)

    # render index template
    return render_template('buyer/index.html', items=items,notifications_number=notifications_number, notifications= buyer.notifications[::-1], buy_requests_number=buy_requests_number)


@buyer_bp.route('/price/ascending')
def price_ascending():

    #get souq items ordered by price ascending
    items = Item.objects.price_ascending()

    # render index template
    return render_template('buyer/index.html', items=items)


@buyer_bp.route('/price/descending')
def price_descending():

    #get souq items ordered by price descending
    items = Item.objects.price_descending()

    # render index template
    return render_template('buyer/index.html', items=items)


@buyer_bp.route('/date/ascending')
def date_ascending():

    #get souq items ordered by date ascending
    items = Item.objects.date_ascending()
    
    # render index template
    return render_template('buyer/index.html', items=items)


@buyer_bp.route('/date/descending')
def date_descending():

    # get souq items ordered by date descending
    items = Item.objects.date_descending()

    # render index template
    return render_template('buyer/index.html', items=items)


@buyer_bp.route('/add/fav/<item_id>')
def add_to_favorite(item_id):

    # get buyer
    buyer = Buyer.objects(email= session['uid']).first()

    # check if the item already exist
    if item_id not in buyer.favorites_list:
        buyer.favorites_list.append(item_id)
        buyer.save()

    # get favorites items
    favorite_items=[]
    for item_id in buyer.favorites_list:
        item = Item.objects(id=item_id).first()
        favorite_items.append(item)

    # render favorite-list template
    return render_template('buyer/favorite-list.html', favorite_items = favorite_items)


@buyer_bp.route('/buy/item/<item_id>')
def buy_item(item_id):

    # get item and save buyer id in item buyers
    item = Item.objects(id=item_id).first()
    item.buyers.append(session['uid'])
    item.save()

    # add the buy request to the reseller
    buy_request = BuyRequest(buyer_id= session['uid'], item=item, status='pending', reseller_id= item.author).save()

    # get all buyer requests for the buyer
    buy_requests = BuyRequest.objects.get_buyer_requests()

    # notify reseller 
    reseller = User.objects(email= item.author).first()
    notification = session['uid'] +" request to buy item '"+ item.title + "' from you"
    reseller.notifications.append(notification)
    reseller.save()

    # redirect to the buy requests list
    return redirect(url_for('buyer.buyer_requests'))


@buyer_bp.route('/buyer/requests')
def buyer_requests():

    # get buyer requests
    buy_requests = BuyRequest.objects.get_buyer_requests()

    # render buy requests list
    return render_template('buyer/buyer-requests.html', buy_requests = buy_requests)


@buyer_bp.route('/search', methods=['GET', 'POST'])
def search_item():

    # instance from search form
    search_form = TextSearchForm()

    # if mothod is POST
    if search_form.validate_on_submit():

        # read value from the search form
        keyword = search_form.keyword.data
        # get results
        results = Item.objects.search_text(keyword).order_by('$text_score')

        # render result template
        return render_template('buyer/search-result.html', items=results)

    # if methos is GET render search template
    return render_template('buyer/search.html', form=search_form, title="Search", icon="fas fa-search")


@buyer_bp.route('/upgrade/<buyer_id>')
def reseller_upgrade(buyer_id):

    # add upgrade request to mongodb
    request = UpgradeToReseller(buyer_id= buyer_id, first_name= session['first_name'], last_name= session['last_name']).save()

    # display msg to the buyer to infom him that the procces completed successfuly
    flash("Your Request sent successfuly")

    # redirect to view user template
    return redirect(url_for('user.view_user', user_id=buyer_id))