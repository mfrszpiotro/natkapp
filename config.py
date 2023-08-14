import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'test')
    TMDB_API_CREDENTIALS = 'Bearer ' + os.environ.get('TMDB_API', '')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///natkapp.db'
    BOOTSTRAP_BOOTSWATCH_THEME = 'lux'