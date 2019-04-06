from flask import Flask
from flask_restful import Api
from base import db
from resources.training import SingleTraining, TrainingsList

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

db.init_app(app)
app.app_context().push()
db.create_all()

# routes
api.add_resource(SingleTraining, '/trainings/<string:identity>/')
api.add_resource(TrainingsList, '/trainings/')

if __name__ == '__main__':
    app.run()
