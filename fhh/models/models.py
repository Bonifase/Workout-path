from flask import Flask
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from fhh import db, app

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


migate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(60))
    phone_number = db.Column(db.String(100))
    y_o_b = db.Column(db.Integer)
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    current_location = db.Column(db.String(100))
    home_town = db.Column(db.String(100))
    country = db.Column(db.String(100))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({"user_id": self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    country = db.Column(db.String(100))
    description = db.Column(db.String(160))

    @staticmethod
    def get_locations():
        locations = [{
            "location_name": location.name,
            "country": location.country,
            "description": location.description
        } for location in Location.query.all()]
        return locations

    @staticmethod
    def get_location(location_id):
        location = Location.query.filter_by(id=location_id).first()
        location_data = {}
        if not location:
            return location_data
        location_data['_id'] = location.id
        location_data['name'] = location.name
        location_data['country'] = location.country,
        location_data['description'] = location.description
        return location_data


if __name__ == '__main__':
    manager.run()
