from app import get_app
from app import configs


app = get_app(configs)


if __name__ == "__main__":
    app.run()
