from app.models.student_course import StudentCourses
from app import db

def getStudentCourse(student_id, course_section_id):
    student_course = StudentCourses.query.get((student_id, course_section_id))
    return student_course

def createStudentCourse(data):
    new_student_course = StudentCourses(
        student_id = data.get('student_id'),
        course_section_id = data.get('course_section_id'),
        state = data.get('state')
    )
    db.session.add(new_student_course)
    db.session.commit()

    return new_student_course

def updateStudentCourse(student_course, data):
    if not student_course:
        return None

    student_course.state = data.get('state', student_course.state)

    db.session.commit()
    return student_course

def deleteStudentCourse(student_id, course_section_id):
    student_course = getStudentCourse(student_id, course_section_id)
    if student_course:
        db.session.delete(student_course)
        db.session.commit()
        return True
    return False