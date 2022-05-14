import datetime

import jwt
import uuid
from functools import wraps

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import MetaData

from config import Configuration



app = Flask(__name__)

app.config.from_object(Configuration)

db = SQLAlchemy(app)


naming_convention = {
    'ix': 'ix_$(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))




migrate = Migrate(app, db, render_as_batch=True)





from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)


from core import views



