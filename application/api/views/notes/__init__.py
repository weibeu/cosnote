from application.utils import format_bad_request
from application.resource import models
from flask import g, current_app

from .. import BaseView
from .serializers import NoteSerializer


def get_note(note_id):
    return models.Note.objects(id=note_id, user=g.user)


class SaveNote(BaseView):

    ROUTE = "/notes/"

    REQUEST_SERIALIZER = NoteSerializer
    RESPONSE_SERIALIZER = NoteSerializer

    @staticmethod
    def post(instance, data):
        if not instance and len(g.user.notes) >= current_app.config["USER_NOTES_MAX_LIMIT"]:
            return format_bad_request(message="This user can't create anymore notes.", status=403)
        if instance and instance.user != g.user:
            return format_bad_request(message="No notes found for this user with specified ID.", status=404)
        note = models.Note(**data)
        try:
            note.metadata = data["metadata"]
        except KeyError:
            pass
        note.user = g.user
        note.save()
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


class SharedNote(BaseView):

    ROUTE = "/notes/shared/<string:note_id>/"
    RESPONSE_SERIALIZER = NoteSerializer

    REQUIRES_AUTHORIZATION = False

    @staticmethod
    def get(note_id):
        note = models.Note.objects(id=note_id, metadata__shared=True).first()
        if not note:
            return format_bad_request(
                message="No shared notes found for with specified object ID.", status=404
            )
        return note
