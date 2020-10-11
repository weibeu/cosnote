from application.utils import format_bad_request
from application.resource.models import User

import functools
import mongoengine
import marshmallow

from flask import views, request, session, Response, g, jsonify


def save_session(username, permanent=True):
    session["username"] = username
    session.permanent = bool(permanent)


def revoke_session():
    session.pop(get_username(), None)


def get_username():
    return session.get("username")


def get_current_user():
    return User.objects(username=get_username()).first()


def requires_authorization(view):
    @functools.wraps(view)
    def decorator(*args, **kwargs):
        user = get_current_user()
        if not user:
            return format_bad_request(message="Unauthorized.", status=401)
        g.user = user
        return view(*args, **kwargs)
    return decorator


class SerializerBaseSchema(marshmallow.Schema):

    SERIALIZE_TO_OBJECT = dict
    SERIALIZE_TO_RESPONSE = None

    errors = marshmallow.fields.Dict()

    @marshmallow.post_load
    def make_instance(self, data, **_kwargs):
        self.context["data"] = data
        instance = None
        if self.SERIALIZE_TO_OBJECT is dict:
            instance = self.SERIALIZE_TO_OBJECT(**data)
        if issubclass(self.SERIALIZE_TO_OBJECT, mongoengine.Document):
            # noinspection PyProtectedMember
            instance = self.SERIALIZE_TO_OBJECT.objects(**{
                pk: data[pk] for pk, f in self.SERIALIZE_TO_OBJECT._fields.items() if f.primary_key
            }).first()
        if issubclass(self.SERIALIZE_TO_OBJECT, mongoengine.EmbeddedDocument):
            instance = self.SERIALIZE_TO_OBJECT(**data)
        return instance

    @marshmallow.post_dump
    def make_response(self, data, **_kwargs):
        if not self.SERIALIZE_TO_RESPONSE:
            return data
        raise NotImplementedError


class __MetaView(views.MethodViewType):

    NAME = ROUTE = str()
    REQUIRES_AUTHORIZATION = True

    def __init__(cls, name, *args, **kwargs):
        if name != "BaseView":
            if not cls.ROUTE:
                raise NotImplementedError("View class should define a valid route as endpoint.")
            if cls.REQUIRES_AUTHORIZATION:
                cls.decorators = (requires_authorization, *cls.decorators)
            cls.NAME = cls.__name__.lower() if not cls.NAME else cls.NAME
        super().__init__(name, *args, **kwargs)


class BaseView(views.MethodView, metaclass=__MetaView):

    REQUEST_SERIALIZER = None
    RESPONSE_SERIALIZER = None
    SERIALIZER_KWARGS = dict()

    @classmethod
    def as_view(cls, *args, **kwargs):
        return super().as_view(cls.NAME, *args, **kwargs)

    def dispatch_request(self, *args, **kwargs):
        try:
            serializer = self.REQUEST_SERIALIZER(**self.SERIALIZER_KWARGS)
            instance = serializer.load(request.get_json() or dict())
        except marshmallow.ValidationError as exc:
            return format_bad_request(exc=exc)
        except TypeError:
            ret = super().dispatch_request(*args, **kwargs)
        else:
            ret = super().dispatch_request(instance, serializer.context["data"], *args, **kwargs)

        if isinstance(ret, Response) or (isinstance(ret, tuple) and isinstance(ret[0], Response)):
            return ret

        try:
            ret = self.RESPONSE_SERIALIZER(**self.SERIALIZER_KWARGS).dump(ret)
        except TypeError:
            pass

        return jsonify(ret)
