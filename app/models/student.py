from app import db

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    student_courses = db.relationship('StudentCourses', back_populates='student', cascade="all, delete-orphan", passive_deletes=True)
    student_evaluations = db.relationship('StudentEvaluations', back_populates='student', cascade="all, delete-orphan", passive_deletes=True)
    
    @property
    def course_sections(self):
        return [sc.course_section for sc in self.student_courses]

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
        