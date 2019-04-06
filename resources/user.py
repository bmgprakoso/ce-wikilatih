from flask_restful import Resource, reqparse
from base import User

class SingleUser(Resource):

    def get(self, identity):
        item = User.query.get(identity)
        if item:
            return item.json()
        return {'message': 'user is not found'}, 400

    def delete(self, identity):
        item = User.query.get(identity)
        if item:
            item.delete_()
            return {'message': 'user with id {} has been deleted from records'.format(identity)}, 400
        return {'message': 'user with id {} is already not on the list'.format(identity)}


class UsersList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    parser.add_argument('role', type=str, required=True)
    parser.add_argument('name', type=str, required=True)
    parser.add_argument('gender', type=str, required=True)
    parser.add_argument('phone', type=str, required=True)
    parser.add_argument('institution', type=str, required=True)

    def get(self):
        return {'users': list(map(lambda x: x.json(), User.query.all()))}

    def post(self):
        args = UsersList.parser.parse_args()
        try:
            item = User(email=args['email'], role=args['role'], name=args['name'], gender=args['gender'],
                        phone=args['phone'], institution=args['institution'])
            item.set_password(args['password'])
            item.save_to()
            return item.json()
        except AssertionError as e:
            return {'message': '{}'.format(e)}, 400

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
