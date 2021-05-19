# -*- coding: utf-8 -*-
"""
Created on Sun May 16 02:39:37 2021

@author: garvi
"""

# Files
from ip_app import app
from ip_app.forms import Login, Register
from ip_app.models import db, User
from ip_app.forms import ResetPasswordRequestForm
#from ip_app.forgot_email import send_password_reset_email

# Packages
from flask import request, render_template, make_response, redirect, flash, url_for
from datetime import datetime as dt
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('test69.html', user=current_user)

@app.route("/user/<username>")
@login_required
def profile(username):
    '''
    Profile, at the dashboard as a "dropdown", login required.
    '''
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_profile.html', user=user)

@app.route('/dummy', methods = ["GET"])
@login_required
def show_users():
    '''
    Show all users, at the dashboard, login required.
    '''
    user_list = User.query.all()
    # When this html file extends my base page, the base page has a var for user that isn't importer
    return render_template("user_test.html", users = user_list, user = current_user)

@app.route('/dashboard')
def show_dashboard():
    '''
    Dashboard, at the dasboard, login required.
    '''
    return render_template("dashboard.html", user=current_user)

@app.before_request
def before_request():
    '''
    Tracks the last time user logged on.
    before_request is a flask thing that triggers before views. Convinent. [is that how you spell it?]
    '''
    if (current_user.is_authenticated):
        current_user.profile_last_login = datetime.utcnow()
        db.session.commit()
        
        
'''
    Login functionality is below, Register, Login, Logout.
'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    registeration_form = Register()
    if (registeration_form.validate_on_submit()):
        # Grab already validated data from the form
        user_username = registeration_form.username.data        
        existing_user = User.query.filter(User.username == user_username).first()
        
        if (existing_user is not None):
            # User already exists.
            flash("Pick another username")
            return redirect(url_for("register"))
        
        user_email = registeration_form.email.data
        
        # Make a user object to add to the DB.
        new_user = User(username = user_username, email = user_email)
        new_user.set_password(registeration_form.password.data)
        
        # Add the user
        db.session.add(new_user)
        flash("Thanks for registering {}".format(new_user.username))
        # Commit the changes.
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form = registeration_form)

@app.route('/login', methods = ["GET", "POST"])
def login():
    login_form = Login()
    if (login_form.validate_on_submit()):        
        # Grab already validated data from the form
        user_username = login_form.username.data        
        existing_user = User.query.filter(User.username == user_username).first()
        
        if (existing_user is not None): 
            user_hash = existing_user.check_password(login_form.password.data)

        if (existing_user is not None and user_hash is True):
            # User has entered decent data for once.
            login_user(existing_user, remember = login_form.remember_me.data)  
            
            # IF the user was blocked by the login.login_view = 'login' redirect to this page.
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            # Wrong data. Either user is not found or hash didn't check out.
            flash("Incorrect Username or Password")
            return redirect("/login")
            
    return render_template('login.html', title='Sign In', form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
