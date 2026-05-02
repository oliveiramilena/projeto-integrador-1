from werkzeug.security import generate_password_hash
from app import create_app
from app.ext.database import db
from app.models.user import User
from app.models.question import Question, AnswerChoice

QUESTIONS = [
    {
        "statement": "Qual é o resultado de 2³ + √16?",
        "option_a": "10",
        "option_b": "12",
        "option_c": "14",
        "option_d": "16",
        "option_e": "20",
        "correct_answer": AnswerChoice.B,
        "subject": "Matemática",
        "source": "ENEM",
        "year": 2022,
    },
    {
        "statement": "Um objeto em queda livre, partindo do repouso, percorre qual distância após 2 segundos? (g = 10 m/s²)",
        "option_a": "5 m",
        "option_b": "10 m",
        "option_c": "20 m",
        "option_d": "40 m",
        "option_e": "80 m",
        "correct_answer": AnswerChoice.C,
        "subject": "Física",
        "source": "FUVEST",
        "year": 2021,
    },
    {
        "statement": "Qual é a fórmula molecular da glicose?",
        "option_a": "C₆H₁₂O₅",
        "option_b": "C₆H₁₂O₆",
        "option_c": "C₁₂H₂₂O₁₁",
        "option_d": "C₂H₅OH",
        "option_e": "CH₄O",
        "correct_answer": AnswerChoice.B,
        "subject": "Química",
        "source": "ENEM",
        "year": 2020,
    },
    {
        "statement": "A Independência do Brasil foi proclamada em:",
        "option_a": "7 de setembro de 1889",
        "option_b": "15 de novembro de 1889",
        "option_c": "7 de setembro de 1822",
        "option_d": "22 de abril de 1500",
        "option_e": "13 de maio de 1888",
        "correct_answer": AnswerChoice.C,
        "subject": "História",
        "source": "UNICAMP",
        "year": 2023,
    },
    {
        "statement": "Qual processo celular é responsável pela produção de ATP na presença de oxigênio?",
        "option_a": "Fotossíntese",
        "option_b": "Fermentação",
        "option_c": "Glicólise anaeróbica",
        "option_d": "Respiração celular aeróbica",
        "option_e": "Osmose",
        "correct_answer": AnswerChoice.D,
        "subject": "Biologia",
        "source": "ENEM",
        "year": 2022,
    },
    {
        "statement": "Qual figura de linguagem está presente em 'A vida é uma viagem'?",
        "option_a": "Metonímia",
        "option_b": "Hipérbole",
        "option_c": "Metáfora",
        "option_d": "Ironia",
        "option_e": "Antítese",
        "correct_answer": AnswerChoice.C,
        "subject": "Português",
        "source": "FUVEST",
        "year": 2021,
    },
    {
        "statement": "Qual é o valor de sen(30°)?",
        "option_a": "√3/2",
        "option_b": "√2/2",
        "option_c": "1",
        "option_d": "1/2",
        "option_e": "0",
        "correct_answer": AnswerChoice.D,
        "subject": "Matemática",
        "source": "ENEM",
        "year": 2019,
    },
    {
        "statement": "Qual é o principal gás responsável pelo efeito estufa antropogênico?",
        "option_a": "Oxigênio (O₂)",
        "option_b": "Nitrogênio (N₂)",
        "option_c": "Dióxido de carbono (CO₂)",
        "option_d": "Argônio (Ar)",
        "option_e": "Hidrogênio (H₂)",
        "correct_answer": AnswerChoice.C,
        "subject": "Geografia",
        "source": "ENEM",
        "year": 2023,
    },
    {
        "statement": "A Lei Áurea, que aboliu a escravidão no Brasil, foi assinada em:",
        "option_a": "13 de maio de 1888",
        "option_b": "15 de novembro de 1889",
        "option_c": "7 de setembro de 1822",
        "option_d": "1 de janeiro de 1863",
        "option_e": "28 de setembro de 1871",
        "correct_answer": AnswerChoice.A,
        "subject": "História",
        "source": "UNICAMP",
        "year": 2022,
    },
    {
        "statement": "Um condutor tem resistência de 10 Ω e é submetido a uma tensão de 220 V. Qual é a corrente elétrica que o percorre?",
        "option_a": "2 A",
        "option_b": "10 A",
        "option_c": "22 A",
        "option_d": "220 A",
        "option_e": "2200 A",
        "correct_answer": AnswerChoice.C,
        "subject": "Física",
        "source": "FUVEST",
        "year": 2020,
    },
]


def seed_user():
    if User.query.filter_by(email="test@example.com").first():
        print("Usuário de testes já existe, pulando.")
        return
    user = User(
        name="Usuário de Testes",  # type: ignore
        email="test@example.com",  # type: ignore
        password=generate_password_hash("password123"),  # type: ignore
    )
    db.session.add(user)
    db.session.commit()
    print(f"Usuário criado: {user.email}")


def seed_questions():
    if Question.query.first():
        print("Questões já existem, pulando.")
        return
    for data in QUESTIONS:
        db.session.add(Question(**data))  # type: ignore
    db.session.commit()
    print(f"{len(QUESTIONS)} questões criadas.")


def seed():
    app = create_app()
    with app.app_context():
        seed_user()
        seed_questions()


if __name__ == "__main__":
    seed()
