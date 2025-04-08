from app import db
from app.models.course_prerequisite import CoursePrerequisite  

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    sections = db.relationship('CourseSection', backref='course', lazy=True)
    
    prerequisites = db.relationship('CoursePrerequisite', back_populates='course', foreign_keys='CoursePrerequisite.course_id')
    prerequired_by = db.relationship('CoursePrerequisite', back_populates='prerequisite', foreign_keys='CoursePrerequisite.prerequisite_id')

    def __repr__(self):
        return f"{self.name}"

