from app import db


class TimeSlot(db.Model):
    __tablename__ = 'time_slots'

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return (
            f'{self.day} {self.start_time.strftime("%H:%M")}-'
            f'{self.end_time.strftime("%H:%M")}'
        )
