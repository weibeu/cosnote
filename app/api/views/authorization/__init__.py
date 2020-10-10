from app.utils import format_bad_request
from app.resource import models

import mongoengine

from .. import BaseView, save_session
from .serializers import RegisterSchema
from ..user.serializer import UserSchema


class Register(BaseView):

    ROUTE = "/register/"

    REQUEST_SERIALIZER = RegisterSchema
    RESPONSE_SERIALIZER = UserSchema

    @staticmethod
    def post(instance, data):
        if instance:
            return format_bad_request(message="Specified username is already registered.")
        user = models.User(**data)
        try:
            user.save()
        except mongoengine.ValidationError as exc:
            return format_bad_request(exc=exc)
        save_session(user.username)
        return user


class Authorize(BaseView):

    ROUTE = "/authorize/"
