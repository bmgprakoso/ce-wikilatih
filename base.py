from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    instructor = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, title, instructor, location, start_date, end_date):
        self.title = title
        self.instructor = instructor
        self.location = location
        self.start_date = start_date
        self.end_date = end_date

    def json(self):
        return {'id': self.id, 'title': self.title, 'instructor': self.instructor, 'location': self.location,
                'start_date': str(self.start_date), 'end_date': str(self.end_date)}

    def save_to(self):
        db.session.add(self)
        db.session.commit()

    def delete_(self):
        db.session.delete(self)
        db.session.commit()
