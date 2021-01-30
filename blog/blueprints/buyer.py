from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from blog.models import Item, Buyer
from ..forms import EditUserForm, ChangePasswordForm

buyer_bp = Blueprint('buyer', __name__)

#buyer home page contains all of the available items
@buyer_bp.route('/buyer/index')
def buyer_index():

    items = Item.objects
    buyer = Buyer.objects(email=session['uid']).first()
    # print(favorite_items.favorite)
    return render_template('buyer/index.html', items=items, favorite_items= buyer.favorites_list)

@buyer_bp.route('/buyer/profile/<buyer_id>')
def view_buyer(buyer_id):

    # get buyer from mango
    buyer = Buyer.objects(email=buyer_id).first()
    
    # render 'profile.html' blueprint with user
    return render_template('buyer/view-buyer.html', buyer=buyer)

@buyer_bp.route('/edit/buyer/<buyer_id>', methods=['GET', 'POST'])
def edit_buyer(buyer_id):

    buyer = Buyer.objects(email= buyer_id).first()


    # create instance of our form
    edit_user_form = EditUserForm()
    if request.method == "GET":
        edit_user_form.first_name.data = buyer.first_name
        edit_user_form.last_name.data = buyer.last_name
        edit_user_form.picture_url.data = ''

    # handle form submission

    if edit_user_form.validate_on_submit():

        # read post values from the form
        first_name = edit_user_form.first_name.data
        last_name = edit_user_form.last_name.data
        picture_url = edit_user_form.picture_url.data

        # save data
        buyer = Buyer.objects(email=buyer_id).update(first_name=first_name, last_name=last_name, picture_url=picture_url)

        buyer = Buyer.objects(email= buyer_id).first()
        # update session
        session['first_name'] = buyer.first_name
        session['last_name'] = buyer.last_name
        session['picture_url'] = buyer.picture_url

        #  flash masseag
        flash("User information updated successfully!")

            # redirect
        return redirect(url_for('buyer.view_buyer', buyer_id=session['uid']))

    # redner the login template
    return render_template("user/edit-user.html", form=edit_user_form)

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
    item.buy_requests.append(session['uid'])
    item.save()

    buyer = Buyer.objects(email= session['uid']).first()
    
    buyer.buy_requests.append(item_id)
    buyer.save()


    # list_id= Buyer.objects(email=session['uid']).first()
    buy_requests=[]

    for item_id in buyer.buy_requests:
        item = Item.objects(id=item_id).first()
        buy_requests.append(item)


    return render_template('buyer/buy-requests.html', buy_requests = buy_requests)