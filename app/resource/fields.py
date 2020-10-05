import unicodedata
import re

from app import bcrypt
from mongoengine import StringField


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

    STRIP_REGEXP = re.compile(r'[^\w\s-]')
    HYPHENATE_REGEXP = re.compile(r'[-\s]+')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, unique=True)

    def slugify(self, value):
        if not isinstance(value, str):
            value = str(value)
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = str(self.STRIP_REGEXP.sub('', value).strip().lower())
        return self.HYPHENATE_REGEXP.sub('-', value)
