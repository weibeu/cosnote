from . import api
from . import resource

from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


def get_app(configs=None):
    app = Flask(__name__)
    app.config.from_object(configs)

    _cors = CORS(app)
    bcrypt.init_app(app)
    resource.initialize_mongo_connection(configs)

    app.register_blueprint(api.blueprint)

    return app
