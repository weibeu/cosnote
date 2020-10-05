from . import resource

from flask import Flask
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


def get_app(configs=None):
    app = Flask(__name__)
    app.config.from_object(configs)

    bcrypt.init_app(app)
    resource.initialize_mongo_connection(configs)

    return app
