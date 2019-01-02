from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity, decode_token, get_raw_jwt
)

from fhh import app
from fhh.models.models import *

jwt = JWTManager(app)


@app.route("/api/user", methods=['GET'])
def get_users():

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['_id'] = user.id
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['email'] = user.email
        user_data['admin'] = user.admin
        output.append(user_data)
    if output == []:
        return jsonify({"message": "There are no users"})

    return jsonify({'users': output})


@app.route("/api/user/<user_id>", methods=['GET'])
def get_user(user_id):

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'}), 401

    user_data = {}
    user_data['_id'] = user.id
    user_data['first_name'] = user.first_name
    user_data['last_name'] = user.last_name
    user_data['email'] = user.email
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


@app.route("/api/user", methods=['POST'])
def create_user():

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        first_name=data['first_name'], last_name=data['last_name'], password=hashed_password, email=data['email'], admin=False)  # noqa

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': new_user.first_name + ' created'}), 201


@app.route("/api/user/<user_id>", methods=['PUT'])
@jwt_required
def update_profile(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'})
    user.location, user.y_o_b = data['location'], data['y_o_b']
    user.admin = True
    db.session.commit()
    return jsonify({'message': 'The user has been promoted to Admin'})


@app.route("/api/user/<user_id>", methods=['DELETE'])
@jwt_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': user.first_name + ' has heen deleted'})
