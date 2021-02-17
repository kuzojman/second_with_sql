from flask import Flask, request, render_template
from wtforms.validators import InputRequired, Email
from flask_wtf import FlaskForm
from wtforms import StringField,RadioField
from data import teachers, goals,day_in_week_dictionary
import random
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.secret_key = "randomstring"
# Это создаст базу в оперативной памяти, которая очистится после завершения программы.
app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql+psycopg2://postgres:Vovik20121985@localhost/for_second_stepic"
####app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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


teacher_11 = db.session.query(Teacher).get(2)
print("study1" in teacher_11.goals)

teachs = Teacher.query.all()

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

teachers = filling_data_from_database(teachs)

teachs_1 = Teacher.goals.contains("study")
teachs_1 = db.session.query(Teacher.goals.contains("study"))

teachs_1 =Teacher.query.filter(Teacher.goals.contains("study"))



for teach in teachs_1:
    print(teach.name)



#print((teachers[1])["free"])


data_to_json = [{"name":"A",
                "phone":"B",
                "trainer":"C",
                "radio_field_week":"D"}]




class MyForm(FlaskForm):
    trainer = RadioField('trainer', choices=[("Для путешествий", "Для путешествий"),
                                             ("Для школы", "Для школы"),
                                             ("Для работы", "Для работы"),
                                             ("Для переезда", "Для переезда"),])

    radio_field_week = RadioField('radio_field_week', choices=[("1-2 часа в неделю", "1-2 часа в неделю"),
                                                               ("3-5 часа в неделю", "3-5 часа в неделю"),
                                                               ("6-7 часа в неделю", "6-7 часа в неделю"),
                                                               ("8-10 часа в неделю", "8-10 часа в неделю")])

    name  = StringField('name',  [InputRequired()])
    phone = StringField('phone', [InputRequired()])








@app.route('/all')
def render_all():
    return render_template("all.html",
                           teachers=teachers)


@app.route('/all_teach/<word>')
def render_all_teach(word):
    if (word=="rating_best"):
        teachs=Teacher.query.order_by(Teacher.rating.desc()).all()
        teachers = filling_data_from_database(teachs)
    elif (word=="rating_worst"):
        teachs=Teacher.query.order_by(Teacher.rating).all()
        teachers = filling_data_from_database(teachs)
    elif (word=="price_best"):
        teachs=Teacher.query.order_by(Teacher.rating.desc()).all()
        teachers = filling_data_from_database(teachs)
    elif (word=="price_worst"):
        teachs=Teacher.query.order_by(Teacher.rating).all()
        teachers = filling_data_from_database(teachs)


    return render_template("all.html",
                           teachers=teachers)





@app.route('/booking/<number>/<day_in_week>/<time_to_study>')
def render_booking(number,day_in_week,time_to_study):
    form = MyForm()
    return render_template("booking.html",
                           teachers=teachers[int(number)],
                           day_in_week_dictionary=day_in_week_dictionary[day_in_week],
                           time_to_study=time_to_study,
                           form=form
                           )




@app.route('/booking_done/<day_in_week>/<time_to_study>',methods=["POST"])
def render_booking_done(day_in_week,time_to_study):
    form  = MyForm()
    name  = form.name.data
    phone = form.phone.data
    book = Booking(name_client=name,
                      phone=phone,
                      day_in_week=day_in_week,
                        time_to_study=time_to_study)
    db.session.add(book)
    db.session.commit()
    data_to_json_2 = [{"name":name,
                       "phone": phone,
                       "day_in_week":day_in_week,
                       "radio_field_week":time_to_study}]
    data_to_json.append(data_to_json_2)
    with open('result.json', 'w') as fp:
        json.dump(data_to_json, fp)

    return render_template("booking_done.html",
                           time_to_study=time_to_study,
                           day_in_week=day_in_week,
                           name=name,
                           phone=phone)





@app.route('/goal/<purpose>/')
def render_goal(purpose):
    teachs =Teacher.query.filter(Teacher.goals.contains(purpose))
    teachers_2 = filling_data_from_database(teachs)
    goal_to_study = goals[purpose]
    return render_template("goal.html",
                           teachers=teachers_2,
                           goal_to_study=goal_to_study,
                           goals=goals)

@app.route('/')
def render_index():
    teachers_3 = random.sample(teachers,6)
    return render_template("index.html",
                           teachers = teachers_3)


@app.route('/profile/<number>')
def render_profile(number):
    return render_template("profile.html",
                           teachers=teachers[int(number)],
                           goals=goals)



@app.route('/request')
def render_request():
    form  = MyForm()
    return render_template("request.html",
                           form=form)



@app.route('/request_done',methods=["POST"])
def render_request_done():
    form  = MyForm()
    name  = form.name.data
    phone = form.phone.data
    trainer = form.trainer.data
    radio_field_week =form.radio_field_week.data
    proposoal = Proposoal(name_client=name,
                      phone=phone,
                      trainer=trainer,
                        radio_field_week=radio_field_week)
    db.session.add(proposoal)
    db.session.commit()
    data_to_json_2 = [{"name":name,
                       "phone": phone,
                       "trainer":trainer,
                       "radio_field_week":radio_field_week}]

    data_to_json.append(data_to_json_2)
    with open('result.json', 'w') as fp:
        json.dump(data_to_json, fp)
    return render_template("request_done.html",
                           form=form,
                           name=name,
                           phone=phone,
                           trainer =trainer,
                           radio_field_week =radio_field_week)





if __name__ == '__main__':
    app.run()