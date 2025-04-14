from app import db
from sqlalchemy import Enum

class CourseSection(db.Model):
    __tablename__ = 'course_sections'

    id = db.Column(db.Integer, primary_key=True)
    nrc = db.Column(db.String(50), nullable=False)
    overall_ponderation_type = db.Column(
        db.Enum('Porcentaje', 'Peso', name='ponderation_type_enum'),
        nullable=False
    )

    course_instance_id = db.Column(db.Integer, db.ForeignKey('course_instances.id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='SET NULL'), nullable=True)

    student_courses = db.relationship(
    'StudentCourses',
    back_populates='course_section',
    cascade='all, delete-orphan',
    passive_deletes=True
    )

    evaluation_types = db.relationship(
        'EvaluationType',
        backref='course_section',
        lazy=True,
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    
    @property
    def students(self):
        return [sc.student for sc in self.student_courses]

    def __repr__(self):
        return f"<Course Section {self.nrc}>"