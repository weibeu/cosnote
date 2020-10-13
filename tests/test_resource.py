from application.resource import initialize_mongo_connection
from application.resource import models
from application import configs

import unittest


configs.MONGODB_DATABASE = "test_{}".format(
    configs.MONGODB_DATABASE
)
initialize_mongo_connection(configs)


class TestNewDocuments(unittest.TestCase):

    @staticmethod
    def _get_user(username):
        return models.User.objects(username=username).first(
        ) or models.User(username=username, password="BruhMoment.7@F")

    def test_new_user(self):
        user = self._get_user("thecosmos1")
        assert user.save()

    def test_new_note(self):
        user = self._get_user("thecosmos1")
        note = models.Note(title="My first note.", content="Lorem ipsum doer solely.")
        note.user = user
        assert note.save()

    def test_get_user(self):
        user = self._get_user("thecosmos1")
        self.test_new_note()
        user.reload()
        self.assertTrue(user.notes)

    def test_get_note(self):
        note = models.Note.objects(id="5f85be20e552d22101ce397c").first()
        self.assertTrue(note.user)
        self.assertIsNotNone(note)

    def test_get_notes(self):
        user = self._get_user("thecosmos1")
        self.assertTrue(user.notes)
        self.assertIsInstance(user.notes, list)

    def test_get_shared_note(self):
        note = models.Note.objects(
            id="5f85be20e552d22101ce397c", metadata__shared=True,
        ).first()
        self.assertIsNotNone(note)
