from application.resource.models.notes import Note, NoteMetadata, SUPPORTED_LANGUAGES
from marshmallow import fields, validate

from .. import SerializerBaseSchema


class NoteMetadataSerializer(SerializerBaseSchema):

    SERIALIZE_TO_OBJECT = NoteMetadata

    language = fields.String(default="text", validate=validate.OneOf(
        SUPPORTED_LANGUAGES, error="Specified language is not supported yet."
    ))
    shared = fields.Boolean(default=False)


class NoteSerializer(SerializerBaseSchema):

    SERIALIZE_TO_OBJECT = Note

    id = fields.String()
    title = fields.String(required=True)
    content = fields.String(required=True)
    metadata = fields.Nested(NoteMetadataSerializer)
