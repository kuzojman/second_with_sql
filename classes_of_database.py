import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    about = db.Column(db.String, unique=True)
    rating = db.Column(db.String)
    picture = db.Column(db.String, unique=True)
    price = db.Column(db.Integer)
    goals = db.Column(db.String)
    free =  db.Column(db.String)
    bookings = db.relationship("Booking", back_populates='teacher')




class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    name_client = db.Column(db.String)
    phone = db.Column(db.String)
    day_in_week= db.Column(db.String)
    time_to_study = db.Column(db.String)
    teacher = db.relationship("Teacher")
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))



class Proposoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_client = db.Column(db.String)
    phone = db.Column(db.String)
    trainer = db.Column(db.String)
    radio_field_week = db.Column(db.String)

class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_in_english = db.Column(db.String)
    name_in_russian = db.Column(db.String)

def filling_data_from_database(teachs):
    query_teachers_from_database =[]
    for teach in teachs:
        query_teacher_from_database = {'id':teach.id-1,
                                    'name':teach.name,
                                    'about':teach.about,
                                    'rating':teach.rating,
                                    'picture':teach.picture,
                                    'price': teach.price,
                                    'goals':json.loads((teach.goals).replace("'", "\"")),
                                    'free':json.loads((teach.free).replace("'", "\""))
                                    }
        query_teachers_from_database.append(query_teacher_from_database)
    return query_teachers_from_database