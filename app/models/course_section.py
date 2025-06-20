from app import db


class CourseSection(db.Model):
    """Represents a course section with scheduling and enrollment info."""

    __tablename__ = "course_sections"

    id = db.Column(db.Integer, primary_key=True)
    nrc = db.Column(db.String(10), nullable=False)
    overall_ponderation_type = db.Column(
        db.Enum("Porcentaje", "Peso", name="ponderation_type_enum"),
        nullable=False,
    )

    state = db.Column(
        db.Enum("Open", "Closed", name="section_state_enum"),
        nullable=False,
        default="Open",
    )

    course_instance_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "course_instances.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )
    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teachers.id", ondelete="SET NULL"),
        nullable=True,
    )

    student_courses = db.relationship(
        "StudentCourses",
        back_populates="course_section",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    evaluation_types = db.relationship(
        "EvaluationType",
        backref="course_section",
        lazy=True,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    schedules = db.relationship(
        "Schedule",
        back_populates="section",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @property
    def students(self):
        """List students enrolled in this course section."""
        return [
            student_course.student for student_course in self.student_courses
        ]

    def __repr__(self):
        """Return a string representation of the course section."""
        return f"<Course Section {self.nrc}>"
