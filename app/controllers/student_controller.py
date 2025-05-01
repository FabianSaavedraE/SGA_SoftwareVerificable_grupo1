from app.models.student import Student
from app import db
from datetime import datetime, date

def get_all_students():
    students = Student.query.all()
    return students

def get_student(student_id):
    student = Student.query.get(student_id)
    print(student)
    return student

def create_student(data):
    entry_date = data.get('entry_date')
    
    if entry_date:
        try:
            entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
        except ValueError:
            entry_date = date.today()
    else:
        entry_date = date.today()
    
    new_student = Student(
        first_name = data.get('first_name'),
        last_name = data.get('last_name'),
        email = data.get('email'),
        entry_date=entry_date
    )
    db.session.add(new_student)
    db.session.commit()

    return new_student

def update_student(student, data):
    if not student:
        return None

    student.first_name = data.get('first_name', student.first_name)
    student.last_name = data.get('last_name', student.last_name)
    student.email = data.get('email', student.email)
    
    entry_date = data.get('entry_date')
    if entry_date:
        try:
            student.entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
        except ValueError:
            pass

    db.session.commit()
    return student

def delete_student(student):
    print(student)
    if not student:
        return False

    db.session.delete(student)
    db.session.commit()
    return True
    