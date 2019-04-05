from flask_restful import Resource
from base import Training


class SingleTraining(Resource):

    def get(self):
        return {"response": "hello get"}

    def delete(self):
        return {"response": "hello delete"}


class TrainingsList(Resource):

    def get(self):
        return {'trainings': list(map(lambda x: x.json(), Training.query.all()))}, 200

    def post(self):
        return {"response": "hello post"}

    def put(self):
        return {"response": "hello put"}
