# Flask is a lightweight web framework: it lets us turn Python functions
# into endpoints that respond to HTTP requests (like visiting a URL in a browser).
from flask import Flask, jsonify, request

# built-in Python module for dealing with time
from datetime import datetime

# library to load and manage environment variables
from dotenv import load_dotenv

# built-in module for interacting with the operating system
import os

# library for managing database connections
import psycopg2

# authors_bp is a Blueprint: a self-contained set of routes defined in authors.py.
# Blueprints let us split routes across multiple files instead of putting
# everything into one giant app.py.
from authors import authors_bp

# Loads variables from the .env.local file (like our database connection string)
# into the environment, so we can read them with os.getenv() instead of hardcoding them. Never use secrets like a connection string openly in your code!
load_dotenv(".env.local")

# Creates the Flask application object. __name__ tells Flask where this file
# lives, which it uses internally to find things like templates and static files.
app = Flask(__name__)

# Registering the blueprint "activates" all the routes defined in authors.py
# (e.g. /authors, /authors/<id>) on this app, exactly as if they'd been
# written here with @app.route directly.
app.register_blueprint(authors_bp)


# @app.route(...) is a decorator: it tells Flask "when someone visits this URL,
# run the function right below me". This connects the URL "/" to hello().
@app.route("/")
def hello():
    # print(not_present)
    # Whatever a route function returns becomes the HTTP response body.
    # A plain string is sent back as-is (Flask wraps it as an HTML response).
    return "Hello, World!"


@app.route("/time")
def right_now():
    now = datetime.now()
    # f-strings let us embed the now variable directly inside the HTML string.
    return f"<h1>It's currently: {now}</h1>"


@app.route("/person")
def some_person():
    # A regular Python dictionary — Flask can't send this back directly,
    # it needs to be converted into JSON text first.
    my_dictionary = {
        "name": "Guybrush",
        "occupation": "pirate",
        "hobbies": ["pillaging", "sailing", 42, True],
    }
    # jsonify() converts the dictionary into a proper JSON HTTP response
    # (it also sets the required header for us).
    return jsonify(my_dictionary)


# This block only runs when the file is executed directly (e.g. "python app.py", "flask --debug --app app run --port 8000"),
# not when it's imported by something else — the standard Python entry-point check.
if __name__ == "__main__":
    # print(os.getenv("PG_URI"))
    # Starts Flask's built-in development server so we can try out the routes above.
    app.run()
