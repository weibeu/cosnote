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


class UserNotes(BaseView):

    ROUTE = "/notes/"

    RESPONSE_SERIALIZER = NoteSerializer
    SERIALIZER_KWARGS = dict(many=True)

    @staticmethod
    def get():
        return g.user.notes
