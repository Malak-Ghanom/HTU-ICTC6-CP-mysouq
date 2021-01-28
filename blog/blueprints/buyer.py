from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from blog.models import Item, Reseller, User, Category, RequestCategory, Buyer
from ..forms import AddItemForm, EditItemForm, RequestCategoryForm, EditUserForm,ChangePasswordForm
from datetime import datetime

buyer_bp = Blueprint('buyer', __name__)

#buyer home page contains all of the available items
@buyer_bp.route('/buyer/index')
def buyer_index():

    items = Item.objects

    return render_template('buyer/index.html', items=items)

@buyer_bp.route('/buyer/profile/<buyer_id>')
def view_buyer(buyer_id):

    # get buyer from mango
    buyer = User.objects(email=buyer_id).first()
    print(buyer)
    
    # render 'profile.html' blueprint with user
    return render_template('buyer/view-buyer.html', buyer=buyer)

@buyer_bp.route('/edit/buyer/<buyer_id>', methods=['GET', 'POST'])
def edit_buyer(buyer_id):

    buyer = User.objects(email= buyer_id).first()


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
        buyer = User.objects(email=buyer_id).update(first_name=first_name, last_name=last_name, picture_url=picture_url)

        buyer = User.objects(email= buyer_id).first()
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
