"""
This script allows for error handling in the flask view functions.
Since this website isn't served to the public, I didn't use this feature often and used the debug server instead.
This module is an example included from Miguel Grinberg's Flask Web Development: Developing Web Applications with Python.
"""

from . import main

@main.errorhandler(404)
def page_not_found(error):
    return "This page does not exist", 404

@main.errorhandler(500)
def internal_server_error(error):
    return "Internal server error", 500