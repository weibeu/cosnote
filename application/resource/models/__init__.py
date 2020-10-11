from mongoengine.base.metaclasses import TopLevelDocumentMetaclass

import mongoengine


class __DocumentMeta(TopLevelDocumentMetaclass):

    def __new__(mcs, name, bases, attrs):
        meta = attrs.get("meta", dict())
        attrs["meta"] = dict(
            collection=meta.pop("collection", None) or "{}s".format(name.lower()), **meta
        )
        return super().__new__(mcs, name, bases, attrs)


class BaseDocument(mongoengine.Document, metaclass=__DocumentMeta):

    meta = {"abstract": True}


from .user import User
from .notes import Note


__all__ = [
    "User",
    "Note",
]
