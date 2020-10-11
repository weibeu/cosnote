from app.resource.models import Note
from flask import g

from .. import BaseView
from .serializers import NoteSerializer


class SaveNote(BaseView):

    ROUTE = "/notes/save/"

    REQUEST_SERIALIZER = NoteSerializer
    RESPONSE_SERIALIZER = NoteSerializer

    @staticmethod
    def post(_instance, data):
        note = Note(**data)
        note.save()
        g.user.notes.append(note)
        g.user.save()
        return note
