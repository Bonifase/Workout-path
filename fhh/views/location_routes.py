from flask import request, jsonify

from fhh import app
from fhh.models.models import *


@app.route("/api/locations", methods=['GET'])
@jwt_required
def all_locations():
    locations = Location.get_locations()
    if locations == []:
        return jsonify({'message': "No locations"})
    return jsonify({"locations": locations})


@app.route("/api/locations/<location_id>", methods=['GET'])
@jwt_required
def location(location_id):
    location = Location.get_location(location_id)
    if location == {}:
        return jsonify({'message': "Location not found"})
    return jsonify({"location": location})


@app.route("/api/locations", methods=['POST'])
@jwt_required
def new_location():
    data = request.get_json()
    location = Location.query.filter_by(name=data.get('name')).first()

    if location:
        return jsonify({'message': "Location already exist"})

    new_location = Location(
        name=data['name'],
        country=data['country'],
        description=data['description'])
    db.session.add(new_location)
    db.session.commit()
    return jsonify({'message': new_location.name + ' created'}), 201


@app.route("/api/locations", methods=['POST'])
@jwt_required
def update_location():
    data = request.get_json()
    location = Location.query.filter_by(name=data.get('name')).first()

    if location:
        return jsonify({'message': "Location already exist"})

    new_location = Location(
        name=data['name'],
        country=data['country'],
        description=data['description'])
    db.session.add(new_location)
    db.session.commit()
    return jsonify({'message': new_location.name + ' created'}), 201
