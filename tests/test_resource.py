from app.resource import initialize_mongo_connection
from app.resource import models
from app import configs

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
        assert note.save()
        user.notes.append(note)
        assert user.save()

    def test_get_user(self):
        user = self._get_user("thecosmos1")
        self.test_new_note()
        user.reload()
        self.assertTrue(user.notes)

    def test_get_note(self):
        note = models.Note.objects(id="5f833b38e6a07361e4092c90").first()
        self.assertIsNotNone(note)
