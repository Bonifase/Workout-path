from workout import app


@app.route("/")
def home():
    return "<h1>Hello world</h1>"