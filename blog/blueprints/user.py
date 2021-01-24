from flask import Blueprint, render_template, request, redirect, session, flash, url_for

from ..forms import EditUserForm, AddUserForm
from blog.models import User, Item, Reseller


# define our blueprint
user_bp = Blueprint('user', __name__)


@user_bp.route('/add/user', methods=['GET', 'POST'])
def add_user():

    # create instance of our form
    add_user_form = AddUserForm()
    # get the DB connection
    user = User()

    # handle form submission
    if add_user_form.validate_on_submit():
        # read post values from the form
        user.email = add_user_form.email.data
        user.password = add_user_form.password.data
        user.first_name = add_user_form.first_name.data
        user.last_name = add_user_form.last_name.data
        user.biography = add_user_form.biography.data
        user.role = add_user_form.role.data

        user.save()

        # flash sin up masseag to user
        flash("Account successfully created! Please log in.")

        return redirect('/login')

    # render the template
    return render_template("user/add-user.html", form=add_user_form)


@user_bp.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):

    # create instance of our form
    edit_user_form = EditUserForm()
    if request.method == "GET":
        edit_user_form.first_name.data = session['first_name']
        edit_user_form.last_name.data = session['last_name']
        edit_user_form.picture_url.data = ''
        edit_user_form.biography.data = session['biography']

    # handle form submission

    if edit_user_form.validate_on_submit():

        user = User()

        # read post values from the form
        user.first_name = edit_user_form.first_name.data
        user.last_name = edit_user_form.last_name.data
        user.picture_url = edit_user_form.picture_url.data
        user.biography = edit_user_form.biography.data

        # save data
        user.save()

        # update session
        session['first_name'] = user.first_name
        session['last_name'] = user.last_name
        session['picture_url'] = user.picture_url
        session['biography'] = user.biography
        
        #  flash masseag
        flash("User information updated successfully!")

            # redirect
        return redirect(url_for('user.view_user', id=session['uid']))

    # redner the login template
    return render_template("user/edit-user.html", form=edit_user_form)
