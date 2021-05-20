# -*- coding: utf-8 -*-
"""
Created on Wed May 19 02:43:10 2021

@author: garvi
    Will try my best to update this as I go this time.
    EDIT: I lied. 

    The love of my life:
            DON'T PANIC, your friendly Werkzeug powered traceback interpreter.

/
    test.py; unit-tests for functionality.
    ip.py; as per flask documentation needed to drive the full thing
ip_app/
    __init__.py;
    app; database file.
    config.py; holds a typical config class
    error.py; 404/500 errors.
    forms.py; the bridge that passes data to the routes.py file, to view the ip_app/templates/
    models.py; hosts the database with flask-sql that can be used to interact with OOP.
    routes.py; 
ip_app/static
    files that use url_for but have no route
ip_app/templates
    html templates for different pages
ip_env/
    virtual env for importing the packages.
migrations/
    database migrations before just porting things.
"""


