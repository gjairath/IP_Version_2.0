# -*- coding: utf-8 -*-
"""
Created on Sun May 16 04:23:47 2021

@author: garvi
"""

# File imports
from ip_app import login, app, db

# Packages
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime
from time import time
import jwt

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
    
    # User related project.
    user_projects = db.relationship('Project', back_populates="author")


    def avatar(self, size):
        email_req = self.email.lower().encode('utf-8')
        digest = md5(email_req).hexdigest()
        return ('https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size))

    # Generic stuff to make my life easier with logins.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, duration = 600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + duration}, app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.username)



class Project(db.Model):
    id = db.Column(db.Integer, 
                    primary_key=True)
    project_name = db.Column(db.String(64), 
                         index=True)
    project_desc = db.Column(db.String(120))
    num_members = db.Column(db.Integer)
    num_tasks = db.Column(db.Integer)
    project_last_changed = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates="user_projects")
    
    # author is the field that connects the 1 to many relationship with users and projects.

    def __repr__(self):
        return '<Project {}>'.format(self.project_name)



# For the flask-login user-session.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
