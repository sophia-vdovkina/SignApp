from flask import request, jsonify
from flask_restful import Resource
from application import models

class TestController(Resource):

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