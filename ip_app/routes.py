# -*- coding: utf-8 -*-
"""
Created on Sun May 16 02:39:37 2021

@author: garvi
"""

# Files
from ip_app import app
from ip_app.forms import Login, Register
from ip_app.models import db, User

# Packages
from flask import request, render_template, make_response, redirect, flash, url_for
from datetime import datetime as dt
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse



@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home', user=current_user)

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
        db.commit()
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

@app.route('/dummy', methods = ["GET"])
@login_required
def show_users():
    user_list = User.query.all()

    return render_template("user_test.html", title = "Show", users = user_list)
