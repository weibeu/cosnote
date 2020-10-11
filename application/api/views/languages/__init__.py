from application.resource.models.notes import SUPPORTED_LANGUAGES
from flask import jsonify

from .. import BaseView


class SupportedLanguages(BaseView):

    ROUTE = "/supported-languages/"
    REQUIRES_AUTHORIZATION = False

    @staticmethod
    def get():
        return jsonify(SUPPORTED_LANGUAGES)
