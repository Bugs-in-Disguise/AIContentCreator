from app.models import User, db
from flask import request, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user
from app.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash

# this just returns a user given an id if one exists, if it doesn't it returns none
# returning none is what we want because that's what flask-login wants if they don't exist
def load_user(user_id):
    return db.session.execute(db.session.query(User).filter_by(id=user_id)).scalar_one_or_none()

def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate(): # makes sure they did everything the form needed filled out
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.session.execute(db.session.query(User).filter_by(username=name, email=email)).scalar_one_or_none() # this'll return none if there's more than one person with the same username, so let's be careful about this

        # log them in baby (if the passwords match)
        if user is not None and check_password_hash(user.password, password): # check if the hashed passwords are the same
            login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next') # go to the page they were already wanting to go to

        #TODO validate url scheme in flask before allowing user login

        return redirect(next or url_for('main.default')) # either go to their page or go to the main page
    else: # otherwise return them to the login page if they didn't validate, and keep the stuff they have in their form, and also sent it to them if it's just a get request
        return render_template('auth/login.html', form=form)

# this one was ai generated, i couldn't be bothered to write it myself it's getting late and im hungry
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        business_type = form.business_type.data
        insta_username = form.insta_username.data
        insta_password = form.insta_password.data

        # Check if username or email already exists
        user = db.session.execute(db.session.query(User).filter_by(username=username)).scalar_one_or_none()
        if user is not None:
            flash("Username already taken. Please choose another one.", "danger")
            return redirect(url_for('register'))

        # Create a new user and store it in the database
        hashed_password = generate_password_hash(password)
        hashed_insta_password = generate_password_hash(insta_password)
        new_user = User(username=username, email=email, password=hashed_password, business_type=business_type, insta_username=insta_username, insta_password=hashed_insta_password)

        db.session.add(new_user)
        db.session.commit()

        # Log the user in after registration
        login_user(new_user)

        flash("Registration successful! You are now logged in.", "success")

        # Redirect to the home page or the page the user wanted
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.default'))

    return render_template('auth/register.html', form=form)

def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('main.default'))