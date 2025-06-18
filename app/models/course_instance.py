from sqlalchemy import UniqueConstraint

from app import db


class CourseInstance(db.Model):
    """Course instance for a specific year and semester."""

    __tablename__ = "course_instances"
    __table_args__ = (
        UniqueConstraint(
            "course_id", "year", "semester", name="uq_course_year_semester"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    sections = db.relationship(
        "CourseSection",
        backref="course_instance",
        lazy=True,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        """Return a string representation of the instance."""
        return f"<Course Instance {self.id}>"
