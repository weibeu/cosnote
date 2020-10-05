from flask_restx import Namespace


class NamespaceBase(Namespace):

    ROUTE = str()

    def __new__(cls, *args, **kwargs):
        if not cls.ROUTE:
            raise NotImplementedError("Namespace should define a valid route as endpoint.")
        return super().__new__(cls, *args, **kwargs)
