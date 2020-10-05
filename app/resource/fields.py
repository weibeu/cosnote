import re

from app import bcrypt, utils
from mongoengine import StringField


class UsernameField(StringField):

    USERNAME_REGEX = re.compile(r"(?=.{4,20}$)(?![.])(?!.*[.]{2})[a-zA-Z0-9_]+(?<![.])")

    def validate(self, value):
        super().validate(value)
        return bool(self.USERNAME_REGEX.match(value))


class PasswordField(StringField):

    def __init__(self, *args, max_length=128, min_length=5, **kwargs):
        super().__init__(
            *args, **kwargs, max_length=max_length, min_length=min_length, required=True,
        )

    def to_mongo(self, value):
        return bcrypt.generate_password_hash(value).decode("utf-8")

    def validate(self, value):
        if not value:
            self.error("Password is empty.")
        super().validate(value)

    @staticmethod
    def verify(hash_, password):
        return bcrypt.check_password_hash(hash_, password)


class SlugField(StringField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, unique=True)

    def validate(self, value):
        if not utils.SLUG_REGEX.match(value):
            self.error("Provided string is not a slug.")
        super().validate(value)
