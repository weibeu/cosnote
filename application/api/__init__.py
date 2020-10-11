from flask import Blueprint

from . import views


version = "1.0.0"


blueprint = Blueprint("API", __name__, url_prefix="/api")


for view_cls in views.__all__:
    blueprint.add_url_rule(view_cls.ROUTE, view_func=view_cls.as_view())
