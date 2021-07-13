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
    # author is the field that connects the 1 to many relationship with users and projects.
    author = db.relationship('User', back_populates="user_projects")

    
    project_sub_tasks = db.relationship("Task", back_populates="project_created_by")    

    def __repr__(self):
        return '<Project {}>'.format(self.project_name)


class Task(db.Model):
    id = db.Column(db.Integer, 
                    primary_key=True)
    task_name = db.Column(db.String(64), 
                         index=True)
    assigned_to = db.Column(db.String(120))
    eta = db.Column(db.String(120))
    progress_bar = db.Column(db.String(120))

    
    # The project that owns this task. Back-link.
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    
    # The 1:many relationship for Project:tasks
    project_created_by = db.relationship('Project', back_populates="project_sub_tasks")
        
    def get_data(self):
        '''
        Take this class, parse the data and return an array, needed to push the pipeline down to JS.
        Will be annoying but I assume it's easier to change this array in one place,
        rather than in a 100 places with the json.toJSon()
        '''
        return {
                "task_name": self.task_name,
                "assigned_to": self.assigned_to,
                "eta": self.eta}

    def __repr__(self):
        return '<Task {}>'.format(self.task_name)



# For the flask-login user-session.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))



def delete_all():
    Project.query.delete()        
    db.session.commit()