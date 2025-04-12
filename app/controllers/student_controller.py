from app.models.student import Student
from app import db

def getAllStudents():
    students = Student.query.all()
    return students

def getStudent(student_id):
    student = Student.query.get(student_id)
    print(student)
    return student

def createStudent(data):
    new_student = Student(
        first_name = data.get('first_name'),
        last_name = data.get('last_name'),
        email = data.get('email')
    )
    db.session.add(new_student)
    db.session.commit()

    return new_student

def updateStudent(student, data):
    if not student:
        return None

    student.first_name = data.get('first_name', student.first_name)
    student.last_name = data.get('last_name', student.last_name)
    student.email = data.get('email', student.email)

    db.session.commit()
    return student

def deleteStudent(student):
    print(student)
    if not student:
        return False

    db.session.delete(student)
    db.session.commit()
    return True
    