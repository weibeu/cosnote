from flask import g

from .. import BaseView
from .serializer import UserSchema


class User(BaseView):

    ROUTE = "/user/"

    RESPONSE_SERIALIZER = UserSchema

    @staticmethod
    def get():
        return g.user
