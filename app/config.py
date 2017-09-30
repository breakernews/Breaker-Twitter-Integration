import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','')
SQLALCHEMY_TRACK_MODIFICATIONS = False