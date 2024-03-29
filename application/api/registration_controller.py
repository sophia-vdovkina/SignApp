from flask import request, jsonify
from flask_restful import Resource
from application import models
from application.services import registration_services


class PersonRegistration(Resource):
    
    def post(self):
        json = request.get_json()
        user_register_context = registration_services.PersonRegistrationService(json)
        code, message = user_register_context.register()
        return message, code


class SignatureRegistration(Resource):
    def post(self):
        json = request.get_json()
        user_register_context = registration_services.SignatureRegistrationService(json)
        code, message = user_register_context.register()
        return message, code

class RegistrationController(Resource):

    def get(self):
        json = {"hello": "world"}
        result = models.Feature.query.all()
        return jsonify(result)

    def post(self):
        json = request.json
        print(json['name'])

    def put(self):
        pass

    def delete(self):
        pass