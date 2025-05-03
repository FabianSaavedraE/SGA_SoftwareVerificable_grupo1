from app import db

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    sections = db.relationship(
        'CourseSection',
        backref='teacher',
        lazy=True,
        passive_deletes=True
    )

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
