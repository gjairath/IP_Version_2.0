# -*- coding: utf-8 -*-
"""
Created on Sun May 16 02:39:37 2021

@author: garvi
"""


from ip_app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hi! :-)"
