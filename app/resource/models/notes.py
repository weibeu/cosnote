from .user import User
from mongoengine import *


SUPPORTED_LANGUAGES = [
    "text",
    "abap",
    "aes",
    "apex",
    "azcli",
    "bat",
    "c",
    "cameligo",
    "clojure",
    "coffeescript",
    "cpp",
    "csharp",
    "csp",
    "css",
    "dart",
    "dockerfile",
    "fsharp",
    "go",
    "graphql",
    "handlebars",
    "hcl",
    "html",
    "ini",
    "java",
    "javascript",
    "json",
    "julia",
    "kotlin",
    "less",
    "lexon",
    "lua",
    "markdown",
    "mips",
    "msdax",
    "mysql",
    "objective-c",
    "pascal",
    "pascaligo",
    "perl",
    "pgsql",
    "php",
    "plaintext",
    "postiats",
    "powerquery",
    "powershell",
    "pug",
    "python",
    "r",
    "razor",
    "redis",
    "redshift",
    "restructuredtext",
    "ruby",
    "rust",
    "sb",
    "scala",
    "scheme",
    "scss",
    "shell",
    "sol",
    "sql",
    "st",
    "swift",
    "systemverilog",
    "tcl",
    "twig",
    "typescript",
    "vb",
    "verilog",
    "xml",
    "yaml",
]


class NoteMeta(EmbeddedDocument):

    language = StringField(required=True, default="text", choices=SUPPORTED_LANGUAGES)


class Note(Document):

    title = StringField()
    content = StringField(required=True)
    # meta = EmbeddedDocumentField(NoteMeta, default=NoteMeta)

    user = ListField(ReferenceField(User, reverse_delete_rule=CASCADE))
