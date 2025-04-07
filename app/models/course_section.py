from app import db

class CourseSection(db.Model):
    __tablename__ = 'course_sections'

    id = db.Column(db.Integer, primary_key=True)
    nrc = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(50), nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)

    student_courses = db.relationship('StudentCourses', back_populates='course_section')
    evaluation_types = db.relationship('EvaluationType', backref='course_section', lazy=True)
    
    @property
    def students(self):
        return [sc.student for sc in self.student_courses]

    def __repr__(self):
        return f"<Course Section {self.nrc}>"