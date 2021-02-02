from flask import Blueprint, render_template, request, redirect, session, url_for
from ..forms import LoginForm
from blog.models import User, Admin

# define our blueprint
login_bp = Blueprint('login', __name__)



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
        print(user.email)
        # check if the user was found and the password matches
        if (user):
            if (user.password == password):
                if user.active == True:
                    session['uid'] = user.id
                    session['email'] = user.email
                    session['first_name'] = user.first_name
                    session['last_name'] = user.last_name
                    session['role'] = user.role
                    print(user.role)
                    # redirect the user after login
                    if user.role == 'Reseller':
                        return redirect(url_for('reseller.check_mode'))

                    elif user.role == 'Buyer':
                        return redirect(url_for('buyer.check_mode'))

                    elif user.role == 'Admin':
                        return redirect(url_for('admin.admin_index'))

                else:
                    return '<h1>this account has been disabled, please contact the support service provider.</h1>'

            else:
                return '<h1>incorrect password</h1>'

        else:
            return '<h1>user not found</h1>'

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
