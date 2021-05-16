# -*- coding: utf-8 -*-
"""
Created on Sun May 16 04:23:47 2021

@author: garvi
"""

from ip_app import db

class User(db.Model):
    
    id = db.Column(db.Integer, 
                    primary_key=True)
    username = db.Column(db.String(64), 
                         index=True, 
                         unique=True)
    email = db.Column(db.String(120), 
                      index=True, 
                      unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
