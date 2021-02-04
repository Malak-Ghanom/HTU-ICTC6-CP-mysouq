from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from blog.models import Item, Reseller, User, Category, RequestCategory, Admin, BuyRequest, Buyer
from ..forms import AddItemForm, EditItemForm, RequestCategoryForm
from datetime import datetime

# define reseller blueprint
reseller_bp = Blueprint('reseller', __name__)


@reseller_bp.route('/reseller/mode')
def check_mode():

    # get admin to check if the web app is in maintenance mode
    admin = Admin.objects.first()

    if admin.under_maintenance == True:
        return render_template('admin/maintenance-mode.html')
    else:
        return redirect(url_for('reseller.reseller_index'))


@reseller_bp.route('/reseller')
def reseller_index():

    # get items from mangodb
    items = Item.objects
    reseller = User.objects(email=session['uid']).first()

    # get notifications and number of it
    notifications = reseller.notifications
    notifications_number = len(notifications)

    # get buy request and number of it
    buy_requests = BuyRequest.objects.get_reseller_pending_requests()
    buy_requests_number = len(buy_requests)
    
    # render index template with the above info
    return render_template('reseller/index.html', items=items, notifications_number=notifications_number, notifications=notifications[::-1], buy_requests_number=buy_requests_number)


@reseller_bp.route('/reseller/items')
def reseller_items():

    # get items from mango database
    items = Item.objects(author=session['uid'])

    # render 'reseller-items' template with items
    return render_template('reseller/reseller-items.html', items=items)


@reseller_bp.route('/request/category', methods=['GET', 'POST'])
def request_category():

    # create instance from RequestedCategory form
    request_category_form = RequestCategoryForm()

    # handle the submission
    if request_category_form.validate_on_submit():

        # read the values from the form
        requested_category = request_category_form.category_name.data

        # get categories to check if the category already exist or not
        categories= [category['name'] for category in Category.objects]

        if requested_category not in categories:

            category = RequestCategory(name=requested_category, user= session['uid'], time= datetime.now()).save()
            flash("Your request is pendding confirmation")

        else:
            flash("Category already exist")

        return redirect(url_for('reseller.reseller_index'))

    # if method is GET render request nnew category template
    return render_template('reseller/request-new-category.html', form= request_category_form)


@reseller_bp.route('/add/item', methods=['GET', 'POST'])
def add_item():

    # get categories from mongodb
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

        # if the page requested by the upgraded buyer redirect to buyer index
        if session['role'] == 'Buyer':
            return redirect(url_for('buyer.buyer_index'))

        # redirect to reseller index
        return redirect(url_for('reseller.reseller_index'))

    # if method is GET render the add-item template
    return render_template("reseller/add-item.html", form=add_item_form)


@reseller_bp.route('/delete/item/<item_id>')
def delete_item(item_id):

    # get item by id  from mongodb
    item = Item.objects(id=item_id).first()

    # if there is no buy request on this item delete it 
    if item.buy_requests == 0:
        item.delete()
    
    # inform reseller to solve buy request first
    else:
        flash("Can't delete item, please solve the buy request first.")

    # redirect to reseller index
    return redirect(url_for('reseller.reseller_index'))


@reseller_bp.route('/item/edit/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):

    # get required item by id
    item = Item.objects(id= item_id).first()

    # get categories list
    categories= [category['name'] for category in Category.objects]

    # create instance of edit form
    edit_item_form = EditItemForm()
    edit_item_form.category.choices = categories

    # write data on the template fields
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

        #  flash a msg to inform the reseller that the item updated successfuly
        flash("item information updated successfully!")

        # redirect to reseller index
        return redirect(url_for('reseller.reseller_index'))

    # if method is GET redner the edit item template
    return render_template("reseller/edit-item.html", form=edit_item_form)


@reseller_bp.route('/hide/item/<item_id>')
def hide_item(item_id):

    # get item from mongodb and change visibility to false
    item = Item.objects(id= item_id).first()
    item.visibility = False
    item.save()

    # redirect to reseller home page
    return redirect(url_for('reseller.reseller_index'))


@reseller_bp.route('/unhide/item/<item_id>')
def unhide_item(item_id):

    # get item from mongodb and change visibility to true
    item = Item.objects(id= item_id).first()
    item.visibility = True
    item.save()

    # redirect to reseller home page
    return redirect(url_for('reseller.reseller_index'))


@reseller_bp.route('/buy/requests')
def buy_requests():

    # get buy request on the reseller item from mongodb
    buy_requests = BuyRequest.objects.get_reseller_pending_requests()

    # render buy requests list template
    return render_template('reseller/buy-requests.html', buy_requests = buy_requests)


@reseller_bp.route('/approve/buy/request/<request_id>')
def approve_buy_request(request_id):

    # get buy requests from mongodb
    buy_request = BuyRequest.objects(id=request_id).first()

    # get buyer of the request from mongoodb to notify him
    buyer = Buyer.objects(email=buy_request.buyer_id).first()
    notification = "Your request to buy item '<b>"+ item.title + "</b>' has been approved"
    buyer.notifications.append(notification)
    buyer.save()

    # get item from mongodb to check quantity
    item_id = buy_request.item.id
    item = Item.objects(id=item_id).first()

    # if there is enough item then approve request and sell item
    if item.quantity >= 1:
        item.quantity -=1
        item.save()
        buy_request.status = 'approved'
        buy_request.save()

    # if there is no enough item decline request
    else:
        item.delete()
        buy_request.status = 'declined'
        buy_request.save()


    return redirect(url_for('reseller.buy_requests'))


@reseller_bp.route('/decline/buy/request/<request_id>')
def decline_buy_request(request_id):

    # get buy requests from mongodb
    buy_request = BuyRequest.objects(id=request_id).first()

    # get buyer of the request from mongoodb to notify him
    buyer = Buyer.objects(email=buy_request.buyer_id).first()
    notification = "Your request to buy item '"+ buy_request.item.title + "' has been declined"
    buyer.notifications.append(notification)
    buyer.save()

    # change request state
    buy_request.status = 'declined'
    buy_request.save()

    # redirect to buy requests
    return redirect(url_for('reseller.buy_requests'))