from flask import Blueprint
from flask_cors import CORS

auth = Blueprint('auth', __name__)
CORS(auth)

from . import views
from . import decorators
from . import models
from . import utils
