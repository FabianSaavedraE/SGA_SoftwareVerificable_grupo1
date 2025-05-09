from app import db

class Schedule(db.Model):
    __tablename__= 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    
    section_id = db.Column(
        db.Integer,
        db.ForeignKey('course_sections.id'),
        nullable=False
    )
    classroom_id = db.Column(
        db.Integer,
        db.ForeignKey('classrooms.id'),
        nullable=False
    )
    time_slot_id = db.Column(
        db.Integer,
        db.ForeignKey('time_slots.id'),
        nullable=False
    )

    section = db.relationship('CourseSection', backref='schedules')
    classroom = db.relationship('Classroom', backref='schedules')
    time_slot = db.relationship('TimeSlot')

    def __repr__(self):
        return f"{self.section_id} -> {self.classroom_id} @ {self.time_slot}"
