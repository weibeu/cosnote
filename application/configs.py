import os
import dotenv


dotenv.load_dotenv(".env")


MONGODB_DATABASE = "cosnote"
MONGODB_URI = os.getenv("MONGODB_URI")

SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
USER_NOTES_MAX_LIMIT = 200
