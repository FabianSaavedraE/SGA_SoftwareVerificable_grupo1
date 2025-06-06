from app import db
from app.models import Student, Schedule, CourseSection, StudentCourses
from app.validators.student_validator import normalize_entry_year

def get_all_students():
    students = Student.query.all()
    return students

def get_student(student_id):
    student = Student.query.get(student_id)
    return student

def create_student(data):
    entry_year = normalize_entry_year(data.get('entry_year'))

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
    student.entry_year = normalize_entry_year(
        data.get('entry_year', student.entry_year)
    )

    db.session.commit()
    return student

def delete_student(student):
    if not student:
        return False

    db.session.delete(student)
    db.session.commit()
    return True
    
def are_students_available_for_timeslot(section, block):
    timeslot_ids = [timeslot.id for timeslot in block]
    students = section['section'].students

    if not students:
        return True
    
    student_ids = [student.id for student in students]
    current_section_id = section['section'].id
    
    conflicts = get_conflicting_schedules(
        timeslot_ids, student_ids, current_section_id
    )

    return len(conflicts) == 0

def get_conflicting_schedules(timeslots_id, students_id, current_section_id):
    return (
        Schedule.query
        .join(CourseSection)
        .join(CourseSection.student_courses)
        .filter(
            Schedule.time_slot_id.in_(timeslots_id),
            StudentCourses.student_id.in_(students_id),
            CourseSection.id != current_section_id
        )
        .all()
    )

def create_students_from_json(data):
    students = data.get('alumnos', [])
    for student in students:
        student_data = transform_json_entry_into_processable_student_format(
            student
        )
        create_student(student_data)

def transform_json_entry_into_processable_student_format(student):
    name = student.get('nombre', '')
    name_parts = name.strip().split()
    data = {
            'first_name' : name_parts[0],
            'last_name' : (
                ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            ),
            'email' : student.get('correo'),
            'entry_year' : int(student.get('anio_ingreso'))
    }
    return data
