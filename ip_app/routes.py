# -*- coding: utf-8 -*-
"""
Created on Sun May 16 02:39:37 2021

@author: garvi
"""


from ip_app import app
from ip_app.forms import Login

from flask import request, render_template, make_response, redirect, flash, url_for
from datetime import datetime as dt
from ip_app.models import db, User



@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Some_Dude_69'}
    
    return render_template('index.html', title='Home', user=user)


@app.route('/login', methods = ["GET", "POST"])
def login():
    login_form = Login()
    if (login_form.validate_on_submit()):
        flash("Done for {} {}".format(login_form.username.data, login_form.password.data))
        return redirect("/index")
    return render_template('login.html', title='Sign In', form=login_form)


@app.route('/dummy', methods = ["GET"])
def create_user():
    user = request.args.get("user")
    email = request.args.get("email")
    
    return render_template("user_test.html", title = "Show", users = User.query.all())
