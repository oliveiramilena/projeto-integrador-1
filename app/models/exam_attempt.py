from app.ext.database import db


class ExamAttempt(db.Model):
    __tablename__ = "exam_attempts"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", backref="exam_attempts")
    answers = db.relationship("ExamAttemptAnswer", backref="attempt", lazy="dynamic")

    @property
    def score_pct(self):
        if self.total_questions == 0:
            return 0
        return round(self.correct_answers / self.total_questions * 100)

    def __repr__(self):
        return f"<ExamAttempt {self.id} user={self.user_id} score={self.correct_answers}/{self.total_questions}>"


class ExamAttemptAnswer(db.Model):
    __tablename__ = "exam_attempt_answers"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    attempt_id = db.Column(db.Integer, db.ForeignKey("exam_attempts.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    given_answer = db.Column(db.String(1), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=False)

    question = db.relationship("Question")

    def __repr__(self):
        return f"<ExamAttemptAnswer attempt={self.attempt_id} q={self.question_id} correct={self.is_correct}>"
