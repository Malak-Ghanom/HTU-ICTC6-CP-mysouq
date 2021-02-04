from flask import Blueprint, render_template, request, redirect, session, url_for
from ..forms import LoginForm
from blog.models import User, Admin

# define login blueprint
login_bp = Blueprint('login', __name__)


@login_bp.route('/', methods=['POST','GET'])
@login_bp.route('/login', methods=['POST', 'GET'])
def login():

    # create instance from login form
    login_form = LoginForm()

    # get admin to check if the application in maintenance mode
    admin = Admin.objects.first()
    session['under_maintenance'] = admin.under_maintenance

    # handle form submission
    if login_form.validate_on_submit():

        # read post values from the form
        email = login_form.email.data
        password = login_form.password.data

        # get user from the mongobd
        user = User.objects(email=email).first()

        # check if the user was found
        if (user):
            # and the password matches
            if (user.password == password):
                # check if the user is active
                if user.active == True:
                    session['uid'] = user.id
                    session['email'] = user.email
                    session['first_name'] = user.first_name
                    session['last_name'] = user.last_name
                    session['role'] = user.role

                    # redirect the user after login depending on user role
                    if user.role == 'Reseller':
                        return redirect(url_for('reseller.check_mode'))

                    elif user.role == 'Buyer':
                        return redirect(url_for('buyer.check_mode'))

                    elif user.role == 'Admin':
                        return redirect(url_for('admin.admin_index'))

                # if the user was disabled render inactive account template
                else:
                    return render_template('user/inactive-account.html')

            # if the password doesn't match render incorrect password template
            else:
                return render_template('user/incorrect-password.html')

        # if the user not found render user not found template
        else:
            return render_template('user/user-not-found.html')

    # if method is GET redner the login template
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
