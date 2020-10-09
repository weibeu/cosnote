from .. import SerializerBaseSchema

from marshmallow import fields


class UserSchema(SerializerBaseSchema):

    username = fields.String(required=True)
    preferences = fields.Dict(required=True)
