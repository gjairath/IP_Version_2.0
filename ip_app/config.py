# -*- coding: utf-8 -*-
"""
Created on Sun May 16 03:02:33 2021

@author: garvi
"""

# Packages
import logging
from logging.handlers import SMTPHandler
import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "hardcode-these-n"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = uri
    import sys
    
    print (uri, file=sys.stdout)