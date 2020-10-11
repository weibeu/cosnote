from application import get_app
from application import configs


app = get_app(configs)


if __name__ == "__main__":
    app.run()
