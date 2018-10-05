from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SECRET_KEY'] = 'some-random-string-that-should-be'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///workout.db"

db = SQLAlchemy(app)

from workout import routes  # noqa