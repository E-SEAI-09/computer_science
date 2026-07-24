from flask import jsonify, request, Blueprint

# run_query is our one shared function for sending SQL to the database (see db.py).
from db import run_query

# A Blueprint groups related routes (everything about "authors") together in
# their own file instead of piling every route into app.py. It behaves like a
# mini Flask app that gets plugged into the real one via app.register_blueprint().
authors_bp = Blueprint("authors", __name__)

# print("__name__ in authors.py", __name__)


# methods=["GET"] means this route only responds to GET requests
# (the default when you type a URL into a browser or "get" data).
# This is the "R" (Read - list) in CRUD: it returns every author in the table.
@authors_bp.route("/authors", methods=["GET"])
def get_authors():
    # run_query() sends the SQL and gives us back a list of rows.
    # Each row is a plain tuple, e.g. (1, "Tolkien", 1892) — no column names attached.
    rows = run_query("select * from authors;")

    # We convert each raw tuple into a dictionary with named keys, since that's
    # what turns into readable JSON like {"id": 1, "name": "Tolkien", "year": 1892}.
    result = []
    for row in rows:
        result.append({"id": row[0], "name": row[1], "year": row[2]})

    # jsonify() turns the Python list of dicts into a proper JSON HTTP response.
    return jsonify(result)
    # Note: the error handling is still missing here, you can implement it as bonus exercise


# Same URL "/authors" as above, but this route only reacts to POST requests
# (used when a client wants to send/create data, not just read it).
# This is the "C" (Create) in CRUD.
@authors_bp.route("/authors", methods=["POST"])
def create_author():
    # request.get_json() reads the JSON body the client sent
    # (e.g. {"name": "Tolkien", "year": 1892}) and turns it into a Python dict.
    data = request.get_json()
    name = data.get("name")
    year = data.get("year")

    # %s are placeholders that psycopg2 fills in safely with the values from
    # the tuple (name, year) — this avoids SQL injection from user input.
    rows = run_query("INSERT INTO authors (name, year) VALUES (%s, %s);", (name, year))

    result = []

    for row in rows:
        result.append({"id": row[0], "name": row[1], "year": row[2]})

    return jsonify(result)
    # Note: the error handling is still missing here, you can implement it as bonus exercise


# Get a single author
# /authors/1  /authors/42
# <int:author_id> is a URL converter: Flask extracts that part of the path,
# converts it to an int, and passes it into the function as the author_id argument.
# This is the "R" (Read - single item) in CRUD.
@authors_bp.route("/authors/<int:author_id>", methods=["GET"])
def get_author_by_id(author_id):
    # try/except catches unexpected errors (e.g. the DB being unreachable) so
    # the client gets a proper JSON error response instead of a crash.
    try:
        row = run_query(
            "SELECT author_id, name, year FROM authors WHERE author_id = %s",
            (author_id,),
        )

        # An empty result means no author with this id exists —
        # 404 is the standard HTTP status code for "not found".
        if not row:
            return jsonify({"error": f"Author with id {author_id} not found"}), 404

        # We only expect one row back since author_id is unique, so we grab the first.
        author = row[0]

        return jsonify({"id": author[0], "name": author[1], "year": author[2]})
    except Exception as e:
        return jsonify({"error": "Something went wrong!", "details": str(e)}), 500


# Update one author
# This is the "U" (Update) in CRUD.
@authors_bp.route("/authors/<int:author_id>", methods=["PUT"])
def update_author(author_id):
    try:
        data = request.get_json()
        name = data.get("name")
        year = data.get("year")

        # Basic input validation: reject the request early if a required
        # field is missing, rather than letting a bad UPDATE hit the database.
        if not name:
            return jsonify({"error": "Author name is required"}), 400

        # RETURNING author_id makes the UPDATE also hand back the id of the row
        # it touched. That's how we can tell whether a matching row existed —
        # UPDATE alone doesn't raise an error if no rows matched the WHERE clause.
        rows = run_query(
            "UPDATE authors SET name = %s, year = %s WHERE author_id = %s RETURNING author_id",
            (name, year, author_id),
        )

        if not rows:
            return jsonify({"error": f"Author with id {author_id} not found"}), 404

        return jsonify({"id": author_id, "name": name, "year": year})
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


# Delete one author
# This is the "D" (Delete) in CRUD.
@authors_bp.route("/authors/<int:author_id>", methods=["DELETE"])
def delete_author(author_id):
    try:
        # Same RETURNING trick as update_author: it tells us whether a row
        # actually existed to delete.
        rows = run_query(
            "DELETE FROM authors WHERE author_id = %s RETURNING author_id", (author_id,)
        )

        if not rows:
            return jsonify({"error": f"Author with id {author_id} not found"}), 404

        # 204 = "No Content": the request succeeded but there's nothing to send back,
        # which fits a delete — there's no resource left to describe.
        return "", 204
    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
