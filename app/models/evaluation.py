from app import db


class Evaluation(db.Model):
    """Represents an evaluation with its properties."""

    __tablename__ = "evaluations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ponderation = db.Column(db.Float, nullable=True)
    optional = db.Column(db.Boolean, nullable=True)

    evaluation_type_id = db.Column(
        db.Integer,
        db.ForeignKey("evaluation_types.id", ondelete="CASCADE"),
        nullable=False,
    )

    student_evaluations = db.relationship(
        "StudentEvaluations",
        back_populates="evaluation",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        """Return the evaluation name."""
        return f"<{self.name}>"
