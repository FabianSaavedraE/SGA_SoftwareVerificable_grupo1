from app import db
from app.models import CourseSection, Student, StudentCourses
from app.validators.constants import (
    ALREADY_EXISTS,
    DOESNT_EXIST,
    KEY_PREREQUISITE,
    KEY_SECTION_ENTRY,
    KEY_SECTION_ID_ENTRY,
    KEY_SECTION_ID_JSON,
    KEY_STATE_ENTRY,
    KEY_STUDENT_ENTRY,
    KEY_STUDENT_ID_ENTRY,
    KEY_STUDENT_ID_JSON,
    MUST_BE_INT,
    NOT_COMPLETED_PREREQUISITES,
)


def validate_student_course_and_return_errors(data, student_course_id=None):
    """Validate student course data and returns any errors."""
    errors = {}

    typing_errors = validate_typing(data)
    if typing_errors:
        return typing_errors

    attribute_errors = validate_attributes(data)
    errors.update(attribute_errors)

    if not attribute_errors:
        uniqueness_errors = validate_uniqueness(data, student_course_id)
        errors.update(uniqueness_errors)

    _, prerequisite_errors = check_prerequisites(data)
    errors.update(prerequisite_errors)

    return errors


def validate_typing(data):
    """Validate the data types for student and section IDs."""
    errors = {}

    student_id, section_id = get_student_and_section_ids(data)

    student_id = parse_int(student_id)
    if student_id is None:
        errors[KEY_STUDENT_ENTRY] = f"{KEY_STUDENT_ENTRY} {MUST_BE_INT}"

    section_id = parse_int(section_id)
    if section_id is None:
        errors[KEY_SECTION_ENTRY] = f"{KEY_SECTION_ENTRY} {MUST_BE_INT}"

    return errors


def validate_attributes(data):
    """Validate the existence of student and section attributes."""
    errors = {}

    student_id, section_id = get_student_and_section_ids(data)
    student = get_student(student_id)
    section = get_section(section_id)

    if not student:
        errors[KEY_STUDENT_ENTRY] = (
            f"{KEY_STUDENT_ENTRY} {student_id} {DOESNT_EXIST}"
        )

    if not section:
        errors[KEY_SECTION_ENTRY] = (
            f"{KEY_SECTION_ENTRY} {section_id} {DOESNT_EXIST}"
        )

    return errors


def validate_uniqueness(data, student_course_id=None):
    """Check for uniqueness of a student's course enrollment."""
    errors = {}

    student_id, section_id = get_student_and_section_ids(data)
    existing = StudentCourses.query.filter_by(
        student_id=student_id, course_section_id=section_id
    ).first()

    if existing and (
        not student_course_id or existing.id != student_course_id
    ):
        student = get_student(student_id)
        section = get_section(section_id)
        if student and section:
            errors[KEY_STATE_ENTRY] = (
                f"{student.first_name} {student.last_name} {ALREADY_EXISTS} de"
                f" {section.course_instance.course.name} - {section.nrc}"
            )

    return errors


def check_prerequisites(data):
    """Verify if a student meets course prerequisites."""
    student_id, section_id = get_student_and_section_ids(data)
    section = get_section(section_id)

    if not section:
        return False, {}

    course = section.course_instance.course
    prerequisites = course.prerequisites

    for prerequisite in prerequisites:
        if not has_approved_course(student_id, prerequisite.prerequisite.id):
            return False, {KEY_PREREQUISITE: NOT_COMPLETED_PREREQUISITES}

    return True, {}


def has_approved_course(student_id, course_id):
    """Check if a student has approved a specific course."""
    return (
        db.session.query(StudentCourses)
        .join(CourseSection)
        .filter(
            StudentCourses.student_id == student_id,
            StudentCourses.state == "Aprobado",
            CourseSection.course_instance.has(course_id=course_id),
        )
        .first()
        is not None
    )


def get_student_and_section_ids(data):
    """Extract student and section IDs from input data."""
    student_id = data.get(KEY_STUDENT_ID_JSON) or data.get(
        KEY_STUDENT_ID_ENTRY
    )
    section_id = data.get(KEY_SECTION_ID_JSON) or data.get(
        KEY_SECTION_ID_ENTRY
    )
    return student_id, section_id


def parse_int(value):
    """Safely converts a value to an integer."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def get_section(section_id):
    """Retrieve a CourseSection by its ID."""
    return CourseSection.query.get(section_id)


def get_student(student_id):
    """Retrieve a Student by their ID."""
    return Student.query.get(student_id)
