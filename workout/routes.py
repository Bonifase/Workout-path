from flask import request, jsonify
from workout import app
from workout.models.models import *
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/user", methods=['GET'])
def get_users():

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['_id'] = user.id
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['email'] = user.email
        user_data['units'] = user.units
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users': output})


@app.route("/user/<user_id>", methods=['GET'])
def get_user(user_id):

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'})

    user_data = {}
    user_data['_id'] = user.id
    user_data['first_name'] = user.first_name
    user_data['last_name'] = user.last_name
    user_data['email'] = user.email
    user_data['units'] = user.units
    user_data['admin'] = user.admin

    return jsonify({'users': user_data})


@app.route("/user", methods=['POST'])
def create_user():

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        first_name=data['first_name'], last_name=data['last_name'], password=hashed_password, email=data['email'], admin=False, units=data['units'])  # noqa

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': new_user.first_name + ' created'})


@app.route("/user/<user_id>", methods=['PUT'])
def promote_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'})
    user.admin = True
    db.session.commit()
    return jsonify({'message': 'The user has been promoted to Admin'})


@app.route("/user/<user_id>", methods=['DELETE'])
def delete_user():
    return ''