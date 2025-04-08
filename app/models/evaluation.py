from app import db

class Evaluation(db.Model):
    __tablename__ = 'evaluations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ponderation_type = db.Column(db.String(50), nullable=False)
    ponderation = db.Column(db.String(50), nullable=True)
    optional = db.Column(db.String(50), nullable=True)

    evaluation_type_id = db.Column(db.Integer, db.ForeignKey('evaluation_types.id'), nullable=False)
    student_evaluations = db.relationship('StudentEvaluations', back_populates='evaluation')

    def __repr__(self):
        return f"<{self.name}>"
    