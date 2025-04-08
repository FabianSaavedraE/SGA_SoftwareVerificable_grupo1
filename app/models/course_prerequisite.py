from app import db

class CoursePrerequisite(db.Model):
    __tablename__ = 'course_prerequisites'

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    prerequisite_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)

    course = db.relationship('Course', foreign_keys=[course_id], back_populates='prerequisites')
    prerequisite = db.relationship('Course', foreign_keys=[prerequisite_id], back_populates='prerequired_by')
