from flask import Flask
from .views import init_app
from dotenv import load_dotenv

load_dotenv()
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    init_app(app)

    return app
