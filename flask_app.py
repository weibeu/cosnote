from pymongo import MongoClient

from flask import Flask, request, abort, render_template


app = Flask(__name__)
app.secret_key = b'\x86\xf0\x15s\xa4\x84\x91\xd1\x95\x131\xe2\xa9f<['
db_client = MongoClient("mongodb://thecosmos:I2vhyffcplsVoAbr@tc-discord-bot-shard-00-00-i4l5o.mongodb.net:27017,"
                        "tc-discord-bot-shard-00-01-i4l5o.mongodb.net:27017,"
                        "tc-discord-bot-shard-00-02-i4l5o.mongodb.net:27017/test?ssl=true&replicaSet=tc-discord-bot"
                        "-shard-0&authSource=admin")
db = db_client["Quick-Notes"]


@app.route('/')
def index():
    return render_template("index.html")


def __save_note(username, note):
    db.notes.update_one({"username": username}, {
        "$set": {"note": note}
    }, upsert=True)


def __get_note(username):
    return db.notes.find_one({"username": username}, {"_id": False, "pin": False})


def __check_username_availability(username):
    if db.notes.find_one({"username": username}):
        return False
    return True


def __get_pin(username):
    return db.notes.find_one({"username": username}, {"_id": False, "pin": True})["pin"]


@app.route('/<username>/', methods=["GET", "POST"])
def user_notes(username):
    json = request.get_json()
    if "pin" not in json or not json["pin"] == __get_pin(username):
        abort(400)    # Wrong PIN.
    if request.method == "POST":
        if not json or "note" not in json:
            abort(401)
        __save_note(username, json["note"])
    return __get_note(username) or abort(404)
