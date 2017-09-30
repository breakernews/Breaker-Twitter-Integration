#!/usr/bin/env python

import os
import sys
import json
import string
import signal
from threading import Timer

import praw
import tweepy

import error
from get_access_token import get_access_token
from ParallelSBTree import ParallelSBTree

from flask import Flask
from flask import render_template
from functools import wraps
from flask import request, Response

app = Flask(__name__)

#seriously?!
# import oauth2
# import oauth2.grant
# import oauth2.error
# import oauth2.store.memory
# import oauth2.tokengenerator
# import oauth2.web

configuration  = "./configure.json"



configure_src = open(configuration)
configure_root = json.load(configure_src)
# reddit creds
REDDIT_CLIENT_ID = configure_root["REDDIT_CLIENT_ID"]
REDDIT_CLIENT_SECRET = configure_root["REDDIT_CLIENT_SECRET"]
REDDIT_PASSWORD = configure_root["REDDIT_PASSWORD"]
REDDIT_USER_AGENT = configure_root["REDDIT_USER_AGENT"]
REDDIT_USERNAME = configure_root["REDDIT_USERNAME"]
subreddit_str = configure_root["SUBREDDIT"]
subreddit_name = 'newstweetfeed'
post = "[post name] post content"
post_url = "https://www.google.com"

#below is the normal http client approach
#headers = {'user-agent': 'User-Agent: python:tweetnews:v0.1 (by /u/untoha)'}

#client_auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)

#post_data = {"grant_type": "password", 
#             "username": REDDIT_USERNAME, "password": REDDIT_PASSWORD}

#response = requests.post("https://ssl.reddit.com/api/v1/access_token", 
#                         auth=client_auth, data=post_data)
#time.sleep(10)
# client = requests.session()
# client.headers = headers

# r = client.get(r'http://www.reddit.com/user/'+REDDIT_USERNAME+'/about/.json')
# r.text
# data = r.json()
# print "request result: ", data


#print "submitting something now!"

# post_data = {"sr": subreddit_name, "title": "test submission title", "text": "Some raw text to be submitted from the tweetnewsbot"}
# r = requests.post(u'http://www.reddit.com/api/submit', auth=client_auth, data=post_data)
# r.text
# #data = r.json()
# ipdb.set_trace()
# print "submission result: ", r

# let's try praw way again

#
# authorize reddit OAUTH initialize praw
#
# def setup_reddit_api(client_id, client_secret, password, user_agent, username):
#     #ipdb.set_trace()
#     reddit_api = None
#     try:
#         reddit_api = praw.Reddit(client_id=client_id, client_secret=client_secret,
#                          password=password, user_agent=user_agent,
#                          username=username)
#         # ipdb.set_trace()
#         reddit_api.set_oauth_app_info (client_id=client_id, client_secret=client_secret, redirect_url="http://127.0.0.1:5000/auth_callback")
#         print "reddit api setup ok:", reddit_api, "\n" 
#         url = reddit_api.get_authorize_url('twitter2reddit', 'identity submit edit', True)
#     except OAuthException:
#         print error.AUTH_ERROR

#     return reddit_api
# Script Application. Requires everything: username, password, app id, app secret
reddit_api = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET,
                     password=REDDIT_PASSWORD, username=REDDIT_USERNAME,
                     user_agent=REDDIT_USER_AGENT)

# print "REDDIT_CLIENT_ID: ", REDDIT_CLIENT_ID# = configure_root["REDDIT_CLIENT_ID"]
# print "REDDIT_CLIENT_SECRET: ", REDDIT_CLIENT_SECRET# = configure_root["REDDIT_CLIENT_SECRET"]
# print "REDDIT_PASSWORD: ", REDDIT_PASSWORD# = configure_root["REDDIT_PASSWORD"]
# print "REDDIT_USER_AGENT: ", REDDIT_USER_AGENT# = configure_root["REDDIT_USER_AGENT"]
# print "REDDIT_USERNAME: ", REDDIT_USERNAME# = configure_root["REDDIT_USERNAME"]
# code = 
# print(reddit_api.auth.authorize(code))
# print(reddit_api.auth.url(['identity submit edit'], '...', 'permanent'))
print "reddit api object: ", reddit_api
subreddit = reddit_api.subreddit(subreddit_name)
print "subreddit object: ", subreddit
print reddit_api.user.me()
result = reddit_api.subreddit(subreddit_name).submit("Text to post", "https://www.google.com")
print "submission result: ", result