from flask import Blueprint, render_template, request, redirect, session, flash, url_for

from ..forms import EditUserForm, AddUserForm, ChangePasswordForm
from blog.models import User, Item, Reseller, Buyer,Admin


# define our blueprint
user_bp = Blueprint('user', __name__)


@user_bp.route('/add/user', methods=['GET', 'POST'])
def add_user():

    # create instance of our form
    add_user_form = AddUserForm()
    # get the DB connection
    reseller = Reseller()
    buyer = Buyer()
    admin = Admin()

    # handle form submission
    if request.method == 'POST':

        if add_user_form.role.data == 'Buyer':
            # read buyer values from the form
            buyer.email = add_user_form.email.data
            buyer.password = add_user_form.password.data
            buyer.first_name = add_user_form.first_name.data
            buyer.last_name = add_user_form.last_name.data
            buyer.birthdate = add_user_form.birthdate.data
            buyer.role = add_user_form.role.data
            
            buyer.save()

        elif add_user_form.role.data == 'Admin':
            # read admin values from the form
            admin.email = add_user_form.email.data
            admin.password = add_user_form.password.data
            admin.first_name = add_user_form.first_name.data
            admin.last_name = add_user_form.last_name.data
            admin.birthdate = add_user_form.birthdate.data
            admin.role = add_user_form.role.data
            admin.save()
        
        elif add_user_form.role.data == 'Reseller':
            # read reseller values from the form
            reseller.email = add_user_form.email.data
            reseller.password = add_user_form.password.data
            reseller.first_name = add_user_form.first_name.data
            reseller.last_name = add_user_form.last_name.data
            reseller.birthdate = add_user_form.birthdate.data
            reseller.role = add_user_form.role.data
            reseller.save()

        # flash sin up masseag to user
        flash("Account successfully created! Please log in.")

        return redirect('/login')

    # render the template
    return render_template("user/add-user.html", form=add_user_form)



@user_bp.route('/view/user/<user_id>')
def view_user(user_id):

    # get user from mango
    user = User.objects(email=user_id).first()

    
    # render 'profile.html' blueprint with user
    return render_template('user/view-user.html', user=user)


@user_bp.route('/edit/user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):

    user = User.objects(email= user_id).first()


    # create instance of our form
    edit_user_form = EditUserForm()
    if request.method == "GET":
        edit_user_form.first_name.data = user.first_name
        edit_user_form.last_name.data = user.last_name
        edit_user_form.birthdate.data = user.birthdate

    # handle form submission

    if edit_user_form.validate_on_submit():

        # read post values from the form
        first_name = edit_user_form.first_name.data
        last_name = edit_user_form.last_name.data
        birthdate = edit_user_form.birthdate.data

        # save data
        user = User.objects(email=user_id).update(first_name=first_name, last_name=last_name, birthdate =birthdate)

        user = User.objects(email= user_id).first()
        # update session
        session['first_name'] = user.first_name
        session['last_name'] = user.last_name
        session['birthdate'] = user.birthdate

        #  flash masseag
        flash("User information updated successfully!")

            # redirect
        return redirect(url_for('user.view_user', user_id=session['uid']))

    # redner the login template
    return render_template("user/edit-user.html", form=edit_user_form)



@user_bp.route('/change/password/<user_id>', methods=['GET','POST'])
def change_password(user_id):

    change_password_form = ChangePasswordForm()

    if change_password_form.validate_on_submit():

        old_password= change_password_form.old_password.data
        new_password= change_password_form.new_password.data
        confirm_password= change_password_form.confirm_password.data

        user = User.objects(email=user_id).first()

        if old_password == user.password:
            # user.update(password=new_password)
            user = User.objects(email=user_id).update(password=new_password)
            
            flash('Your Password Updated successfully')
            return redirect(url_for('login.login'))

        else:
            flash('faild to change password')
            return redirect(url_for('buyer.view_buyer'))

    return render_template("user/change-password.html", form=change_password_form)