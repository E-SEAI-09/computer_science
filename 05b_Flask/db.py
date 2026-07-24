# built-in module for reading environment variables (like our DB connection string)
import os

# psycopg2 is the library that lets Python talk to a PostgreSQL database
import psycopg2


# A single reusable helper for running ANY SQL query (SELECT, INSERT, UPDATE, DELETE).
# Every route in authors.py calls this instead of talking to the database directly,
# so the connection/cursor bookkeeping only has to be written once.
def run_query(query, params=None):
    # Read the connection string from the environment (set via .env.local)
    # instead of hardcoding it — keeps secrets out of the source code.
    conn_str = os.getenv("PG_URI")

    # Open a new connection to the database...
    connection = psycopg2.connect(conn_str)
    # ...and a cursor, which is what we use to actually send commands over that connection.
    cursor = connection.cursor()

    # Run the SQL query. `params` is a tuple of values that get safely substituted
    # into the query's %s placeholders — this prevents SQL injection, so never
    # build queries by directly gluing user input into the query string.
    cursor.execute(query, params)

    # SELECT queries return rows, so cursor.description is set; INSERT/UPDATE/DELETE
    # without a RETURNING clause don't return rows, so cursor.description is None.
    # fetchall() would raise an error in that case, hence this check.
    rows = cursor.fetchall() if cursor.description else []

    # commit() makes any changes (INSERT/UPDATE/DELETE) permanent in the database.
    # Without it, the changes would be rolled back when the connection closes.
    connection.commit()
    # Always clean up the cursor and connection once we're done with them.
    cursor.close()
    connection.close()

    return rows
