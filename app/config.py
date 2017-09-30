import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'IPPA5OHeMXuetungokci7fEajoNBIuY2Epam72rlBsTbsqUwt3'

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','')
DATABASE_CONNECT_OPTIONS = {}

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = "fXxoffZT4SJgvi37bYLdjtikOGEQxpeiUqKqSC2HtH8vbBYer4"