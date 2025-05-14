from app import db
from app.models import Classroom, Schedule

def get_all_classrooms():
    return Classroom.query.all()

def get_classroom(classroom_id):
    classroom = Classroom.query.get(classroom_id)
    return classroom

def create_classroom(data):
    classroom_id = data.get('id')
    new_classroom = Classroom(
        name = data.get('name'),
        capacity = data.get('capacity')

    )

    if classroom_id is not None:
        new_classroom.id = classroom_id
        
    db.session.add(new_classroom)
    db.session.commit()

    return new_classroom

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
    classrooms = data.get('salas', [])
    for classroom in classrooms:
        classroom_data = transform_json_entry_into_classroom_format(classroom)
        create_classroom(classroom_data)

def transform_json_entry_into_classroom_format(classroom):
    data = {
        'id' : classroom.get('id'),
        'name' : classroom.get('nombre'),
        'capacity' : classroom.get('capacidad')
    }
    return data

def get_available_classrooms_for_block(block, num_students):
    timeslot_ids = [timeslot.id for timeslot in block]
    all_classrooms = get_all_classrooms()

    occupied_classroom_ids = (
        Schedule.query
        .filter(Schedule.time_slot_id.in_(timeslot_ids))
        .with_entities(Schedule.classroom_id)
        .distinct()
        .all()
    )

    occupied_classroom_ids = [cid for (cid,) in occupied_classroom_ids]

    available_classrooms = [
        classroom for classroom in all_classrooms
        if classroom.id not in occupied_classroom_ids
        and classroom.capacity >= num_students
    ]

    return available_classrooms
