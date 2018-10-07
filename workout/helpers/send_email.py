from workout import mail
from flask import url_for
from workout.models.models import User
from flask_mail import Message


def send_reset_email(user):
    reset_token = user.get_reset_token()
    msg = Message(
        'Password Reset Request',
        sender='jazymula@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, follow the following link: 
    {url_for('reset_token', token=reset_token, _external=True)}
    '''
    mail.send(msg)
