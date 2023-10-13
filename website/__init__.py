from flask import Flask
from .views import init_app
# from dotenv import load_dotenv

# load_dotenv()
import os


def create_app():
    app = Flask(__name__)
    # app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SECRET_KEY'] = 'kfjsdf616sgsgt4gtd6gs4'
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'instances', 'pdf_database')

    init_app(app)

    return app
