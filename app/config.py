"""
This file acts a config file and it contains environment settings. 
This script accesses configuration settings through Windows Environment variables.
For this app to work, you will need to set a windows environment variable for a CouchDB Root URL.
This root URL will path to CouchDB and contain CouchDB log in information. 
Additionally, you will need to set an environment variable to path to flasky.py and to indicate if Debug mode should be on.
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    DEBUG = False
    TESTING = False
    COUCHDB_ROOT_URL = os.environ.get('COUCHDB_ROOT_URL')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    ABC = '123'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}