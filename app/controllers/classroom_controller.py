from app.models import Classroom
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
