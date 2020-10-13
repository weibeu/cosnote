from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


def get_app(configs=None):
    from . import api
    from . import resource

    app = Flask(__name__)
    app.config.from_object(configs)

    _cors = CORS(app, supports_credentials=True, origins=["http://localhost:3000", ])
    bcrypt.init_app(app)
    resource.initialize_mongo_connection(configs)

    app.register_blueprint(api.blueprint)

    return app
