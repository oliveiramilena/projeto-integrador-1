from flask import Blueprint, flash, redirect, render_template, request
from werkzeug.security import check_password_hash
from flask_login import login_user

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

        user =  User.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.password, password): # type: ignore
            flash("Usuário ou senha inválidos.")
            return render_template("login.html")

        login_user(user)
        flash("Login realizado com sucesso.")
        return redirect("/") # type: ignore

    return render_template("login.html")
