from flask import Flask
from workout import db, app

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


migate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    units = db.Column(db.String(3))
    workouts = db.relationship('Workout', backref='user', lazy='dynamic')


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notes = db.Column(db.Text)
    bodyweight = db.Column(db.Numeric)
    exercises = db.relationship('Exercise', backref='workout', lazy='dynamic')


class Exercises(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))
    exercise = db.relationship('Exercise', backref='exercise', lazy='dynamic')


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(
        db.Integer, db.ForeignKey('workout.id'), primary_key=True)
    order = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    sets = db.relationship('Set', backref='exercise', lazy='dynamic')


class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Numeric)
    reps = db.Column(db.Integer)
    exercise_id = db.Column(
        db.Integer, db.ForeignKey('exercise.id'), primary_key=True)

if __name__ == '__main__':
    manager.run()