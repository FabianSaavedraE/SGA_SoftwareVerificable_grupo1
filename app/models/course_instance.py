from app import db

class CourseInstance(db.Model):
    __tablename__ = 'course_instances'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    sections = db.relationship('CourseSection', backref='course_instance', lazy=True)

    def __repr__(self):
        return f"<Course Intance {self.id}>"