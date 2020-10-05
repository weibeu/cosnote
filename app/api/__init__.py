from flask import Blueprint
from flask_restx import Api


version = "1.0.0"


__namespaces__ = [

]


blueprint = Blueprint("API", __name__, url_prefix="/api")
api = Api(blueprint, title="Instant Notes API", version=version)

for ns in __namespaces__:
    api.add_namespace(ns, path=ns.ROUTE)
