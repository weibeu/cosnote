from application.resource import models
from marshmallow import fields

from .. import SerializerBaseSchema


class RegisterSchema(SerializerBaseSchema):

    SERIALIZE_TO_OBJECT = models.User

    username = fields.String(required=True)
    email = fields.Email()
    password = fields.String(required=True)
