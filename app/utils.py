import unicodedata
import re

from collections import UserString


SLUG_REGEX = re.compile(r"^[-\w]+$")


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
