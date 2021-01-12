# importing libraries
from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import  SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# creating an instance of the flask app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    slot = db.Column(db.Integer , nullable = False)
    name = db.Column(db.String(50),unique = True,nullable = False)

    def __init__(self,slot,name):
        self.slot = slot
        self.name = name

class ScheduleSchema(ma.Schema):
    class Meta:
        fields = ('id','slot','name')

# Init schema
schedule_schema = ScheduleSchema()
schedules_schema = ScheduleSchema(many=True)

@app.route('/booking',methods = ['POST'])
def add_schedule():
    slot = request.json['slot']
    name = request.json['name']

    q1 = Schedule.query.filter_by(slot = slot).all()
    if len(q1) >= 2 :
        return "error"
    else:
        new_schedule = Schedule(slot,name)
        db.session.add(new_schedule)
        db.session.commit()

    return schedule_schema.jsonify(new_schedule)

@app.route('/cancel/<string:name>/<int:slot>',methods = ['DELETE'])
def cancel_schedule(name,slot):
    booked_schedule = Schedule.query.filter_by(name = name,slot = slot).one()
    db.session.delete(booked_schedule)
    db.session.commit()

    return schedule_schema.jsonify(booked_schedule)

@app.route('/allBookings', methods=['GET'])
def get_schedules():
  all_products = Schedule.query.all()
  result = schedules_schema.dump(all_products)
  return jsonify(result)




if __name__ == '__main__':
    app.run(debug = True)

