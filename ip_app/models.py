# -*- coding: utf-8 -*-
"""
Created on Sun May 16 04:23:47 2021

@author: garvi
"""

# File imports
from ip_app import db
from ip_app import login

# Packages
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime

class User(UserMixin, db.Model):
    
    id = db.Column(db.Integer, 
                    primary_key=True)
    username = db.Column(db.String(64), 
                         index=True, 
                         unique=True)
    email = db.Column(db.String(120), 
                      index=True, 
                      unique=True)
    password_hash = db.Column(db.String(128))
    profile_last_login = db.Column(db.DateTime, default=datetime.utcnow)


    def avatar(self, size):
        email_req = self.email.lower().encode('utf-8')
        digest = md5(email_req).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    # Generic stuff to make my life easier with logins.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


# For the flask-login user-session.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
