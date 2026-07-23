# Flask is a lightweight web framework: it lets us turn Python functions
# into endpoints that respond to HTTP requests (like visiting a URL in a browser).
from flask import Flask, jsonify, request

# in-built Python module for dealing with time
from datetime import datetime

# library to load and manage environment variables
from dotenv import load_dotenv

# in-built module for interacting with the operating system
import os

# library for managing database connections
import psycopg2

# Loads variables from the .env.local file (like our database connection string)
# into the environment, so we can read them with os.getenv() instead of hardcoding them. Never use secrets like a connection string openly in your code!
load_dotenv(".env.local")

# Creates the Flask application object. __name__ tells Flask where this file
# lives, which it uses internally to find things like templates and static files.
app = Flask(__name__)


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


# methods=["GET"] means this route only responds to GET requests
# (the default when you type a URL into a browser or "get" data).
@app.route("/authors", methods=["GET"])
def get_authors():
    # Read the database connection string from the environment variables
    # we loaded above via load_dotenv().
    conn_str = os.getenv("PG_URI")
    # Open a connection to the PostgreSQL database...
    connection = psycopg2.connect(conn_str)
    # ...and a cursor, which is what we use to actually send SQL commands.
    cursor = connection.cursor()

    # Ask the database for every row in the "authors" table.
    cursor.execute("SELECT * FROM authors;")

    # fetchall() retrieves all the matching rows as a list of tuples,
    # e.g. [(1, "Astrid Lindgren", 1907), ...].
    rows = cursor.fetchall()

    result = []

    # The database gives us plain tuples, so we convert each row into a
    # dictionary with named keys — that's easier to work with as JSON.
    for row in rows:
        result.append({"id": row[0], "name": row[1], "year": row[2]})

    # Always close the cursor and connection once we're done with them,
    # to free up the resources on the database side.
    cursor.close()
    connection.close()

    return jsonify(result)


# Same URL "/authors" as above, but this route only reacts to POST requests
# (used when a client wants to send/create data, not just read it).
@app.route("/authors", methods=["POST"])
def create_author():
    # request.get_json() reads the JSON body the client sent with their
    # POST request and turns it into a Python dictionary.
    data = request.get_json()
    name = data.get("name")
    year = data.get("year")

    conn_str = os.getenv("PG_URI")
    connection = psycopg2.connect(conn_str)
    cursor = connection.cursor()

    # The %s placeholders are filled in safely with (name, year) by psycopg2.
    # This avoids SQL injection — never build queries with f-strings/string
    # concatenation using user input. RETURNING * gives us the new row back,
    # including the id the database generated for it.
    cursor.execute(
        "INSERT INTO authors (name, year) VALUES (%s, %s) RETURNING *;", (name, year)
    )

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({"id": row[0], "name": row[1], "year": row[2]})

    # commit() saves the INSERT permanently. Without it, the change would be
    # rolled back once the connection closes.
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify(result)


# This block only runs when the file is executed directly (e.g. "python app.py", "flask --debug --app app run --port 8000"),
# not when it's imported by something else — the standard Python entry-point check.
if __name__ == "__main__":
    # print(os.getenv("PG_URI"))
    # Starts Flask's built-in development server so we can try out the routes above.
    app.run()
