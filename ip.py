# -*- coding: utf-8 -*-
"""
Created on Sun May 16 02:40:36 2021

@author: garvi
"""


from ip_app import app
from ip_app import app, db, error
from ip_app.models import User



@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
