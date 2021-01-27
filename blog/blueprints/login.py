from flask import Blueprint, render_template, request, redirect, session, url_for
from ..forms import LoginForm
from blog.models import User

# define our blueprint
login_bp = Blueprint('login', __name__)

@login_bp.route('/')
@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    # create instance of our form
    login_form = LoginForm()

    # handle form submission
    if login_form.validate_on_submit():

        # read post values from the form
        email = login_form.email.data
        password = login_form.password.data

        # get the DB connection
        user = User.objects(email=email).first()

        # check if the user was found and the password matches
        if (user) and (user.password == password) and user.active==True:
            session['uid'] = user.id
            session['email'] = user.email
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['role'] = user.role

            # redirect the user after login
            if user.role == 'Reseller':
                return redirect(url_for('reseller.reseller_index'))

            elif user.role == 'Buyer':
                return redirect('#')

            elif user.role == 'Admin':
                return redirect(url_for('admin.admin_index'))

        else:
            # redirect to 404 if the login was invalid
            return redirect("#")

    # redner the login template
    return render_template("login/login.html", form=login_form)


@login_bp.route('/session')
def show_session():
    return dict(session)


@login_bp.route('/logout')
def logout():
    # pop 'uid' from session
    session.clear()

    # redirect to index
    return redirect("/login")
