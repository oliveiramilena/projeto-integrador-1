from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from sqlalchemy import func

from app.ext.database import db
from app.models.question import Question
from app.models.exam_attempt import ExamAttempt, ExamAttemptAnswer

home = Blueprint("home", __name__)


@home.route("/")
def inicio():
    if current_user.is_authenticated:
        return render_template("index.html")

    return render_template("inicio.html")


@home.route("/questionario", methods=["GET"])
def questionario():
    materias = db.session.query(Question.subject).distinct().order_by(Question.subject).all()
    materias = [m[0] for m in materias]
    return render_template("questionario_config.html", materias=materias)


@home.route("/questionario/iniciar", methods=["GET"])
def questionario_iniciar():
    materias_sel = request.args.getlist("materias")
    quantidade = request.args.get("quantidade", 10, type=int)
    tempo_min = request.args.get("tempo", 60, type=int)

    quantidade = max(1, min(quantidade, 100))
    tempo_min = max(1, min(tempo_min, 240))

    query = Question.query
    if materias_sel:
        query = query.filter(Question.subject.in_(materias_sel))

    questoes = query.order_by(db.func.random()).limit(quantidade).all()

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
    return render_template("questionario.html", questions=questoes_dict, tempo_min=tempo_min)


@home.route("/questionario/responder", methods=["POST"])
def questionario_responder():
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

    if current_user.is_authenticated:
        attempt = ExamAttempt(
            user_id=current_user.id, # type: ignore
            total_questions=len(questoes), # type: ignore
            correct_answers=acertos, # type: ignore
        )
        db.session.add(attempt)
        db.session.flush()

        for detalhe in detalhes:
            db.session.add(ExamAttemptAnswer(
                attempt_id=attempt.id, # type: ignore
                question_id=detalhe["id"], # type: ignore
                given_answer=detalhe["sua_resposta"], # type: ignore
                is_correct=detalhe["acertou"], # type: ignore
            ))

        db.session.commit()

    return jsonify({
        "acertos": acertos,
        "total": len(questoes),
        "detalhes": detalhes,
    })


@home.route("/historico")
@login_required
def historico():
    tentativas = (
        ExamAttempt.query
        .filter_by(user_id=current_user.id)
        .order_by(ExamAttempt.created_at.desc())
        .all()
    )
    return render_template("historico.html", tentativas=tentativas)


@home.route("/desempenho")
@login_required
def desempenho():
    resumo = db.session.query(
        func.count(ExamAttempt.id).label("total_simulados"),
        func.sum(ExamAttempt.total_questions).label("total_questoes"),
        func.avg(
            ExamAttempt.correct_answers * 100.0 / ExamAttempt.total_questions
        ).label("media_aproveitamento"),
    ).filter(ExamAttempt.user_id == current_user.id).first()

    por_materia = db.session.query(
        Question.subject,
        func.count(ExamAttemptAnswer.id).label("total"),
        func.sum(
            db.case((ExamAttemptAnswer.is_correct, 1), else_=0)
        ).label("acertos"),
    ).join(Question, ExamAttemptAnswer.question_id == Question.id
    ).join(ExamAttempt, ExamAttemptAnswer.attempt_id == ExamAttempt.id
    ).filter(ExamAttempt.user_id == current_user.id
    ).group_by(Question.subject
    ).order_by(func.count(ExamAttemptAnswer.id).desc()
    ).all()

    evolucao = (
        ExamAttempt.query
        .filter_by(user_id=current_user.id)
        .order_by(ExamAttempt.created_at.asc())
        .limit(10)
        .all()
    )

    return render_template(
        "desempenho.html",
        resumo=resumo,
        por_materia=por_materia,
        evolucao=evolucao,
    )