from app import db

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    sections = db.relationship('CourseSection', backref='course', lazy=True)

    def __repr__(self):
        return f"{self.name}"