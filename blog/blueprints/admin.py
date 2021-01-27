from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from ..forms import AddCategoryForm
from blog.models import User, Item, Category, RequestCategory
# from .reseller import requested_categories


# define our blueprint
admin_bp = Blueprint('admin', __name__)

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

@admin_bp.route('/admin/delete/item/<item_id>')
def admin_delete_item(item_id):

    item = Item.objects(id=item_id).first().delete()

    return redirect(url_for('admin.admin_index'))

@admin_bp.route('/users')
def get_users():

    # get all users from the mango
    users = User.objects

    # render 'list.html' blueprint with users
    return render_template('admin/users.html', users=users)

@admin_bp.route('/add/category', methods=['GET', 'POST'])
def add_category():

    add_category_form = AddCategoryForm()

    if add_category_form.validate_on_submit():
        # read item values from the form
        new_category = add_category_form.category_name.data
        
        categories= [category['name'] for category in Category.objects]

        if new_category not in categories:
            category = Category(name=new_category).save()
            flash("The new category added successfully")
        else:
            flash("Category already exist")

        return redirect(url_for('admin.categories_list'))


    return render_template('admin/add-category.html', form= add_category_form)

@admin_bp.route('/categories')
def categories_list():

    categories = Category.objects
    return render_template('admin/categories.html',categories= categories)


@admin_bp.route('/requested/categories')
def requested_categories_list():
    
    requested_categories = RequestCategory.objects

    return render_template('admin/requested-categories.html', requested_categories= requested_categories)


@admin_bp.route('/approve/category/<category_id>')
def approve_category(category_id):
    
    requested_category = RequestCategory.objects(id=category_id).first()
    category = Category(name=requested_category.name).save()
    
    flash(f"The '{requested_category.name}' category added successfully")
    requested_category.delete()
    
    requested_categories = RequestCategory.objects
    return render_template('admin/requested-categories.html', requested_categories= requested_categories)


@admin_bp.route('/decline/category/<category_id>')
def decline_category(category_id):
    
    requested_category = RequestCategory.objects(id=category_id).first().delete()
    flash(f"The '{requested_category.name}' has been removed")

    requested_categories = RequestCategory.objects

    return render_template('admin/requested-categories.html', requested_categories= requested_categories)



@admin_bp.route('/user/view/<id>')
def view_user(id):

    # get user from mango
    user = User.objects(email=id).first()

    
    # render 'profile.html' blueprint with user
    return render_template('admin/view-user.html', user=user)


@admin_bp.route('/deactivate/user/<user_id>')
def deactivate_user(user_id):

    # get user from mango
    user = User.objects(email=user_id).first()
    user.active = False
    user.save()
    
    users = User.objects
    # render 'profile.html' blueprint with user
    return render_template('admin/users.html',users=users)


@admin_bp.route('/activate/user/<user_id>')
def activate_user(user_id):

    # get user from mango
    user = User.objects(email=user_id).first()
    user.active = True
    user.save()
    
    users = User.objects
    # render 'profile.html' blueprint with user
    return render_template('admin/users.html',users=users)
