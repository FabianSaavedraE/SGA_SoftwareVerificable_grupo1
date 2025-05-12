from app import db

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=False, unique=True)
    credits = db.Column(db.Integer, nullable=False, default=0)

    instances = db.relationship(
        'CourseInstance',
        backref='course',
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    prerequisites = db.relationship(
        'CoursePrerequisite',
        back_populates='course',
        foreign_keys='CoursePrerequisite.course_id',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    prerequired_by = db.relationship(
        'CoursePrerequisite',
        back_populates='prerequisite',
        foreign_keys='CoursePrerequisite.prerequisite_id',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def __repr__(self):
        return f"{self.name}"
