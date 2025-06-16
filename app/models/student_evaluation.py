from app import db


class StudentEvaluations(db.Model):
    __tablename__ = 'student_evaluations'

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id', ondelete='CASCADE'),
        primary_key=True,
    )
    evaluation_id = db.Column(
        db.Integer,
        db.ForeignKey('evaluations.id', ondelete='CASCADE'),
        primary_key=True,
    )
    grade = db.Column(db.Float, nullable=False)

    student = db.relationship(
        'Student', back_populates='student_evaluations', passive_deletes=True
    )
    evaluation = db.relationship(
        'Evaluation',
        back_populates='student_evaluations',
        passive_deletes=True,
    )
