import os
from fhh import mail
from flask import url_for
from fhh.models.models import User
from flask_mail import Message

sender = os.environ.get('EMAIL_USER')


def send_reset_email(user):
    reset_token = user.get_reset_token()
    msg = Message(
        subject='Password Reset Request', recipients=[user.email],
        sender="hcravens25@gmail.com",
        body=f'''To reset your password, follow the following link: 
    {url_for('reset_token', token=reset_token, _external=True)}
    ''')
    
    mail.send(msg)
