from flask import abort, jsonify, session
from app.resource import models

import functools

from .serializers import RegisterSchema
from .. import BaseView
from ..user.serializer import UserSchema


def requires_authorization(view):
    @functools.wraps(view)
    def decorator(*args, **kwargs):
        if not session.get("username"):
            abort(401)
        return view(*args, **kwargs)
    return decorator


class Register(BaseView):

    ROUTE = "/register/"

    REQUEST_SERIALIZER = RegisterSchema
    RESPONSE_SERIALIZER = UserSchema

    @staticmethod
    def post(payload):
        user = models.User.objects(username=payload["username"]).first()
        if user:
            return jsonify(errors=dict(username=["Specified username is already registered."])), 400
        user.save()
        session["username"] = user.username
        return user


class Authorize(BaseView):

    ROUTE = "/authorize/"
