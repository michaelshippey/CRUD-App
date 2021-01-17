import datetime
import json
import os
from psycopg2.extras import RealDictCursor
import psycopg2
from datetime import datetime
from flask import send_file, make_response
from flask import Flask, jsonify, request, json, flash, redirect, url_for
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from validate_email import validate_email
from flask import Flask, render_template, request
from flask_session import Session
from flask import session
from flask_socketio import SocketIO, emit
from DBinfo import DatabaseConfig

from datetime import date

userid = -1
logflag = "0"


def create_app():
    app = Flask(__name__)
    app.secret_key = "CS471-team2"

    app.config["SECRET_KEY"] = "CS471-team2"
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PERMANENT"] = False
    app.config["CORS_HEADERS"] = "Content-Type"
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    local_host = psycopg2.connect(
        host=DatabaseConfig.db_host,
        port=DatabaseConfig.db_port,
        user=DatabaseConfig.db_user,
        password=DatabaseConfig.db_passwd,
        dbname=DatabaseConfig.db_database,
    )

    @app.route("/", methods=["GET", "POST"])
    def base_route():
        return render_template("index.html")

    @app.route("/index.html", methods=["GET", "POST"])
    def index_route():
        return render_template("index.html")

    @app.route("/review.html", methods=["GET", "POST"])
    def review_route():
        return render_template("review.html")

    @app.route("/signup.html", methods=["GET", "POST"])
    def signup_route():
        return render_template("signup.html")

    @app.route("/login.html", methods=["GET", "POST"])
    def login_route():
        return render_template("login.html")

    @app.route("/history.html", methods=["GET", "POST"])
    def history_route():
        return render_template("history.html")

    @app.route("/history/update", methods=["GET", "POST"])
    def update_review():
        print("hello")
        cur = local_host.cursor()
        score = request.form["score"]
        movie = request.form["movie"]
        new_movie = movie.replace("'", "''")
        comment = request.form["comment"]
        date = datetime.utcnow()
        cur.execute(
            "UPDATE "
            + DatabaseConfig.db_review_table
            + " SET "
            + "score = "
            + str(score)
            + ", "
            + "comment = '"
            + str(comment)
            + "'"
            + ", "
            + "update_date = '"
            + str(date)
            + "'"
            + " WHERE "
            + "reviews.user_id = "
            + str(userid)
            + " AND reviews.movie = '"
            + str(new_movie)
            + "'"
            + ""
        )
        local_host.commit()
        return "true"

    @app.route("/history", methods=["GET", "POST"])
    def display_review():
        cur = local_host.cursor()
        s = ""
        s += "SELECT * FROM "
        s += DatabaseConfig.db_review_table
        s += " WHERE "
        s += "reviews.user_id = "
        s += str(userid)
        s += ";"
        cur.execute(s)
        array_names = json.dumps(cur.fetchall())
        cur.close()
        if os.path.exists("static/data/history.json"):
            os.remove("static/data/history.json")

        f = open("static/data/history.json", "a")
        f.write(array_names)
        f.close
        return array_names

    @app.route("/history/delete", methods=["GET", "POST"])
    def delete_review():
        print("hello")

        cur = local_host.cursor()
        date = request.form["date"]
        print(
            "DELETE FROM "
            + DatabaseConfig.db_review_table
            + " WHERE "
            + 'reviews.update_date = "'
            + str(date)
            + '"'
        )
        cur.execute(
            "DELETE FROM "
            + DatabaseConfig.db_review_table
            + " WHERE "
            + "reviews.update_date = '"
            + str(date)
            + "'"
        )

        local_host.commit()
        return redirect(url_for("history_route"))

    @app.route("/review/create", methods=["GET", "POST"])
    def create_review():
        print("hi")
        print("userid:", userid)
        cur = local_host.cursor()
        print(request.form)
        score = request.form["score"]
        movie = request.form["title"]
        new_movie = movie.replace("'", "''")
        comment = request.form["comment"]
        date = datetime.utcnow()
        user_id = userid

        created_at = datetime.utcnow()

        cur.execute(
            "INSERT INTO "
            + DatabaseConfig.db_review_table
            + "(score, movie,comment, update_date, user_id) VALUES ('"
            + str(score)
            + "', '"
            + str(new_movie)
            + "', '"
            + str(comment)
            + "', '"
            + str(date)
            + "', '"
            + str(user_id)
            + "')"
        )

        local_host.commit()

        return "true"

    @app.route("/users/register", methods=["GET", "POST"])
    def register():
        cur = local_host.cursor()
        print("new user registered")
        print(request.form)
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        username = request.form["username"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode(
            "utf-8"
        )
        created_at = datetime.utcnow()

        cur.execute(
            "INSERT INTO "
            + DatabaseConfig.db_user_table
            + " (first_name, last_name,username, email, password, created_at) VALUES ('"
            + str(first_name)
            + "', '"
            + str(last_name)
            + "', '"
            + str(username)
            + "', '"
            + str(email)
            + "', '"
            + str(password)
            + "', '"
            + str(created_at)
            + "')"
        )

        local_host.commit()

        if validate_email(email):

            result = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "created": created_at,
            }
            print("user registered successfully")
            return jsonify({"result": result})
        else:
            return "Invalid Information"

    @app.route("/login", methods=["GET", "POST"])
    def login():
        global userid
        global logflag
        cur = local_host.cursor(cursor_factory=RealDictCursor)
        print("new log in ")
        print(request.form)
        email = request.form["email"]
        password = request.form["password"]

        print(email)
        print(password)
        cur.execute(
            "SELECT id, first_name, last_name, email, username, password, created_at FROM {} WHERE email='{}'".format(
                DatabaseConfig.db_user_table, str(email)
            )
        )

        rv = cur.fetchone()
        print("*" * 50)
        print(rv)
        print("*" * 50)

        if rv is not None and bcrypt.check_password_hash(rv["password"], password):
            access_token = create_access_token(
                identity={
                    "id": rv["id"],
                    "first_name": rv["first_name"],
                    "last_name": rv["last_name"],
                    "email": rv["email"],
                    "username": rv["username"],
                }
            )
            result = access_token

            userid = rv["id"]
            print("userid in login: ", userid)
            session.permanent = True
            session["user"] = rv["username"]
            logflag = "1"

        else:
            result = "Invalid username or password"
        # redirect(url_for("history_route"))
        # return result
        return redirect(url_for("history_route"))

    @app.route("/logout")
    def logout():
        global userid
        global logflag
        userid = -1
        logflag = "0"
        session.pop("user", None)
        return redirect(url_for("login_route"))

    @app.route("/logincheck")
    def logincheck():
        print("logflag:", logflag)

        return logflag

    return app


app = create_app()

if __name__ == "__main__":
    sess = Session()
    sess.init_app(app)
    app.run(port=5000, debug=True)
