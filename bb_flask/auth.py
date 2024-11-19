import functools, os, hashlib
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from bb_flask.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        cursor = db.cursor()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            # try:
            cursor.execute(
                f"INSERT INTO user_accs (username, password) VALUES ('{username}', '{generate_password_hash(password)}')"
                # (, /),
            )
            db.commit()
            # except cursor.IntegrityError:
            #     error = f"User {username} is already registered."
            # else:
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        cursor = db.cursor()
        print("=== suername ===")
        print(username)
        cursor.execute(f"SELECT * FROM user_accs WHERE username = '{username}'")
        # user = cursor.execute(
        # "SELECT EXISTS ( SELECT FROM user WHERE  table_name   = 'user_accs');"
        # )
        user = cursor.fetchall()[0]
        print("=== useruseruser ===")
        print(user)

        if user is None:
            error = "Incorrect username."
        elif not password:
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user[0]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    db = get_db()
    cursor = db.cursor()

    if user_id is None:
        g.user = None
    else:
        cursor.execute(f"SELECT * FROM user_accs WHERE user_id = {user_id}")
        print("===== =========")
        col_names = [description[0] for description in cursor.description]
        print("colnames", col_names)
        users = cursor.fetchall()[0]
        print("users fetch", users)

        # user_zip = [dict(zip(col_names, user)) for user in users]
        user_zip = {col_names[i]: users[i] for i in range(len(users))}

        print("user zip", user_zip)
        g.user = user_zip
        print(g.user)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
