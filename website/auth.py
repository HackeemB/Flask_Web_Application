from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


#Has a bunch of URLs defined in it
auth = Blueprint('auth', __name__)

#Inside my login.html template, I can access my variable text. This is how we pass a value
#This is how we would use the values in the login.html file {{text}} {{user + "s"}}
#{%if boolean==True%} Yes, it is true! {%else %} No it is not true! {%endif%}
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #This is what you do when you look for a specific entry in your DB.
        #This means we filter all users who has the following email
        #This returns the first result, if there is any result.
        user = User.query.filter_by(email=email).first()
        if user: #if we found a user, we check the password
            #hash the given password then compare to the password in the DB, then log in successfully
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exist!', category='error')
                 

    #This gets the information that was sent to this form, which has all of the data that was sent as a part of the form
    #data = request.form 
    #print(data)
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #This decorator makes sure that we cannot access this page (or root) unless the user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',  methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST': 
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        
        user = User.query.filter_by(email=email).first()
        #The line above queries the user and makes sure that we are not signing up another person with the same email
        if user:
            flash('Email already exists!', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2: 
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #add user to database
            new_user = User(email=email, first_name=first_name, 
            password=generate_password_hash(password1, method='sha256'))

            db.session.add(new_user)
            db.session.commit() 
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
            


    return render_template("sign_up.html", user=current_user)