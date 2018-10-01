from flask import render_template, flash, redirect, url_for
from workout import app


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")