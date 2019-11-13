import random
import string

from pymongo import MongoClient

from flask_cors import CORS
from flask_restful import Api, Resource
from flask import Flask, request, abort, render_template, session

app = Flask(__name__)
cors = CORS(app)
api = Api(app)
app.secret_key = b"'\x14Q\x17\xda\xc6\x8f\x01V\x9et\xdf\x81\xa0$m"
db_client = MongoClient("mongodb://thecosmos:I2vhyffcplsVoAbr@tc-discord-bot-shard-00-00-i4l5o.mongodb.net:27017,"
                        "tc-discord-bot-shard-00-01-i4l5o.mongodb.net:27017,"
                        "tc-discord-bot-shard-00-02-i4l5o.mongodb.net:27017/test?ssl=true&replicaSet=tc-discord-bot"
                        "-shard-0&authSource=admin")
db = db_client["instant-notes"]


@app.route('/')
def index():
    return render_template("index.html")


def get_user_info():
    json = request.get_json() or dict()
    username = json.get("username")
    password = json.get("password")
    if not username:
        abort(400)
    if not password:
        abort(400)
    return username, password, json.get("note")


def update_session(**kwargs):
    session.update(kwargs)


class UserNotes(Resource):

    BASE_URL = "/api/"

    @staticmethod
    def __save_note(username, password, note=None):
        document = {"password": password}
        if note:
            document["note"] = note
        db.notes.update_one({"username": username}, {"$set": document}, upsert=True)

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
        username, password, note = get_user_info()
        if self.__is_username_available(username):    # New user.
            # No password check for new users.
            update_session(username=username, password=password)
            self.__save_note(username, password, note)
        else:
            if not password == self.__get_password(username):
                abort(401)  # Wrong password.
            update_session(username=username, password=password)
            self.__save_note(username, password, note)

        return self.__get_note(username) or abort(404)

    @staticmethod
    def get():
        username = session.get("username", str())
        password = session.get("password", str())
        if not (username and password):
            abort(400)
        return dict(username=username, password=password)


class ShareNote(Resource):

    BASE_URL = "/api/share/"

    @staticmethod
    def __get_random_uri():
        return str().join(random.choices(string.ascii_letters + string.digits, k=7))

    def post(self):
        username, password, _ = get_user_info()

        note = db.notes.find_one({"username": username, "password": password}, {"note": True, "_id": False}).get("note")
        if not note:
            abort(404)    # That user hasn't created any note yet.
        uri = self.__get_random_uri()
        db.sharedNotes.update_one({"username": username}, {"$set": {
            "note": note,
            "uri": uri
        }}, upsert=True)
        return {
            "share_url": f"{request.base_url.replace(self.BASE_URL, str())}/shared/{uri}/"
        }


class RevokeAuth(Resource):

    BASE_URL = "/api/revoke/"

    @staticmethod
    def delete():
        session.clear()
        return dict(), 200


@app.route('/shared/<uri>/')
def get_shared_note(uri):
    payload = db.sharedNotes.find_one({"uri": uri}, {"_id": False}) or abort(404)
    return render_template("index.html", shared=payload)


api.add_resource(UserNotes, UserNotes.BASE_URL)
api.add_resource(ShareNote, ShareNote.BASE_URL)
api.add_resource(RevokeAuth, RevokeAuth.BASE_URL)
