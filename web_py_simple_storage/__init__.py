from flask import Flask


def create_app():
    app = Flask(__name__)
    
    from web_py_simple_storage.routes import app as home
    app.register_blueprint(home)

    return app

