#!/usr/bin/env python

from flask import Flask
from functools import wraps
from app import app, db, defaults

class Tweet(db.Model):

	__tablename__ = 'tweetposted'
	id = db.Column(db.Integer, primary_key=True)
	tweet_id = db.Column(db.String(100), unique=True)

	def __init__(self, tweet_id=None):
		self.tweet_id = tweet_id

	def __repr__(self):
		return self.tweet_id