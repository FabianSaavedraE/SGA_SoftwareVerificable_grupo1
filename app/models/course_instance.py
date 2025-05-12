from app import db
from sqlalchemy import UniqueConstraint

class CourseInstance(db.Model):
    __tablename__ = 'course_instances'
    __table_args__ = (
        UniqueConstraint(
            'course_id',
            'year',
            'semester',
            name='uq_course_year_semester'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('courses.id', ondelete='CASCADE'),
        nullable=False
    )
    sections = db.relationship(
        'CourseSection',
        backref='course_instance',
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def __repr__(self):
        return f"<Course Intance {self.id}>"
    