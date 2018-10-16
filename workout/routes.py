from flask import request, jsonify
import datetime
from jwt import ExpiredSignatureError

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token,  decode_token, get_raw_jwt
)
from workout import app, mail
from workout.models.models import *
from workout.helpers.send_email import send_reset_email


jwt = JWTManager(app)

blacklist = set()
stored_reset_tokens = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


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
        user_data['units'] = user.units
        user_data['admin'] = user.admin
        output.append(user_data)

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
    user_data['units'] = user.units
    user_data['admin'] = user.admin

    return jsonify({'users': user_data})


@app.route("/api/user", methods=['POST'])
def create_user():

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        first_name=data['first_name'], last_name=data['last_name'], password=hashed_password, email=data['email'], admin=False, units=data['units'])  # noqa

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': new_user.first_name + ' created'}), 201


@app.route("/api/user/<user_id>", methods=['PUT'])
def promote_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'})
    user.admin = True
    db.session.commit()
    return jsonify({'message': 'The user has been promoted to Admin'})


@app.route("/api/user/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': user.first_name + ' has heen deleted'})


@app.route("/api/login", methods=['POST'])
def login():

    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Provide login data'})

    user = User.query.filter_by(email=data.get('email')).first()

    if not user:
        return jsonify({'message': 'User not found'})

    if check_password_hash(user.password, data.get('password')):
        access_token = create_access_token(
                identity=user.id, expires_delta=datetime.timedelta(minutes=60))
        if access_token:
            response = {
                    'access_token': access_token,
                    'frist_name': user.first_name,
                    'last_name': user.last_name,
                    'admin': user.admin,
                    'userId': user.id,
                    'message': 'You logged in successfully.'
                }
            return jsonify(response), 200

    return jsonify({'message': 'Wrong Password'})


@app.route("/api/logout", methods=['POST'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"message": "Logout Successful", }), 200


@app.route("/api/reset_password", methods=['POST'])
def reset_password():
    data = request.get_json()

    if not data or not data.get('email'):
        return jsonify({'message': 'Provide your email'})

    user = User.query.filter_by(email=data.get('email')).first()

    if not user:
        return jsonify({'message': 'User not registered yet. Please register'})

    send_reset_email(user)
    print('I wonder', send_reset_email(user))
    return jsonify(
        {'meaasge': "Reset password link has been sent to your email"})


@app.route("/api/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    data = request.get_json()
    return jsonify({'dada': data})


@app.route("/api/add_workout", methods=['POST'])
@jwt_required
def add_workout():
    data = request.get_json()
    user = get_jwt_identity()
    for exercice in Exercises.query.all():
        exercise_id = exercice.id
    new_workout = Workout(
        name=data['name'], notes=data['notes'], bodyweight=data['bodyweight'], user_id=data['email'], exercise=exercise_id)  # noqa

    db.session.add(new_workout)
    db.session.commit()
    return jsonify({'message': new_workout.first_name + ' created'})


@app.route("/api/exercise", methods=['GET'])
def get_exercises():
    exercises = [
        {
            "_id": exercise.id,
            "name": exercise.name,
            "exercise": exercise.exercise,
            "description": exercise.description} for exercise in Exercises.get_exercises()]  # noqa

    if exercises == []:
        return jsonify({"message": "No Exercises"}), 404
    else:
        return jsonify({"message": exercises}), 200
