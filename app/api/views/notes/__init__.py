from app.utils import format_bad_request
from app.resource import models
from flask import g

from .. import BaseView
from .serializers import NoteSerializer


class SaveNote(BaseView):

    ROUTE = "/notes/"

    REQUEST_SERIALIZER = NoteSerializer
    RESPONSE_SERIALIZER = NoteSerializer

    @staticmethod
    def post(_instance, data):
        note = models.Note(**data)
        try:
            note.metadata = data["metadata"]
        except KeyError:
            pass
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


class Note(BaseView):

    ROUTE = "/note/<string:note_id>/"
    RESPONSE_SERIALIZER = NoteSerializer

    @staticmethod
    def get(note_id):
        try:
            return [n for n in g.user.notes if n.id.is_valid(note_id)][0]
        except IndexError:
            return format_bad_request(
                message="No notes found for this user with specified ID.", status=404
            )
