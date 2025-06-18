from app import db


class Course(db.Model):
    """Represents a course with details and relationships."""

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=False, unique=True)
    credits = db.Column(db.Integer, nullable=False, default=0)
    state = db.Column(
        db.Enum("Open", "Closed", name="section_state_enum"),
        nullable=False,
        default="Open",
    )

    instances = db.relationship(
        "CourseInstance",
        backref="course",
        lazy=True,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    prerequisites = db.relationship(
        "CoursePrerequisite",
        back_populates="course",
        foreign_keys="CoursePrerequisite.course_id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    prerequired_by = db.relationship(
        "CoursePrerequisite",
        back_populates="prerequisite",
        foreign_keys="CoursePrerequisite.prerequisite_id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        """Return the course name."""
        return f"{self.name}"
