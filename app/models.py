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

	def __repr__(self):
		return self.tweet_name + " | " + self.tweet_handle
