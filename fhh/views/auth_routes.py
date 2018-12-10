from flask import request, jsonify
import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token,  decode_token, get_raw_jwt
)
from fhh import app, mail
from fhh.models.models import *
from fhh.helpers.send_email import send_reset_email


jwt = JWTManager(app)

blacklist = set()
stored_reset_tokens = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


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
