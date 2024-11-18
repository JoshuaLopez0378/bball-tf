from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from bb_flask.auth import login_required
from bb_flask.db import get_db

bp = Blueprint("nbatf", __name__)


@bp.route("/")
def index():
    db = get_db()
    query = """
        SELECT 
            ug.user_game_id, ug.team_id_choice, at2.full_name as choice_full_name, ug.team_id_opponent, at3.full_name as opp_full_name, 
            case 
                when ug.is_choice_win = true then 'WIN'
                else 'LOSE'
            end as is_choice_win, ug.is_choice_home, ug.game_id 
        FROM user_games ug 
        inner join all_teams at2 
            on at2.team_id = ug.team_id_choice 
        inner join all_teams at3 
            on at3.team_id = ug.team_id_opponent
    """
    cursor = db.cursor()
    cursor.execute(query)
    games = cursor.fetchall()
    print("== games ==")
    print(games)
    print("=== cursor desc ===")
    # print(cursor.description[0])
    col_names = [description[0] for description in cursor.description]
    print(col_names)
    print("=== game zip ===")
    game_zip = [dict(zip(col_names, game_res)) for game_res in games]
    print(game_zip)
    # db.commit()
    return render_template("nbatf/index.html", game=game_zip)


@bp.route("/nbacreate", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id)" " VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("nbatf.index"))

    return render_template("nbatf/choose_game.html")


def get_post(id, check_author=True):
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ?" " WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))
