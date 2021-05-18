# -*- coding: utf-8 -*-
"""
Created on Mon May 17 22:39:56 2021

@author: garvi
"""


from flask import render_template
from ip_app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
