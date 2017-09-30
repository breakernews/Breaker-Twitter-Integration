import os
_basedir = os.path.abspath(os.path.dirname(__file__))

class test_config(object):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
