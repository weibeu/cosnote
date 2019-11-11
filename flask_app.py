from pymongo import MongoClient

from flask_cors import CORS
from flask_restful import Api, Resource
from flask import Flask, request, abort, render_template

app = Flask(__name__)
cors = CORS(app)
api = Api(app)
app.secret_key = b'\x86\xf0\x15s\xa4\x84\x91\xd1\x95\x131\xe2\xa9f<['
db_client = MongoClient("mongodb://thecosmos:I2vhyffcplsVoAbr@tc-discord-bot-shard-00-00-i4l5o.mongodb.net:27017,"
                        "tc-discord-bot-shard-00-01-i4l5o.mongodb.net:27017,"
                        "tc-discord-bot-shard-00-02-i4l5o.mongodb.net:27017/test?ssl=true&replicaSet=tc-discord-bot"
                        "-shard-0&authSource=admin")
db = db_client["instant-notes"]


@app.route('/')
def index():
    return render_template("index.html")


class UserNotes(Resource):

    @staticmethod
    def __register(username, password, note=None):
        document = {"username": username, "password": password}
        if note:
            document["note"] = note
        db.notes.insert_one(document)

    @staticmethod
    def __save_note(username, note):
        db.notes.update_one({"username": username}, {
            "$set": {"note": note}
        })

    @staticmethod
    def __get_note(username):
        return db.notes.find_one({"username": username}, {"_id": False, "password": False})

    @staticmethod
    def __is_username_available(username):
        if db.notes.find_one({"username": username}):
            return False
        return True

    @staticmethod
    def __get_password(username):
        return db.notes.find_one({"username": username}, {"_id": False, "password": True})["password"]

    def post(self):
        print(request.get_json(), request.json)
        if not (json := request.get_json()):
            abort(400)
        if ("username" not in json) or ("password" not in json):
            abort(400)

        username = json["username"]

        if self.__is_username_available(username):  # New user.
            self.__register(username, json["password"], json.get("note"))
        else:
            if "password" not in json or not json["password"] == self.__get_password(username):
                abort(401)  # Wrong password.

            if note := json.get("note"):
                self.__save_note(username, note)

        return self.__get_note(username) or abort(404)


api.add_resource(UserNotes, "/api/")
