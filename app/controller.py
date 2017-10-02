#!/usr/bin/env python

import os
import sys
import json
import string
import signal
from threading import Timer, Lock

import praw
import tweepy

import error
from get_access_token import get_access_token
# from ParallelSBTree import ParallelSBTree
from bintrees import AVLTree

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON, JsonError, json_response, as_json 

from models import *

# twitter_posts = ParallelSBTree({})
# handles_in_a_tree = ParallelSBTree({})
twitter_posts = {}
handles_in_a_tree = {}

configuration  = "./app/configure.json"

handle_list_key = ""
subreddit_str = ""
reddit_url = "https://reddit.com/"
twitter_url = "https://twitter.com/"

GET_INTERVAL = 20  # 20 seconds to not let heroku's process manager kill our thread
UTF_8 = 'utf-8'
_timer = None
lock = Lock()

#
# write to json file in file_src
#
def update_json(file_src, keys, values):
    with open(file_src, "r+") as json_src:
        json_root = json.load(json_src)
        for i in range(0, len(keys)):
            json_root[keys[i]] = values[i]
        # write update
        json_src.close()
        json_src = open(file_src, "w+")
        json_src.write(json.dumps(json_root))


#
# initialize OAUTH with twitter api
#
def setup_twitter_api(consumer_key, consumer_secret, access_token, access_key, username, password):
    if access_token == "" or access_key == "":
        (access_token, access_key) = get_access_token(consumer_key, consumer_secret, username, password)
        #  update config  file
        update_json(configuration, ["TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_KEY"], [access_token, access_key])

    twitter_api = None
    try:    # authorize twitter, initialize tweepy 
       auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
       auth.set_access_token( access_token, access_key)
       twitter_api = tweepy.API(auth)
    except tweepy.TweepError:
       print error.AUTH_ERROR

    return twitter_api


#
# authorize reddit OAUTH initialize praw
#
def setup_reddit_api(client_id, client_secret, password, user_agent, username):
    reddit_api = None
    reddit_api = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET,
                         password=REDDIT_PASSWORD, username=REDDIT_USERNAME,
                         user_agent=REDDIT_USER_AGENT)
    print "reddit api setup ok:", reddit_api, "\n" 
    print "authorized as: ", reddit_api.user.me()
    return reddit_api

#
# fetch twitter top tweet from account
#
def get_tweet(twitter_api, account):
    global twitter_handles, twitter_posts
    print "accout: ", account
    recent_user_tweet = twitter_api.user_timeline(screen_name = account ,count=1)
    if len(recent_user_tweet) > 0:
        recent_user_tweet = recent_user_tweet[0]
    else:
        return None
    # print recent_user_tweet
    print account
    print "tweet_id:", recent_user_tweet.id,  "max_tweet_id:", str(handles_in_a_tree[account]['tweet_max_id'])
    lock.acquire()
    for item in Handles.query.all():
        if item.tweet_handle == account:
            if recent_user_tweet.id > int(str(account['tweet_max_id']) ):
                #final double check with db now due to thread concurrency, although we did a thread lock...
                if recent_user_tweet.id > long(item.tweet_max_id):
                    tweet_url = twitter_url + account + "/status/"  + str(recent_user_tweet.id)
                    handles_in_a_tree[account] = {'tweet_handle':account, "tweet_name": str(account['tweet_name']), "tweet_max_id":int(recent_user_tweet.id) } # update user in twitter_handles
                    twitter_posts[account] = { 'tweet_handle' : account, "tweet_name" : str(account['tweet_name']), "url":tweet_url, "content" : recent_user_tweet.text.encode(UTF_8) }
                    print "updating handle ", item.tweet_handle
                    print "current max_id value: ", item.tweet_max_id
                    print "new max_id value: ", str(recent_user_tweet.id)
                    item.tweet_max_id = str(recent_user_tweet.id)
                    db.session.commit()
                    # print twitter_handles
                    signal.alarm(10)   # send signal to process tweet 10 seconds later
    lock.release()

#
# post tweet to subreddit
#
def post_thread(reddit_api, tweet):
    global twitter_posts
    print "HIT"
    print "tweet ", tweet
    lock.acquire()
    post = "[{th}] {tp}".format(
                        th = str(tweet['tweet_name']),
                        tp = str(tweet['content']) )

    post_url = tweet['url']
    print "attempt to submit this: ", post, post_url, tweet['tweet_name'], "\n"
    twitter_posts.pop(str(tweet['tweet_handle']))
    reddit_api.subreddit(subreddit_str).submit(post, url=post_url), "\n" 
    lock.release()

#
# calls the handler get_tweet every interval
#
def signal_get_handler(handles_in_a_tree, interval):
    # check twitter every interval
    global _timer
    global twitter_api
    # handles_in_a_tree.foreach(get_tweet, handles_in_a_tree.psbt._root)
    for item in handles_in_a_tree:
    	print "calling get_tweet with this account: ", item
        get_tweet(twitter_api, item)
    if _timer == None:
        _timer = Timer(interval, signal_get_handler, args=[handles_in_a_tree, interval]).start()
    else:
        _time.stop()
        _timer = Timer(interval, signal_get_handler, args=[handles_in_a_tree, interval]).start()

#
# attached to SIGALRM to get called
#
def signal_post_handler(signum, stack):
     # twitter_posts.foreach(post_thread, twitter_posts.psbt._root)
     global reddit_api
     for item in twitter_posts:
        post_thread(reddit_api, item)

def reload():
    global twitter_handles
    global handles_in_a_tree
    global twitter_api
    handle_list = Handles.query.all()
    print handle_list
    twitter_handles = {}
    for i in range(len(handle_list)):
        twitter_handles[handle_list[i].tweet_handle] = {'tweet_handle': str(handle_list[i].tweet_handle), 
        'tweet_name': handle_list[i].tweet_name, 
        'tweet_max_id': long(handle_list[i].tweet_max_id) }
    print twitter_handles
    handles_in_a_tree = twitter_handles
    signal_get_handler(handles_in_a_tree, GET_INTERVAL)
    # attach post to  signal.SIGALARM
    signal.signal(signal.SIGALRM, signal_post_handler)
    return False

# account configuration
configure_src = open(configuration)
# twitter creds
configure_root = json.load(configure_src)
TWITTER_CONSUMER_KEY = configure_root["TWITTER_CONSUMER_KEY"]
TWITTER_CONSUMER_SECRET = configure_root["TWITTER_CONSUMER_SECRET"]
TWITTER_ACCESS_TOKEN = configure_root["TWITTER_ACCESS_TOKEN"]
TWITTER_ACCESS_KEY = configure_root["TWITTER_ACCESS_KEY"]
username = configure_root["TWITTER_USER"]
password = configure_root["TWITTER_PASS"]
# reddit creds
REDDIT_CLIENT_ID = configure_root["REDDIT_CLIENT_ID"]
REDDIT_CLIENT_SECRET = configure_root["REDDIT_CLIENT_SECRET"]
REDDIT_PASSWORD = configure_root["REDDIT_PASSWORD"]
REDDIT_USER_AGENT = configure_root["REDDIT_USER_AGENT"]
REDDIT_USERNAME = configure_root["REDDIT_USERNAME"]
handle_list_key = configure_root["HANDLE_LIST_KEY"]
subreddit_str = configure_root["SUBREDDIT"]

twitter_handles = {}

twitter_api = setup_twitter_api(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_KEY, username, password)
reddit_api = setup_reddit_api(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_PASSWORD, REDDIT_USER_AGENT, REDDIT_USERNAME)

reload()

# twitter_posts.shared = reddit_api
