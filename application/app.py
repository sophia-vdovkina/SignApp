from flask import Flask
from flask_restful import Api
import application.database
import application.api.registration_controller as a_test
import application.api.identification_controller as i_test

def create_app(config_name):
    
    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    api = Api(app)
    api.add_resource(a_test.PersonRegistration, "/api/v1/test/hello")
    api.add_resource(a_test.SignatureRegistration, "/api/v1/test/sig")
    api.add_resource(i_test.SignatureIdentification, "/api/v1/test/identificate")
    return app