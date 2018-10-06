import os
from flask import Flask
from flask_mail import Mail

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
mail = Mail(app)

app.config['SECRET_KEY'] = 'some-random-string-that-should-be'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///workout.db"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

db = SQLAlchemy(app)

from workout import routes  # noqa