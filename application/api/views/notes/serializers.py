from application.resource.models.notes import Note, NoteMetadata, SUPPORTED_LANGUAGES
from marshmallow import fields, validate

import datetime

from .. import SerializerBaseSchema


class NoteMetadataSerializer(SerializerBaseSchema):

    SERIALIZE_TO_OBJECT = NoteMetadata

    language = fields.String(default="text", validate=validate.OneOf(
        SUPPORTED_LANGUAGES, error="Specified language is not supported yet."
    ))
    shared = fields.Boolean(default=False)
    last_updated = fields.DateTime(default=datetime.datetime.utcnow)


class NoteSerializer(SerializerBaseSchema):

    SERIALIZE_TO_OBJECT = Note

    id = fields.String()
    title = fields.String(default=str())
    content = fields.String(required=True)
    metadata = fields.Nested(NoteMetadataSerializer)
