from flask import Flask
from flask_restful import Api
from application.database import setup_db

def create_app(config_name):
    
    setup_db()
    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    api = Api(app)

    return app