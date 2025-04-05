from app.models.student import Student
from app import db

def getAllStudents():
    students = Student.query.all()
    return [serializeStudent(s) for s in students]

def createStudent(data):
    new_student = Student(
        first_name = data.get('first_name'),
        last_name = data.get('last_name'),
        email = data.get('email')
    )
    db.session.add(new_student)
    db.session.commit()

    return serializeStudent(new_student)

def updateStudent(student_id, data):
    student = Student.query.get(student_id)
    if not student:
        return None

    student.first_name = data.get('first_name', student.first_name)
    student.last_name = data.get('last_name', student.last_name)
    student.email = data.get('email', student.email)

    db.session.commit()
    return serializeStudent(student)

def deleteStudent(student_id):
    student = Student.query.get(student_id)
    if not student:
        return False

    db.session.delete(student)
    db.session.commit()
    return True

def serializeStudent(student):
    return {
        "id": student.id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "email": student.email
    }