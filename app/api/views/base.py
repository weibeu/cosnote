from app.utils import format_bad_request

import functools
import mongoengine
import marshmallow

from flask import views, request, jsonify, session, Response


def requires_authorization(view):
    @functools.wraps(view)
    def decorator(*args, **kwargs):
        if not session.get("username"):
            jsonify(errors=dict(message="Unauthorized"))
        return view(*args, **kwargs)
    return decorator


class SerializerBaseSchema(marshmallow.Schema):

    SERIALIZE_TO_OBJECT = dict
    errors = marshmallow.fields.Dict()

    @marshmallow.post_load
    def make_instance(self, data, **_kwargs):
        instance = None
        if self.SERIALIZE_TO_OBJECT is dict:
            instance = self.SERIALIZE_TO_OBJECT(**data)
        if isinstance(self.SERIALIZE_TO_OBJECT, mongoengine.Document):
            # noinspection PyProtectedMember
            instance = self.SERIALIZE_TO_OBJECT.objects(**{
                pk: data[pk] for pk in self.SERIALIZE_TO_OBJECT._fields
            }).first()
        return instance, data


class __MetaView(views.MethodViewType):

    NAME = ROUTE = str()
    decorators = []
    REQUIRES_AUTHORIZATION = False

    def __init__(cls, name, *args, **kwargs):
        if name != "BaseView":
            if not cls.ROUTE:
                raise NotImplementedError("View class should define a valid route as endpoint.")
            if cls.REQUIRES_AUTHORIZATION:
                cls.decorators.append(requires_authorization)
            cls.NAME = cls.__name__.lower() if not cls.NAME else cls.NAME
        super().__init__(name, *args, **kwargs)


class BaseView(views.MethodView, metaclass=__MetaView):

    REQUEST_SERIALIZER = None
    RESPONSE_SERIALIZER = None

    @classmethod
    def as_view(cls, *args, **kwargs):
        return super().as_view(cls.NAME, *args, **kwargs)

    def dispatch_request(self, *args, **kwargs):
        try:
            instance, data = self.REQUEST_SERIALIZER().load(request.get_json() or dict())
        except marshmallow.ValidationError as exc:
            return format_bad_request(exc=exc)
        except TypeError:
            ret = super().dispatch_request(*args, **kwargs)
        else:
            ret = super().dispatch_request(*args, instance, data, **kwargs)

        if isinstance(ret, Response) or (isinstance(ret, tuple) and isinstance(ret[0], Response)):
            return ret

        try:
            return self.RESPONSE_SERIALIZER().dump(ret)
        except TypeError:
            return ret
