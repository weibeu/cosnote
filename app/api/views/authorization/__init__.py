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

    REQUEST_SERIALIZER = RegisterSchema
    RESPONSE_SERIALIZER = UserSchema

    @staticmethod
    def post(instance, data):
        if not instance:
            return format_bad_request(message="No account exists with specified username.", status=404)
        if not instance.authorize(data["password"]):
            return format_bad_request(message="The password you entered isn't correct. Please try again.")
        save_session(instance.username)
        return instance
