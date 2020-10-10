from ..fields import UsernameField
from ..fields import PasswordField

from mongoengine import Document, EmbeddedDocument
from mongoengine import EmbeddedDocumentField, BooleanField, EmailField


class UserPreferences(EmbeddedDocument):

    developer = BooleanField(default=False)


class User(Document):

    username = UsernameField(minimum_length=5, max_length=20, primary_key=True)
    email = EmailField()
    password = PasswordField(required=True)
    preferences = EmbeddedDocumentField(UserPreferences, default=UserPreferences)
