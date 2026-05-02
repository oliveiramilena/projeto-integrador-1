import enum

from app.ext.database import db


class AnswerChoice(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now()
    )
    statement = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    option_e = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Enum(AnswerChoice), nullable=False)
    subject = db.Column(db.String(64), nullable=False)
    source = db.Column(db.String(64), nullable=True)
    year = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Question {self.id} - {self.subject} ({self.year})>"
