from app import db

class StudentCourses(db.Model):
    __tablename__ = 'student_courses'

    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_section_id = db.Column(db.Integer, db.ForeignKey('course_sections.id'), primary_key=True)
    state = db.Column(db.String(50))

    student = db.relationship('Student', back_populates='student_courses')
    course_section = db.relationship('CourseSection', back_populates='student_courses')
