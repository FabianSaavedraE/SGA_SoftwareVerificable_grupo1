from collections import defaultdict
from sqlalchemy import func

from app import db
from app.models import CourseSection, Schedule, Teacher
from app.validators.data_load_validators import (
    validate_entry_can_be_loaded,
    validate_entry_has_required_keys,
    validate_json_has_required_key,
)

TEACHERS_JSON_KEY = 'profesores'
KEY_ID_ENTRY = 'id'
KEY_NAME_ENTRY = 'nombre'
KEY_MAIL_ENTRY = 'correo'
KEYS_NEEDED_FOR_TEACHER_JSON = [KEY_ID_ENTRY, KEY_MAIL_ENTRY, KEY_NAME_ENTRY]


def get_all_teachers():
    teachers = Teacher.query.all()
    return teachers


def get_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    return teacher


def create_teacher(data):
    teacher_id = data.get('teacher_id')
    
    new_teacher = Teacher(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
    )
    
    if teacher_id is not None:
        new_teacher.id = teacher_id
    
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
        Schedule.query.join(CourseSection)
        .filter(
            CourseSection.teacher_id == teacher_id,
            Schedule.time_slot_id.in_(timeslot_ids),
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
                f'bloques disponibles.'
            )
            return False, message

    return True, ''


def create_teachers_from_json(data):
    if not validate_json_has_required_key(data, TEACHERS_JSON_KEY):
        return None

    teachers = data.get('profesores', [])

    # Validation cicle  (Will break if an entry it's not valid -----------------
    for teacher in teachers:
        if not validate_entry_has_required_keys(
            teacher, KEYS_NEEDED_FOR_TEACHER_JSON
        ):
            return None

        if not validate_entry_can_be_loaded(
            transform_json_entry_into_processable_teacher_format(teacher),
            'teacher',
        ):
            return None

    # Creation cicle (Will only execute if ALL validations pass) -----------
    # (Thus, two for cicles are needed) ------------------------------------
    for teacher in teachers:
        id = teacher.get('id')
        teacher_data = transform_json_entry_into_processable_teacher_format(
            teacher
        )
        
        if check_if_teacher_with_id_exists(id):
            handle_teacher_with_existing_id(id)
        
        if teacher_data:
            create_teacher(teacher_data)
        else:
            break


def transform_json_entry_into_processable_teacher_format(teacher):
    name = teacher.get('nombre', '')
    data = {
        'first_name': name.split()[0] if isinstance(name, str) else name,
        'last_name': ' '.join(name.split()[1:])
        if (isinstance(name, str) and len(name.split()) > 1)
        else (''),
        'email': teacher.get('correo'),
        'teacher_id': teacher.get('id')
    }
    return data


def check_if_teacher_with_id_exists(id):
    teacher = Teacher.query.filter_by(id=id).first()
    if teacher:
        return True
    else:
        return False
    
    
def handle_teacher_with_existing_id(id):
    teacher = Teacher.query.filter_by(id=id).first()
    max_id = db.session.query(func.max(Teacher.id)).scalar() or 0
    new_id = max_id + 1

    teacher.id = new_id
    db.session.commit()