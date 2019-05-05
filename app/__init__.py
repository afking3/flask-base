import os

from flask import Flask


basedir = os.path.abspath(os.path.dirname(__file__))



def create_app(config_name):
    app = Flask(__name__)
    

    return app
