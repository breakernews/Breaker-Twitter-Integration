#!/usr/bin/env python
import os
import sys
import json
import string
from flask import Flask, render_template, request, Response
from flask_json import FlaskJSON, JsonError, json_response, as_json
from functools import wraps
from app import app, defaults, db, models
from models import *

#auth stuff
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'password'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# main route for the web app
@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
@requires_auth
def index():
	global defaults
	handles = Handles.query.all()
	return render_template("index.html", handles=handles)




@app.route("/save", methods=['POST'])
@requires_auth
def save_json():
	temp = request.get_json(force=True)
	print temp
	print temp['tweet_handle']
	h = json.load(temp)
	db.session.query(Handles).delete()
	for _h in h:
		db.session.add(Handles(tweet_handle=_h['tweet_handle'], tweet_name=_h['tweet_name'], tweet_max_id=_h['tweet_max_id']))
	db.session.commit()
	return "Saved!"


t = "[{tweet_max_id: 'None', tweet_name: 'business acc', tweet_handle: 'business'}]"