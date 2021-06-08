from werkzeug.exceptions import abort
import logging
import sqlite3

from flask import (Flask, json, render_template, request,
                   url_for, redirect, flash)


conn_counter = 0


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global conn_counter

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    conn_counter += 1
    return connection


# Function to get all posts in the database
def get_posts():
    connection = get_db_connection()
    posts = connection.execute("SELECT * FROM posts").fetchall()
    connection.close()
    return posts


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute("SELECT * FROM posts WHERE id = ?",
                              (post_id,)).fetchone()
    connection.close()
    return post


# Define the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"


# Define the main route of the web application
@app.route("/")
def index():
    posts = get_posts()
    return render_template("index.html", posts=posts)


# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)

    if post is None:
        app.logger.info("Article ID %d not found. Returning 404.", post_id)
        return render_template("404.html"), 404
    else:
        app.logger.info("Article %s was retrieved.", post['title'])
        return render_template("post.html", post=post)


# Define the About Us page
@app.route("/about")
def about():
    app.logger.info("'About Us' page was retrieved.")

    return render_template("about.html")


# Define the post creation functionality
@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            connection = get_db_connection()
            connection.execute("INSERT INTO posts (title, content)"
                               " VALUES (?, ?)", (title, content))
            connection.commit()
            connection.close()

            app.logger.info("Article %s was created.", title)

            return redirect(url_for("index"))

    return render_template("create.html")


# Define the healthcheck endpoint
@app.route("/healthz", methods=("GET",))
def healthz():
    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype="application/json"
    )
    return response


# Define the metrics endpoint
@app.route("/metrics", methods=("GET",))
def metrics():
    global conn_counter

    posts = len(get_posts())
    response = app.response_class(
        response=json.dumps({"db_connection_count": conn_counter,
                             "post_count": posts}),
        status=200,
        mimetype="application/json"
    )
    return response


# start the application on port 3111
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    app.run(host="0.0.0.0", port="3111")
