from app.models.teacher import Teacher
from app import db

def getAllTeachers():
    teachers = Teacher.query.all()
    return teachers

def getTeacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    return teacher

def createTeacher(data):
    new_teacher = Teacher(
        first_name = data.get('first_name'),
        last_name = data.get('last_name'),
        email = data.get('email')
    )
    db.session.add(new_teacher)
    db.session.commit()

    return new_teacher

def updateTeacher(teacher, data):
    if not teacher:
        return None

    teacher.first_name = data.get('first_name', teacher.first_name)
    teacher.last_name = data.get('last_name', teacher.last_name)
    teacher.email = data.get('email', teacher.email)

    db.session.commit()
    return teacher

def deleteTeacher(teacher):
    if not teacher:
        return False

    db.session.delete(teacher)
    db.session.commit()
    return True
    