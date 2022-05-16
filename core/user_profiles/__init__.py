from flask import Blueprint

user_profiles = Blueprint('user_profiles', __name__)

from . import views
