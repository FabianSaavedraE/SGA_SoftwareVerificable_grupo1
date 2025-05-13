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

    return new_teacher, None

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


def validate_teacher_data(data):
    errors = []

    first_name = data.get('first_name', '').strip()
    if len(first_name) > MAX_LENGTH_FIRST_NAME:
        errors.append(
            f"El nombre es demasiado largo (máx. "
            f"{MAX_LENGTH_FIRST_NAME} caracteres)."
        )

    last_name = data.get('last_name', '').strip()
    if len(last_name) > MAX_LENGTH_LAST_NAME:
        errors.append(
            f"El apellido es demasiado largo (máx. "
            f"{MAX_LENGTH_LAST_NAME} caracteres)."
        )    

    email = data.get('email', '').strip()
    if len(email) > MAX_LENGTH_EMAIL:
        errors.append(
            f"El email es demasiado largo (máx. {MAX_LENGTH_EMAIL} caracteres)"
        )

    return errors

def create_teachers_from_json(data):
    teachers = data.get('profesores', [])
    for teacher in teachers:
        name = teacher.get('nombre', '')
        name_parts = name.strip().split()
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        new_teacher = Teacher(
            first_name=first_name,
            last_name=last_name,
            email=teacher.get('correo'),
        )
        db.session.add(new_teacher)

    db.session.commit()

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
            message = (
                f"El profesor con ID {teacher_id} tiene {total_credits} horas "
                f"asignadas, pero solo hay {total_slots} bloques disponibles.")
            return False, message
        
    return True, ""

def create_teachers_from_json(data):
    teachers = data.get('profesores', [])
    for teacher in teachers:
        name = teacher.get('nombre', '')
        name_parts = name.strip().split()
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        new_teacher = Teacher(
            first_name=first_name,
            last_name=last_name,
            email=teacher.get('correo'),
        )
        db.session.add(new_teacher)

    db.session.commit()