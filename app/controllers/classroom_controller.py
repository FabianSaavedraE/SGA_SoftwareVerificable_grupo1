from app import db
from app.models import Classroom, Schedule
from app.validators.data_load_validators import (
    validate_entry_can_be_loaded,
    validate_entry_has_required_keys,
    validate_json_has_required_key,
    flash_custom_error
)
from app.validators.constants import *

KEYS_NEEDED_FOR_CLASSROOM_JSON = [
    KEY_ID_ENTRY,
    KEY_CLASSROOM_NAME,
    KEY_CAPACITY_JSON,
]

def get_all_classrooms():
    return Classroom.query.all()


def get_classroom(classroom_id):
    classroom = Classroom.query.get(classroom_id)
    return classroom


def create_classroom(data):
    if data:
        classroom_id = data.get('id')
        new_classroom = Classroom(
            name=data.get('name'), capacity=data.get('capacity')
        )

        if classroom_id is not None:
            new_classroom.id = classroom_id

        db.session.add(new_classroom)
        db.session.commit()

        return new_classroom
    return None


def update_classroom(classroom, data):
    if not classroom:
        return None

    classroom.name = data.get('name', classroom.name)
    classroom.capacity = data.get('capacity', classroom.capacity)

    db.session.commit()
    return classroom


def delete_classroom(classroom):
    if not classroom:
        return False

    db.session.delete(classroom)
    db.session.commit()
    return True


def create_classroom_from_json(data):
    if not validate_json_has_required_key(data, CLASSROOM_JSON_KEY):
        return None

    classrooms = data.get('salas', [])

    # Validation cicle  (Will break if an entry it's not valid ----------------
    for classroom in classrooms:
        if not validate_entry_has_required_keys(
            classroom, KEYS_NEEDED_FOR_CLASSROOM_JSON
        ):
            return None

        if not validate_entry_can_be_loaded(
            (transform_json_entry_into_classroom_format(classroom)),
            'classroom',
        ):
            return None
        
        if get_classroom(classroom.get(KEY_ID_ENTRY)):
            flash_custom_error(f'{classroom}: {KEY_ID_ENTRY} {ALREADY_EXISTS}')

            return None

    # Creation cicle (Will only execute if ALL validations pass) --------------
    # (Thus, two for cicles are needed) ---------------------------------------
    for classroom in classrooms:
        classroom_data = transform_json_entry_into_classroom_format(classroom)
        if classroom_data:
            create_classroom(classroom_data)
        else:
            break


def transform_json_entry_into_classroom_format(classroom):
    data = {
        'id': classroom.get('id'),
        'name': classroom.get('nombre'),
        'capacity': classroom.get('capacidad'),
    }
    return data


def get_available_classrooms_for_block(block, num_students):
    timeslot_ids = [timeslot.id for timeslot in block]
    all_classrooms = get_all_classrooms()

    occupied_classroom_ids = (
        Schedule.query.filter(Schedule.time_slot_id.in_(timeslot_ids))
        .with_entities(Schedule.classroom_id)
        .distinct()
        .all()
    )

    occupied_classroom_ids = [cid for (cid,) in occupied_classroom_ids]

    available_classrooms = [
        classroom
        for classroom in all_classrooms
        if classroom.id not in occupied_classroom_ids
        and classroom.capacity >= num_students
    ]

    return available_classrooms
