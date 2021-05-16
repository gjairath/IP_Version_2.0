# -*- coding: utf-8 -*-
"""
Created on Sun May 16 02:33:24 2021

@author: garvi
"""

# File imports
from ip_app.config import Config


# Packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)


from ip_app import routes
