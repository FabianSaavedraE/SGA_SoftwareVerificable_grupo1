from app import db


class EvaluationType(db.Model):
    __tablename__ = 'evaluation_types'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(50), nullable=False)
    ponderation_type = db.Column(
        db.Enum('Porcentaje', 'Peso', name='ponderation_type_enum'),
        nullable=False,
    )
    overall_ponderation = db.Column(db.Float, nullable=False)

    course_section_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'course_sections.id', ondelete='CASCADE', onupdate='CASCADE'
        ),
        nullable=False,
    )

    evaluations = db.relationship(
        'Evaluation',
        backref='evaluation_type',
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True,
    )

    def __rpr__(self):
        return f'{self.topic}'
