# -*- coding: utf-8 -*-
"""
Created on Sun May 16 02:33:24 2021

@author: garvi
"""

# File imports
from ip_app.config import Config
import os
import sys

# Packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap

app = Flask(__name__)

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri

print ("\n\n\n\n{}".format(uri), file=sys.stdout)

login = LoginManager(app)
# Set login view to make a wall user shall not pass.
login.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

mail = Mail(app)
bootstrap = Bootstrap(app)

from ip_app import routes
