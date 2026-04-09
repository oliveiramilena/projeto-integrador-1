from flask import Blueprint, render_template

home = Blueprint("home", __name__)


@home.route("/")
def inicio():
    return render_template("inicio.html")
