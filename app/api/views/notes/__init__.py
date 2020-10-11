from app.utils import format_bad_request
from app.resource import models
from flask import g, current_app

from .. import BaseView
from .serializers import NoteSerializer


def get_note(note_id):
    try:
        return [n for n in g.user.notes if n.id.is_valid(note_id)][0]
    except IndexError:
        return


class SaveNote(BaseView):

    ROUTE = "/notes/"

    REQUEST_SERIALIZER = NoteSerializer
    RESPONSE_SERIALIZER = NoteSerializer

    @staticmethod
    def post(_instance, data):
        note = get_note(data.get("id"))
        if not note:
            if len(g.user.notes) >= current_app.config["USER_NOTES_MAX_LIMIT"]:
                return format_bad_request(message="This user can't create anymore notes.", status=403)
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
        note = get_note(note_id)
        if not note:
            return format_bad_request(
                message="No notes found for this user with specified ID.", status=404
            )
        return note
