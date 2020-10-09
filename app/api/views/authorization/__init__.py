from flask import jsonify, session
from app.resource import models
from app.utils import format_bad_request

import mongoengine

from .. import BaseView
from .serializers import RegisterSchema
from ..user.serializer import UserSchema


class Register(BaseView):

    ROUTE = "/register/"

    REQUEST_SERIALIZER = RegisterSchema
    RESPONSE_SERIALIZER = UserSchema

    @staticmethod
    def post(*, instance):
        user = models.User.objects(username=instance["username"]).first()
        if user:
            return format_bad_request(message="Specified username is already registered.")
        user = models.User(**instance)
        try:
            user.save()
        except mongoengine.ValidationError as exc:
            return format_bad_request(exc=exc)
        session["username"] = user.username
        return user


class Authorize(BaseView):

    ROUTE = "/authorize/"
