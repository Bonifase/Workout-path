from flask import request, jsonify
from workout import app
from workout.models.models import *
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/user", methods=['GET'])
def get_users():
    return ''


@app.route("/user/<user_id>", methods=['GET'])
def get_user():
    return ''


@app.route("/user", methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        first_name=data['first_name'], last_name=data['last_name'], password=hashed_password, admin=False, units=data['units'])  # noqa
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': new_user.first_name + ' created'})


@app.route("/user/<user_id>", methods=['PUT'])
def promote():
    return ''


@app.route("/user/<user_id>", methods=['DELETE'])
def delete_user():
    return ''