from collections import defaultdict

from app import db
from app.models import Teacher, CourseSection, Schedule

def get_all_teachers():
    teachers = Teacher.query.all()
    return teachers

def get_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    return teacher

def create_teacher(data):
    new_teacher = Teacher(
        first_name = data.get('first_name'),
        last_name = data.get('last_name'),
        email = data.get('email')
    )
    db.session.add(new_teacher)
    db.session.commit()

    return new_teacher

def update_teacher(teacher, data):
    if not teacher:
        return None

    teacher.first_name = data.get('first_name', teacher.first_name)
    teacher.last_name = data.get('last_name', teacher.last_name)
    teacher.email = data.get('email', teacher.email)

    db.session.commit()
    return teacher

def delete_teacher(teacher):
    if not teacher:
        return False

    db.session.delete(teacher)
    db.session.commit()
    return True

def is_teacher_available_for_timeslot(section, block):
    teacher_id = section['section'].teacher_id
    timeslot_ids = [slot.id for slot in block]

    has_conflict = (
        Schedule.query
        .join(CourseSection)
        .filter(
            CourseSection.teacher_id == teacher_id,
            Schedule.time_slot_id.in_(timeslot_ids)
        )
        .first()
    )

    return has_conflict is None

def validate_teacher_overload(ranked_sections, timeslots):
    teacher_load = defaultdict(int)

    for section_data in ranked_sections:
        teacher_id = section_data['section'].teacher_id
        credits = section_data['num_credits']
        teacher_load[teacher_id] += credits

    total_slots = len(set(
        (slot.day, slot.start_time) for slot in timeslots
    ))

    for teacher_id, total_credits in teacher_load.items():
        if total_credits > total_slots:
            return False, f"El profesor con ID {teacher_id} tiene {total_credits} horas asignadas, pero solo hay {total_slots} bloques disponibles."
        
    return True, ""
