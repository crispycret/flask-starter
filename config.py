import os
from dotenv import load_dotenv

load_dotenv()


basedir = os.path.abspath(os.path.dirname(__file__))

class Configuration (object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    

