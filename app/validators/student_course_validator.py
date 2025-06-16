from app import db
from app.models import CourseSection, StudentCourses


def has_met_prerequisites(student_id, course_section):
    course = course_section.course_instance.course
    prerequisites = course.prerequisites
    error_message = 'El estudiante no ha aprobado todos los requisitos.'

    for prerequisite in prerequisites:
        if not has_approved_course(student_id, prerequisite.prerequisite.id):
            return False, error_message

    return True, None


def has_approved_course(student_id, course_id):
    approved = (
        db.session.query(StudentCourses)
        .join(CourseSection)
        .filter(
            StudentCourses.student_id == student_id,
            StudentCourses.state == 'Aprobado',
            CourseSection.course_instance.has(course_id=course_id),
        )
        .first()
    )

    return approved is not None
