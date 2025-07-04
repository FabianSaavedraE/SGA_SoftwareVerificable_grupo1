from app import db


class StudentCourses(db.Model):
    """Model linking students with course sections and their status."""

    __tablename__ = "student_courses"

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id", ondelete="CASCADE"),
        primary_key=True,
    )
    course_section_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "course_sections.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        primary_key=True,
    )
    state = db.Column(
        db.Enum("Inscrito", "Aprobado", "Reprobado", name="state_type_enum"),
        nullable=False,
    )
    final_grade = db.Column(db.Float, nullable=True)

    student = db.relationship(
        "Student", back_populates="student_courses", passive_deletes=True
    )
    course_section = db.relationship(
        "CourseSection", back_populates="student_courses", passive_deletes=True
    )
