from app.models.student_course import StudentCourses
from app import db

def createStudentCourse(data):
    new_student_course = StudentCourses(
        student_id = data.get('student_id'),
        course_section_id = data.get('course_section_id'),
        state = data.get('state')
    )
    db.session.add(new_student_course)
    db.session.commit()

    return new_student_course
