from app import db
from app.models import StudentCourses

APPROVED = "Aprobado"
FAILED = "Reprobado"
APPROVED_GRADE = 4

def get_student_course(student_id, course_section_id):
    student_course = StudentCourses.query.get((student_id, course_section_id))
    return student_course

def create_student_course(data):
    new_student_course = StudentCourses(
        student_id = data.get('student_id'),
        course_section_id = data.get('course_section_id'),
        state = data.get('state')
    )
    db.session.add(new_student_course)
    db.session.commit()

    return new_student_course

def apply_final_grade(student_course, final_grade):
    if not student_course:
        return None
    
    student_course.final_grade = final_grade
    update_state(student_course, final_grade)

    db.session.commit()
    return student_course

def update_state(student_course, final_grade):
    if not student_course:
        return None

    student_course.state = (
        APPROVED if final_grade >= APPROVED_GRADE else FAILED
    )
    return student_course

def update_student_course(student_course, data):
    if not student_course:
        return None

    student_course.state = data.get('state', student_course.state)

    final_grade = data.get('final_grade')
    if final_grade == '':
        student_course.final_grade = None
    elif final_grade is not None:
        try:
            student_course.final_grade = float(final_grade)
        except ValueError:
            pass

    db.session.commit()
    return student_course

def delete_student_course(student_id, course_section_id):
    student_course = get_student_course(student_id, course_section_id)
    if student_course:
        db.session.delete(student_course)
        db.session.commit()
        return True
    return False

def create_student_courses_from_json(data):
    student_courses = data.get('alumnos_seccion', [])
    for student_course in student_courses:
        student_course_data = (
            transform_json_entry_into_processable_student_course_format(
                student_course
        ))
        create_student_course(student_course_data)
    
def transform_json_entry_into_processable_student_course_format(student_course):
    data = {
        'student_id' : student_course.get('alumno_id'),
        'course_section_id' : student_course.get('seccion_id'),
        'state' : 'Inscrito'
    }
    return(data)
