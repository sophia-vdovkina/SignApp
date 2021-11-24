from flask import Flask
from flask_restful import Api
import application.database

def create_app(config_name):
    
    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    api = Api(app)

    return app