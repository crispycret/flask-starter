from flask import Blueprint
from flask_cors import CORS

user_profiles = Blueprint('user_profiles', __name__)
CORS(user_profiles)

from . import views
from . import decorators
from . import models