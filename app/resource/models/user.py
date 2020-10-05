from mongoengine import Document, StringField, EmbeddedDocument, EmbeddedDocumentField, BooleanField

from ..fields import PasswordField


class UserPreferences(EmbeddedDocument):

    developer = BooleanField(default=False)


class User(Document):

    username = StringField(minimum_length=5, max_length=20, primary_key=True)
    password = PasswordField()
    preferences = EmbeddedDocumentField(UserPreferences, default=UserPreferences)
