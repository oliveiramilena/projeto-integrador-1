from flask import Blueprint, render_template
from flask_login import current_user

home = Blueprint("home", __name__)


@home.route("/")
def inicio():
    if current_user.is_authenticated:
        return render_template("index.html", name=current_user.name) # type: ignore 

    return render_template("inicio.html")

