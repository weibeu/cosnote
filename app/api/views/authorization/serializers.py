from marshmallow import fields

from .. import SerializerBaseSchema


class RegisterSchema(SerializerBaseSchema):

    username = fields.String(required=True)
    email = fields.Email()
    password = fields.String(required=True)
