from flask import g
from pymongo import MongoClient


def get_db():
    if "db" not in g:
        g.db_client = MongoClient("mongodb://thecosmos:I2vhyffcplsVoAbr@tc-discord-bot-shard-00-00-i4l5o.mongodb.net"
                                  ":27017,tc-discord-bot-shard-00-01-i4l5o.mongodb.net:27017,"
                                  "tc-discord-bot-shard-00-02-i4l5o.mongodb.net:27017/test?ssl=true&replicaSet=tc"
                                  "-discord-bot-shard-0&authSource=admin")
        g.db = g.db_client["Quick-Notes"]

        return g.db
