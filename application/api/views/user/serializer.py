from .. import SerializerBaseSchema
from ..notes.serializers import NoteSerializer

import json

from marshmallow import fields


class UserPreferences(fields.Dict):

    def _serialize(self, value, *args, **kwargs):
        return super()._serialize(json.loads(value.to_json()), *args, **kwargs)


class PartialUserSchema(SerializerBaseSchema):

    username = fields.String(required=True)
    preferences = UserPreferences(required=True)


class UserSchema(PartialUserSchema):

    notes = fields.List(fields.Nested(NoteSerializer))
