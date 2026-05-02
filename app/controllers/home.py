from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user

from app.ext.database import db
from app.models.question import Question

home = Blueprint("home", __name__)


@home.route("/")
def inicio():
    if current_user.is_authenticated:
        return render_template("index.html", name=current_user.name)  # type: ignore

    return render_template("inicio.html")


@home.route("/questionario", methods=["GET", "POST"])
def questionario():
    if request.method == "POST":
        dados = request.get_json(silent=True) or {}
        respostas = dados.get("respostas", {})

        ids = [int(k) for k in respostas if k.isdigit()]
        questoes = Question.query.filter(Question.id.in_(ids)).all()

        acertos = 0
        detalhes = []
        for q in questoes:
            sua_resposta = respostas.get(str(q.id))
            gabarito = q.correct_answer.value
            acertou = sua_resposta == gabarito
            if acertou:
                acertos += 1
            detalhes.append({
                "id": q.id,
                "sua_resposta": sua_resposta,
                "gabarito": gabarito,
                "acertou": acertou,
            })

        return jsonify({
            "acertos": acertos,
            "total": len(questoes),
            "detalhes": detalhes,
        })

    questoes = Question.query.order_by(db.func.random()).all()
    questoes_dict = [
        {
            "id": q.id,
            "statement": q.statement,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "option_e": q.option_e,
            "subject": q.subject,
            "source": q.source,
            "year": q.year,
        }
        for q in questoes
    ]
    return render_template("questionario.html", questions=questoes_dict)