# -*- coding: utf-8 -*-
"""
Created on Sun May 16 02:33:24 2021

@author: garvi
"""


from flask import Flask

app = Flask(__name__)

from ip_app import routes
