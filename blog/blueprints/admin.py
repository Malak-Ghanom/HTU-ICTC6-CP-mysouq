from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from ..forms import AddCategoryForm
from blog.models import User, Item


# define our blueprint
admin_bp = Blueprint('admin', __name__)

categories= ['clothes','electrical devices','shoes','Accessories','furniture','food']

@admin_bp.route('/admin')
def admin_index():

    # get items from mango database
    items = Item.objects

    # render 'post' blueprint with posts
    return render_template('admin/index.html', items=items)


@admin_bp.route('/user/delete/<user_id>')
def delete_user(user_id):

    # get user from mango
    user = User.objects(email=user_id).first().delete()

    # get posts for the user from mango
    user_item = Item.objects(author=user_id).delete()

    # render 'profile.html' blueprint with user
    return redirect(url_for('user.get_users'))


@admin_bp.route('/users')
def get_users():

    # get all users from the mango
    users = User.objects

    # render 'list.html' blueprint with users
    return render_template('admin/users.html', users=users)


@admin_bp.route('/add/category', methods=['GET', 'POST'])
def add_category():
    global categories

    add_category_form = AddCategoryForm()

    if add_category_form.validate_on_submit():
        # read item values from the form
        new_category = add_category_form.category_name.data
        categories.append(new_category)

        flash("The new category added successfully")
        
        return redirect(url_for('admin.admin_index'))


    return render_template('admin/add-category.html', form= add_category_form, categoties= categories)


@admin_bp.route('/user/view/<id>')
def view_user(id):

    # get user from mango
    user = User()
    user.objects(_id=id)


    # render 'profile.html' blueprint with user
    return render_template('user/view-user.html', user=user, posts=posts)

