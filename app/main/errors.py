from . import main

@main.errorhandler(404)
def page_not_found(error):
    return "This page does not exist", 404

@main.errorhandler(500)
def internal_server_error(error):
    return "Internal server error", 404