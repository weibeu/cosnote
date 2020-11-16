from ..fields import UsernameField
from ..fields import PasswordField

from . import notes
from . import BaseDocument

from mongoengine import EmbeddedDocument
from mongoengine import EmbeddedDocumentField, BooleanField, EmailField


class UserPreferences(EmbeddedDocument):

    developer = BooleanField(default=True)


class User(BaseDocument):

    username = UsernameField(minimum_length=5, max_length=20, primary_key=True)
    email = EmailField(unique=True, sparse=True)
    password = PasswordField()
    preferences = EmbeddedDocumentField(UserPreferences, default=UserPreferences)

    def authorize(self, password):
        return PasswordField.verify(self.password, password)

    @property
    def notes(self):
        return list(notes.Note.objects(user=self))
