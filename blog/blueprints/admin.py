from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from ..forms import AddCategoryForm
from blog.models import User, Item, Category, RequestCategory, Admin, UpgradeToReseller, Buyer
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

    item = Item.objects(id=item_id).first()
    notification = "Your item number '"+ item_id + "' has been deleted"
    print(item.author)
    user = User.objects(email= item.author).first()
    user.notifications.append(notification)
    user.save()

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
    
    notification = "Your request to add category '"+ requested_category.name + "' has been approved"
    
    user = User.objects(email= requested_category.user).first()
    user.notifications.append(notification)
    user.save()


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


@admin_bp.route('/enable/maintenance/mode')
def enable_maintenance_mode():

    admins = Admin.objects

    for admin in admins:
        admin.under_maintenance = True
        admin.save()

    return redirect(url_for('login.logout'))

@admin_bp.route('/disable/maintenance/mode')
def disable_maintenance_mode():

    admins = Admin.objects

    for admin in admins:
        admin.under_maintenance = False
        admin.save()

    return redirect(url_for('login.login'))

@admin_bp.route('/report')
def report():
    users = User.objects
    items = Item.objects

    admin_number=0
    reseller_number=0
    buyer_number=0
    total_users=0
    items_number=0

    for item in items:
        items_number += 1

    for user in users:
        if user.role == 'Admin':
            admin_number += 1
            total_users += 1
        elif user.role == 'Reseller':
            reseller_number += 1 
            total_users += 1
        elif user.role == 'Buyer':
            buyer_number += 1 
            total_users += 1

    return render_template('admin/report.html', items_number=items_number ,total_users=total_users , admin_number=admin_number, reseller_number=reseller_number, buyer_number=buyer_number)

@admin_bp.route('/upgrade/reseller')
def upgraded_to_reseller_list():
    
    requested_upgrades = UpgradeToReseller.objects

    return render_template('admin/requested-upgrades.html', requested_upgrades= requested_upgrades)

@admin_bp.route('/approve/reseller/upgrade/<request_id>')
def approve_upgrade_request(request_id):
    
    requested_upgrade = UpgradeToReseller.objects(id=request_id).first()
    buyer = Buyer.objects(email=requested_upgrade.buyer_id).first()
    buyer.update(upgraded_to_reseller=True)
    buyer.notifications.append("Your request to upgrade your account to reseller level has been approved")
    buyer.save()
    
    session['upgraded'] = buyer.upgraded_to_reseller

    flash(f"'{buyer.first_name.title()} {buyer.last_name.title()}' upgraded successfully to reseller level")
    requested_upgrade.delete()
    
    requested_upgrades = UpgradeToReseller.objects
    return render_template('admin/requested-upgrades.html', requested_upgrades= requested_upgrades)


@admin_bp.route('/decline/reseller/upgrade/<request_id>')
def decline_upgrade_request(request_id):
    
    requested_upgrade = UpgradeToReseller.objects(id=request_id).first()
    buyer = Buyer.objects(email=requested_upgrade.buyer_id).first()
    buyer.notifications.append("Your request to upgrade your account to reseller level has been declined")
    buyer.save()

    requested_upgrade.delete()

    flash(f"'{buyer.first_name.title()} {buyer.last_name.title()}' request to upgrade his/her account to reseller level declined")

    requested_upgrades = UpgradeToReseller.objects

    return render_template('admin/requested-upgrades.html', requested_upgrades= requested_upgrades)
