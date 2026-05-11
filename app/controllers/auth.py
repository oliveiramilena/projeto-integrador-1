from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

from app.ext.database import db
from app.ext.oauth import oauth
from app.models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("username")
        password = request.form.get("password")

        if not email or not password:
            flash("Usuário e senha são obrigatórios.")
            return render_template("login.html")

        user = User.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.password, password):  # type: ignore
            flash("Usuário ou senha inválidos.")
            return render_template("login.html")

        login_user(user)
        flash("Login realizado com sucesso.")
        return redirect("/")  # type: ignore

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@auth.route("/auth/google")
def google_login():
    redirect_uri = url_for("auth.google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth.route("/auth/google/callback")
def google_callback():
    token = oauth.google.authorize_access_token()
    userinfo = token.get("userinfo")

    if not userinfo:
        flash("Não foi possível obter as informações do Google.")
        return redirect(url_for("auth.login"))

    google_id = userinfo["sub"]
    email = userinfo["email"]
    name = userinfo.get("name", email)

    user = User.query.filter_by(google_id=google_id).first()

    if user is None:
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User()
            user.name = name  # type: ignore[assignment]
            user.email = email  # type: ignore[assignment]
            user.google_id = google_id  # type: ignore[assignment]
            db.session.add(user)
        else:
            user.google_id = google_id
        db.session.commit()

    login_user(user)
    return redirect("/")
