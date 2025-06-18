from app import db


class Classroom(db.Model):
    """Classroom model with name and capacity."""

    __tablename__ = "classrooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    schedules = db.relationship(
        "Schedule",
        back_populates="classroom",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        """Return the classroom name."""
        return f"{self.name}"
