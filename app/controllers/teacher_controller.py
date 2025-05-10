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

    # Estos prints son puro para debugging, se borra cuando este todo listo
    if has_conflict:
        print(f"[DEBUG] Profesor ya tienen sección en {has_conflict.time_slot}")
    else:
        print(f"[INFO] Profesor disponible")

    return has_conflict is None
