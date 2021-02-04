from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from ..forms import AddCategoryForm
from blog.models import User, Item, Category, RequestCategory, Admin, UpgradeToReseller, Buyer, Reseller


# define "Admin" blueprint
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
def admin_index():

    # get requseted category with length for navbar
    category_requests = RequestCategory.objects
    category_requests_number = len(category_requests)

    # get upgrade requsets with length for navbar
    upgrade_requests = UpgradeToReseller.objects
    upgrade_requests_number = len(upgrade_requests)

    # get items from mangodb
    items = Item.objects

    # render 'admin index' templates with items
    return render_template('admin/index.html', items=items, upgrade_requests_number=upgrade_requests_number, category_requests_number=category_requests_number)


@admin_bp.route('/user/delete/<user_id>')
def delete_user(user_id):

    # delete user from mangodb
    user = User.objects(email=user_id).first().delete()

    # delete items for the user from mangodb
    user_item = Item.objects(author=user_id).delete()

    # back to 'users list' page
    return redirect(url_for('user.get_users'))


@admin_bp.route('/admin/delete/item/<item_id>')
def admin_delete_item(item_id):

    # get item from mongodb
    item = Item.objects(id=item_id).first()

    # notify reseller that his item has been deleted
    notification = "Your item number '" + item.title + "' has been deleted"
    reseller = Reseller.objects(email=item.author).first()
    reseller.notifications.append(notification)
    reseller.save()

    # delete item from mongodb
    item.delete()

    # redirect to admin home page
    return redirect(url_for('admin.admin_index'))


@admin_bp.route('/users')
def get_users():

    # get all users from the mangodb
    users = User.objects

    # render 'users.html' template
    return render_template('admin/users.html', users=users)


@admin_bp.route('/add/category', methods=['GET', 'POST'])
def add_category():

    # create instance from the add category form
    add_category_form = AddCategoryForm()

    # if method is POST
    if add_category_form.validate_on_submit():

        # read category name values from the form
        new_category = add_category_form.category_name.data

        # get all categories from mongodb
        categories = [category['name'] for category in Category.objects]

        # check if the new category already exist in categories
        if new_category not in categories:
            category = Category(name=new_category).save()
            flash("The new category added successfully")
        else:
            flash("Category already exist")

        # redirect to categories list
        return redirect(url_for('admin.categories_list'))

    # if method is GET return add category template
    return render_template('admin/add-category.html', form=add_category_form)


@admin_bp.route('/categories')
def categories_list():

    # get all categories from mongodb
    categories = Category.objects

    # return render to categories template
    return render_template('admin/categories.html', categories=categories)


@admin_bp.route('/requested/categories')
def requested_categories_list():

    # get requested categories from mongobd
    requested_categories = RequestCategory.objects

    # display requested categories
    return render_template('admin/requested-categories.html', requested_categories=requested_categories)


@admin_bp.route('/approve/category/<category_id>')
def approve_category(category_id):

    # get category by category_id
    requested_category = RequestCategory.objects(id=category_id).first()

    # approve it by adding it to the categories list
    category = Category(name=requested_category.name).save()

    # notify reseller that his category has been approved
    notification = "Your request to add category '" + \
        requested_category.name + "' has been approved"
    reseller = Reseller.objects(email=requested_category.user).first()
    reseller.notifications.append(notification)
    reseller.save()

    # inform admin that the category added successfuly
    flash(f"The '{requested_category.name}' category added successfully")

    # delete request from mongodb
    requested_category.delete()

    # redirect to requested categories list
    return redirect(url_for('admin.requested_categories_list'))


@admin_bp.route('/decline/category/<category_id>')
def decline_category(category_id):

    # get requested category from mongobd
    requested_category = RequestCategory.objects(id=category_id).first()

    # inform admin that the categoriy declined successfuly
    flash(f"The '{requested_category.name}' has been removed")

    # delete category from requested categories list
    requested_category.delete()

    requested_categories = RequestCategory.objects

    # redirect to requested categories list
    return redirect(url_for('admin.requested_categories_list'))


@admin_bp.route('/deactivate/user/<user_id>')
def deactivate_user(user_id):

    # get user(reseller/buyer) from mangodb and change his state
    user = User.objects(email=user_id).first()
    user.active = False
    user.save()

    # get users from mangodb
    users = User.objects

    # render 'users.html' template
    return render_template('admin/users.html', users=users)


@admin_bp.route('/activate/user/<user_id>')
def activate_user(user_id):

    # get user(reseller/buyer) from mangodb and change his state
    user = User.objects(email=user_id).first()
    user.active = True
    user.save()

    # get users from mangodb
    users = User.objects

    # render 'users.html' template
    return render_template('admin/users.html', users=users)


@admin_bp.route('/enable/maintenance/mode')
def enable_maintenance_mode():

    # get admins from mongodb
    admins = Admin.objects

    # change mode to maintenance mode for all admins
    for admin in admins:
        admin.under_maintenance = True
        admin.save()

    # redirect to home page for admin
    return redirect(url_for('login.logout'))


@admin_bp.route('/disable/maintenance/mode')
def disable_maintenance_mode():

    # get admins from mongodb
    admins = Admin.objects

    # change mode to maintenance mode for all admins
    for admin in admins:
        admin.under_maintenance = False
        admin.save()

    # redirect to home page for admin
    return redirect(url_for('admin.admin_index'))


@admin_bp.route('/report')
def report():

    # get all users and items from mongodb
    users = User.objects
    admins = User.objects(role='Admin')
    resellers = User.objects(role='Reseller')
    buyers = User.objects(role='Buyer')
    items = Item.objects

    # get number of users and items
    report_info = [
        {'Admins': len(admins)},
        {'Resellers': len(resellers)},
        {'Buyers': len(buyers)},
        {'Total Users': len(users)},
        {'Items': len(items)}
    ]

    # render report template with length of users and items
    return render_template('admin/report.html', report_info= report_info)


@admin_bp.route('/upgrade/reseller')
def upgraded_to_reseller_list():

    # get all upgrade requests
    requested_upgrades = UpgradeToReseller.objects

    # render requested-upgrades-list
    return render_template('admin/requested-upgrades-list.html', requested_upgrades=requested_upgrades)


@admin_bp.route('/approve/reseller/upgrade/<request_id>')
def approve_upgrade_request(request_id):

    # get request that admin wish to approve
    requested_upgrade = UpgradeToReseller.objects(id=request_id).first()
    
    # get request that admin wish to approve
    # get buyer and upgrade him to reseller
    buyer = Buyer.objects(email=requested_upgrade.buyer_id).first()
    buyer.update(upgraded_to_reseller=True)

    # notify buyer
    buyer.notifications.append("Your request to upgrade your account to reseller level has been approved")
    buyer.save()

    # save state of buyer in session
    session['upgraded'] = buyer.upgraded_to_reseller

    # flash a msg to admin to inform him that the buyer upgraded successfuly
    flash(f"'{buyer.first_name.title()} {buyer.last_name.title()}' upgraded successfully to reseller level")

    # delete request from the list
    requested_upgrade.delete()

    # return back to upgraded to reseller list
    return redirect(url_for('admin.upgraded_to_reseller_list'))

@admin_bp.route('/decline/reseller/upgrade/<request_id>')
def decline_upgrade_request(request_id):

    # get request that admin wish to approve
    requested_upgrade = UpgradeToReseller.objects(id=request_id).first()

    # get buyer and upgrade him to reseller
    buyer = Buyer.objects(email=requested_upgrade.buyer_id).first()

    # notify buyer that his request has been declined
    buyer.notifications.append("Your request to upgrade your account to reseller level has been declined")
    buyer.save()

    # delete request from the list
    requested_upgrade.delete()

    # flash a msg to admin to inform him that the buyer request declined successfuly
    flash(f"'{buyer.first_name.title()} {buyer.last_name.title()}' request to upgrade his/her account to reseller level declined")

    # return back to upgraded to reseller list
    return redirect(url_for('admin.upgraded_to_reseller_list'))
