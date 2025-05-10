from app.models import Classroom, Schedule
from app import db

def get_all_classrooms():
    return Classroom.query.all()

def get_classroom(classroom_id):
    classroom = Classroom.query.get(classroom_id)
    return classroom

def create_classroom(data):
    new_classroom = Classroom(
        name = data.get('name'),
        capacity = data.get('capacity')

    )

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

def get_available_classrooms_for_block(block, num_students):
    print("\nBLOCK IN CLASSROOM FUNCTION:", block)

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

    # Esto es puro para debugging, se borra y se ocupa el código comentado de 
    # abajo cuando este todo listo.
    available_classrooms = []
    for classroom in all_classrooms:
        if classroom.id in occupied_classroom_ids:
            print(f"Sala ocupada: {classroom.name} (ID {classroom.id})")
            continue

        if classroom.capacity < num_students:
            print(f"Sala sin capacidad suficiente: {classroom.name} (ID {classroom.id})")
            continue

        print(f"Sala disponible: {classroom.name} (ID {classroom.id})")
        available_classrooms.append(classroom)




    # available_classrooms = [
    #     classroom for classroom in all_classrooms
    #     if classroom.id not in occupied_classroom_ids
    #     and classroom.capacity >= num_students
    # ]

    return available_classrooms