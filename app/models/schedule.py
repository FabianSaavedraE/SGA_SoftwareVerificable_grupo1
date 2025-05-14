from app import db

class Schedule(db.Model):
    __tablename__= 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    
    section_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'course_sections.id', ondelete='CASCADE', onupdate='CASCADE'
        ),
        nullable=False
    )
    classroom_id = db.Column(
        db.Integer,
        db.ForeignKey('classrooms.id', ondelete='CASCADE'),
        nullable=False
    )
    time_slot_id = db.Column(
        db.Integer,
        db.ForeignKey('time_slots.id'),
        nullable=False
    )

    classroom = db.relationship('Classroom', back_populates='schedules')
    section = db.relationship('CourseSection', back_populates='schedules')
    time_slot = db.relationship('TimeSlot')

    def __repr__(self):
        return f'{self.section_id} -> {self.classroom_id} @ {self.time_slot}'
