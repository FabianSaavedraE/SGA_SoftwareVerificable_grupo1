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
    teacher_id = get_teacher_id_from_section(section)
    timeslot_ids = extract_timeslot_ids(block)

    return not has_schedule_conflict(teacher_id, timeslot_ids)

def get_teacher_id_from_section(section):
    return section['section'].teacher_id

def extract_timeslot_ids(block):
    return [slot.id for slot in block]

def has_schedule_conflict(teacher_id, timeslot_ids):
    conflict = (
        Schedule.query
        .join(CourseSection)
        .filter(
            CourseSection.teacher_id == teacher_id,
            Schedule.time_slot_id.in_(timeslot_ids)
        )
        .first()
    )

    return conflict is not None

def validate_teacher_overload(ranked_sections, timeslots):
    credits_per_teacher = defaultdict(int)

    for section_info in ranked_sections:
        section = section_info['section']
        credits_per_teacher[section.teacher_id] += section_info['num_credits']

    unique_blocks = set((slot.day, slot.start_time) for slot in timeslots)
    max_blocks_per_teacher = len(unique_blocks)

    for teacher_id, assigned_credits in credits_per_teacher.items():
        if assigned_credits > max_blocks_per_teacher:
            message = (
                f'El profesor con ID {teacher_id} tiene {assigned_credits} '
                f'horas asignadas, pero solo hay {max_blocks_per_teacher} '
                f'bloques disponibles.')
            return False, message
        
    return True, ''

def create_teachers_from_json(data):
    teachers = data.get('profesores', [])
    for teacher in teachers:
        teacher_data = transform_json_entry_into_processable_teacher_format(
            teacher
        )
        create_teacher(teacher_data)

def transform_json_entry_into_processable_teacher_format(teacher):
    name = teacher.get('nombre', '')
    name_parts = name.strip().split()
    data = {
        'first_name' : name_parts[0],
        'last_name' :' '.join(name_parts[1:]) if len(name_parts) > 1 else '',
        'email' : teacher.get('correo')
    }
    return data
