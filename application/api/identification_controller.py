from flask import request, jsonify
from flask_restful import Resource
from application import models
from application.services import identification_service


class SignatureIdentification(Resource):
    
    def post(self):
        json = request.get_json()
        user_register_context = identification_service.Identification()
        code, message = user_register_context.train()
        return message, code