from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from blog.models import Item, Reseller, User, Category, RequestCategory, Admin, BuyRequest
from ..forms import AddItemForm, EditItemForm, RequestCategoryForm
from datetime import datetime

reseller_bp = Blueprint('reseller', __name__)

@reseller_bp.route('/reseller/mode')
def check_mode():

    admin = Admin.objects.first()
    if admin.under_maintenance == True:
        return 'the system is under maintenance'
    else:
        return redirect(url_for('reseller.reseller_index'))


@reseller_bp.route('/reseller')
def reseller_index():

    # get items from mango database
    items = Item.objects
    reseller = User.objects(email=session['uid']).first()
    notifications = reseller.notifications

    # render 'post' blueprint with posts
    return render_template('reseller/index.html', items=items, notifications=notifications)


@reseller_bp.route('/reseller/items')
def reseller_items():

    # get items from mango database
    items = Item.objects(author=session['uid'])

    # render 'post' blueprint with posts
    return render_template('reseller/reseller-items.html', items=items)


@reseller_bp.route('/request/category', methods=['GET', 'POST'])
def request_category():

    request_category_form = RequestCategoryForm()

    if request_category_form.validate_on_submit():
        # read item values from the form

        requested_category = request_category_form.category_name.data
        
        categories= [category['name'] for category in Category.objects]
                
        if requested_category not in categories:
            category = RequestCategory(name=requested_category, user= session['uid'], time= datetime.now()).save()
            flash("Your request is pendding confirmation")
        else:
            flash("Category already exist")
        
        return redirect(url_for('reseller.reseller_index'))

    return render_template('reseller/request-new-category.html', form= request_category_form)


@reseller_bp.route('/add/item', methods=['GET', 'POST'])
def add_item():

    categories= [category['name'] for category in Category.objects]

    # create instance of our form
    add_item_form = AddItemForm()
    add_item_form.category.choices = categories

    # handle form submission
    if add_item_form.validate_on_submit():

        # read item values from the form
        category = add_item_form.category.data
        price = add_item_form.price.data
        title = add_item_form.title.data
        description = add_item_form.description.data
        quantity = add_item_form.quantity.data
        author = session['uid']
        item = Item(category=category, price=price,
                    title=title, description=description, author=author, quantity=quantity).save()

        return redirect(url_for('reseller.reseller_index'))

    # render the template
    return render_template("reseller/add-item.html", form=add_item_form)


@reseller_bp.route('/delete/item/<item_id>')
def delete_item(item_id):

    item = Item.objects(id=item_id).first()
    
    if item.buy_requests == 0:
        item.delete()
    else:
        flash("Can't delete item, please solve the buy request first.")

    return redirect(url_for('reseller.reseller_index'))


@reseller_bp.route('/item/edit/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):

    item = Item.objects(id= item_id).first()

    categories= [category['name'] for category in Category.objects]

    # create instance of our form
    edit_item_form = EditItemForm()
    edit_item_form.category.choices = categories

    if request.method == "GET":
        edit_item_form.category.data = item.category
        edit_item_form.price.data = item.price
        edit_item_form.title.data = item.title
        edit_item_form.description.data = item.description
        edit_item_form.quantity.data = item.quantity

    # handle form submission

    if edit_item_form.validate_on_submit():

        # read item values from the form
        category = edit_item_form.category.data
        price = edit_item_form.price.data
        title = edit_item_form.title.data
        description = edit_item_form.description.data
        quantity = edit_item_form.quantity.data
        item = Item.objects(id= item_id).update(category=category, price=price, title=title, description=description, quantity=quantity)

        #  flash masseag
        flash("item information updated successfully!")

        # redirect
        return redirect(url_for('reseller.reseller_index'))

    # redner the login template
    return render_template("reseller/edit-item.html", form=edit_item_form)


@reseller_bp.route('/hide/item/<item_id>')
def hide_item(item_id):

    item = Item.objects(id= item_id).first()
    item.visibility = False
    item.save()

    return redirect(url_for('reseller.reseller_index'))

@reseller_bp.route('/unhide/item/<item_id>')
def unhide_item(item_id):

    item = Item.objects(id= item_id).first()
    item.visibility = True
    item.save()

    return redirect(url_for('reseller.reseller_index'))


@reseller_bp.route('/buy/requests')
def buy_requests():
    
    buy_requests = BuyRequest.objects.get_reseller_pending_requests()

    return render_template('reseller/buy-requests.html', buy_requests = buy_requests)


@reseller_bp.route('/approve/buy/request/<request_id>')
def approve_buy_request(request_id):
    
    buy_request = BuyRequest.objects(id=request_id).first()
    item_id = buy_request.item.id

    item = Item.objects(id=item_id).first()

    if item.visibility == True:
        if item.quantity >= 1:
            item.quantity -=1
            buy_request.status = 'approved'
            buy_request.save()
        else:
            item.delete()
            buy_request.status = 'declined'
            buy_request.save()

    return redirect(url_for('reseller.buy_requests'))


@reseller_bp.route('/decline/buy/request/<request_id>')
def decline_buy_request(request_id):
    
    buy_request = BuyRequest.objects(id=request_id).first()

    buy_request.status = 'declined'
    buy_request.save()

    return redirect(url_for('reseller.buy_requests'))

