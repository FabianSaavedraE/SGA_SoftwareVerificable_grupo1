from datetime import date

from app import db


class Student(db.Model):
    """Represents a student with courses and evaluations."""

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    entry_year = db.Column(
        db.Integer, nullable=False, default=date.today().year
    )

    student_courses = db.relationship(
        "StudentCourses",
        back_populates="student",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    student_evaluations = db.relationship(
        "StudentEvaluations",
        back_populates="student",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @property
    def course_sections(self):
        """Return a list of course sections the student is enrolled in."""
        return [
            student_course.course_section
            for student_course in self.student_courses
        ]

    def __repr__(self):
        """Return a readable string representation of the student."""
        return (
            f"ID: {self.id}, Nombre: {self.first_name}, "
            f"Apellido: {self.last_name}, "
            f"Email: {self.email}, Año de Ingreso: {self.entry_year}"
        )
