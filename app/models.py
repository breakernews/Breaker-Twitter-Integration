#!/usr/bin/env python

from flask import Flask
from functools import wraps
from app import app, db

class Handles(db.Model):
	__tablename__ = 'tweethandles'
	id = db.Column(db.Integer, primary_key=True)
	tweet_handle = db.Column(db.String(100), unique=True)
	tweet_name = db.Column(db.String(100), unique=False)
	tweet_max_id = db.Column(db.String(100), unique=False)

	# def __init__(self, tweet_handle=None, tweet_name=None, tweet_max_id=None):
	# 	self.tweet_handle = tweet_handle
	# 	self.tweet_name = tweet_name
	# 	self.tweet_max_id = tweet_max_id

	def __repr__(self):
		return self.tweet_name + " | " + self.tweet_handle
