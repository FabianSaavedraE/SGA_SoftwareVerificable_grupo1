from app import db
from app.models import StudentCourses
from app.validators.data_load_validators import (
    validate_entry_can_be_loaded,
    validate_entry_has_required_keys,
    validate_json_has_required_key,
)

APPROVED = "Aprobado"
FAILED = "Reprobado"
APPROVED_GRADE = 4
STUDENT_COURSES_JSON_KEY = "alumnos_seccion"
KEYS_NEEDED_FOR_STUDENT_COURSE_JSON = ["seccion_id", "alumno_id"]


def get_student_course(student_id, course_section_id):
    """Return student course by student and section IDs."""
    student_course = StudentCourses.query.get((student_id, course_section_id))
    return student_course


def create_student_course(data):
    """Create and save a new student course entry."""
    new_student_course = StudentCourses(
        student_id=data.get("student_id"),
        course_section_id=data.get("course_section_id"),
        state=data.get("state"),
    )
    db.session.add(new_student_course)
    db.session.commit()

    return new_student_course


def apply_final_grade(student_course, final_grade):
    """Apply final grade and update course state."""
    if not student_course:
        return None

    student_course.final_grade = final_grade
    update_state(student_course, final_grade)

    db.session.commit()
    return student_course


def update_state(student_course, final_grade):
    """Set course state based on final grade."""
    if not student_course:
        return None

    student_course.state = (
        APPROVED if final_grade >= APPROVED_GRADE else FAILED
    )
    return student_course


def update_student_course(student_course, data):
    """Update state and final grade of a student course."""
    if not student_course:
        return None

    student_course.state = data.get("state", student_course.state)

    final_grade = data.get("final_grade")
    if final_grade == "":
        student_course.final_grade = None
    elif final_grade is not None:
        try:
            student_course.final_grade = float(final_grade)
        except ValueError:
            pass

    db.session.commit()
    return student_course


def delete_student_course(student_id, course_section_id):
    """Delete student course by student and section IDs."""
    student_course = get_student_course(student_id, course_section_id)
    if student_course:
        db.session.delete(student_course)
        db.session.commit()
        return True
    return False


def create_student_courses_from_json(data):
    """Create student courses after validating JSON data."""
    if not validate_json_has_required_key(data, STUDENT_COURSES_JSON_KEY):
        return None

    student_courses = data.get(STUDENT_COURSES_JSON_KEY, [])

    for student_course in student_courses:
        if not validate_entry_has_required_keys(
            student_course, KEYS_NEEDED_FOR_STUDENT_COURSE_JSON
        ):
            return None

        if not validate_entry_can_be_loaded(
            transform_json_entry_into_processable_student_course_format(
                student_course
            ),
            "student_course",
        ):
            return None

    create_all_student_course_entries(student_courses)


def create_all_student_course_entries(student_courses):
    """Create all student course entries from data."""
    for entry in student_courses:
        transformed_data = (
            transform_json_entry_into_processable_student_course_format(entry)
        )

        if transformed_data:
            create_student_course(transformed_data)
        else:
            break


def transform_json_entry_into_processable_student_course_format(
    student_course,
):
    """Transform JSON entry to a dict for student course creation."""
    data = {
        "student_id": student_course.get("alumno_id"),
        "course_section_id": student_course.get("seccion_id"),
        "state": "Inscrito",
    }
    return data
