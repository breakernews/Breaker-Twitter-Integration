#!/usr/bin/env python

from flask import Flask
from functools import wraps
from app import app, defaults

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
	with open(defaults) as twitter_handles_src:
		return render_template("index.html", json=json.load(twitter_handles_src))


@app.route("/save", methods=['POST'])
@requires_auth
def save_json():
	return "Not finished yet"
