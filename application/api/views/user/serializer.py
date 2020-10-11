from .. import SerializerBaseSchema

import json

from marshmallow import fields


class UserPreferences(fields.Dict):

    def _serialize(self, value, *args, **kwargs):
        return super()._serialize(json.loads(value.to_json()), *args, **kwargs)


class UserSchema(SerializerBaseSchema):

    username = fields.String(required=True)
    preferences = UserPreferences(required=True)
