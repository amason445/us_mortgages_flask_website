"""
This file contains a flask blue print. It allows the app to render the views.py file and the errors.py file.
"""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors