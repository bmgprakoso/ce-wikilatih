from flask_restful import Resource, reqparse
from base import Training
from datetime import datetime


class SingleTraining(Resource):

    def get(self, identity):
        item = Training.query.get(identity)
        if item:
            return item.json()
        return {'message': 'training is not found'}, 400

    def delete(self, identity):
        item = Training.query.get(identity)
        if item:
            item.delete_()
            return {'message': 'training with id={} has been deleted from records'.format(identity)}, 400
        return {'message': 'training with id={} is already not on the list'.format(identity)}


class TrainingsList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True)
    parser.add_argument('instructor', type=str, required=True)
    parser.add_argument('location', type=str, required=True)
    parser.add_argument('start_date', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ'), required=True)
    parser.add_argument('end_date', type=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ'), required=True)

    def get(self):
        return {'trainings': list(map(lambda x: x.json(), Training.query.all()))}

    def post(self):
        args = TrainingsList.parser.parse_args()
        item = Training(args['title'], args['instructor'], args['location'], args['start_date'], args['end_date'])

        item.save_to()
        return item.json()

    # def put(self, movie):
    #     args = MoviesList.parser.parse_args()
    #     item = Movies.find_by_title(movie)
    #     if item:
    #         item.collection = args['collection']
    #         item.save_to()
    #         return {'Movie': item.json()}
    #     item = Movies(movie, args['director'], args['genre'], args['collection'])
    #     item.save_to()
    #     return item.json()
