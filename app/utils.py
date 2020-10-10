import unicodedata
import re
import marshmallow
import mongoengine

from flask import jsonify
from collections import UserString


SLUG_REGEX = re.compile(r"^[-\w]+$")


def format_bad_request(exc=None, **kwargs):
    if isinstance(exc, marshmallow.ValidationError):
        kwargs = {k: v[0] for k, v in exc.messages.items()}
    if isinstance(exc, mongoengine.ValidationError):
        kwargs = {k: v.message for k, v in exc.errors.items()}
    return jsonify(errors=kwargs), 400


class Slug(UserString):

    STRIP_REGEXP = re.compile(r'[^\w\s-]')
    HYPHENATE_REGEXP = re.compile(r'[-\s]+')

    def __init__(self, object_):
        super().__init__(self.slugify(object_))

    def slugify(self, value):
        if not isinstance(value, str):
            value = str(value)
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = str(self.STRIP_REGEXP.sub('', value).strip().lower())
        return self.HYPHENATE_REGEXP.sub('-', value)