from datetime import date

from app import db
from app.models import Student, StudentCourses, CourseSection, Schedule

def get_all_students():
    students = Student.query.all()
    return students

def get_student(student_id):
    student = Student.query.get(student_id)
    return student

def create_student(data):
    entry_year = data.get('entry_year')

    if entry_year:
        try:
            entry_year = int(entry_year)
        except ValueError:
            entry_year = date.today().year
    else:
        entry_year = date.today().year
        
    entry_year = max(1900, min(date.today().year, entry_year))

    new_student = Student(
        first_name = data.get('first_name'),
        last_name = data.get('last_name'),
        email = data.get('email'),
        entry_year=entry_year
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

    entry_year = data.get('entry_year')
    if entry_year:
        try:
            student.entry_year = max(1900, min(date.today().year, int(entry_year)))
        except ValueError:
            pass

    db.session.commit()
    return student

def delete_student(student):
    if not student:
        return False

    db.session.delete(student)
    db.session.commit()
    return True

def create_students_from_json(data):
    students = data.get('alumnos', [])
    for student in students:
        name = student.get('nombre', '')
        name_parts = name.strip().split()
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        
        entry_year = int(student.get('anio_ingreso'))

        new_student = Student(
            first_name=first_name,
            last_name=last_name,
            email=student.get('correo'),
            entry_year=entry_year
        )
        db.session.add(new_student)

    db.session.commit()
    
def are_students_available_for_timeslot(section, block):
    timeslot_ids = [timeslot.id for timeslot in block]

    students = section['section'].students

    if not students:
        return True
    
    student_ids = [student.id for student in students]
    
    conflicting_schedules = (
        Schedule.query
        .join(CourseSection)
        .join(CourseSection.student_courses)
        .filter(
            Schedule.time_slot_id.in_(timeslot_ids),
            StudentCourses.student_id.in_(student_ids),
            CourseSection.id != section['section'].id
        )
        .all()
    )

    return len(conflicting_schedules) == 0

def create_students_from_json(data):
    students = data.get('alumnos', [])
    for student in students:
        name = student.get('nombre', '')
        name_parts = name.strip().split()
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        
        entry_year = int(student.get('anio_ingreso'))

        new_student = Student(
            first_name=first_name,
            last_name=last_name,
            email=student.get('correo'),
            entry_year=entry_year
        )
        db.session.add(new_student)

    db.session.commit()