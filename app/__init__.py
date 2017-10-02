#!/usr/bin/env python

import os
import sys
import json
import string
from werkzeug.contrib.fixers import ProxyFix

import error
from get_access_token import get_access_token

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON, JsonError, json_response, as_json 

app = Flask(__name__)
FLjson = FlaskJSON(app)
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 10
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
#                        pool_size=20, max_overflow=0)
db = SQLAlchemy(app)

# web interface
app.wsgi_app = ProxyFix(app.wsgi_app)
from . import views, models, controller