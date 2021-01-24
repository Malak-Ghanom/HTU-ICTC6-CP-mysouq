from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from blog.models import Item, Reseller, User
from ..forms import AddItemForm, EditItemForm, RequestCategoryForm
from .admin import categories

reseller_bp = Blueprint('reseller', __name__)


@reseller_bp.route('/reseller')
def reseller_index():

    # get items from mango database
    items = Item.objects

    # render 'post' blueprint with posts
    return render_template('reseller/index.html', items=items)

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

        flash("Your request is pendding confirmation")
        
        return redirect(url_for('reseller.reseller_index'))


    return render_template('reseller/request-new-category.html', form= request_category_form)


@reseller_bp.route('/add/item', methods=['GET', 'POST'])
def add_item():

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
        author = session['uid']
        item = Item(category=category, price=price,
                    title=title, description=description, author=author).save()

        return redirect(url_for('reseller.reseller_index'))

    # render the template
    return render_template("reseller/add-item.html", form=add_item_form)


@reseller_bp.route('/delete/item/<item_id>')
def delete_item(item_id):

    item = Item.objects(id=item_id).first().delete()

    return redirect(url_for('reseller.reseller_index'))



@reseller_bp.route('/item/edit/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):

    item = Item.objects(id= item_id).first()

    # create instance of our form
    edit_item_form = EditItemForm()
    edit_item_form.category.choices = categories

    if request.method == "GET":
        edit_item_form.category.data = item.category
        edit_item_form.price.data = item.price
        edit_item_form.title.data = item.title
        edit_item_form.description.data = item.description

    # handle form submission

    if edit_item_form.validate_on_submit():

        # read item values from the form
        category = edit_item_form.category.data
        price = edit_item_form.price.data
        title = edit_item_form.title.data
        description = edit_item_form.description.data
        item = Item.objects(id= item_id).update(category=category, price=price, title=title, description=description)

        #  flash masseag
        flash("item information updated successfully!")

        # redirect
        return redirect(url_for('reseller.reseller_index'))

    # redner the login template
    return render_template("reseller/edit-item.html", form=edit_item_form)



