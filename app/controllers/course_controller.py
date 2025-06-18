from sqlalchemy import func

from app import db
from app.controllers.course_prerequisites_controllers import (
    create_course_prerequisite,
)
from app.controllers.course_section_controller import (
    close_all_sections_for_course,
)
from app.models import Course
from app.validators.constants import (
    CODE_LENGTH,
    COURSE_CODE_PREFIX,
    KEY_CODE_JSON,
    KEY_COURSE_JSON,
    KEY_CREDITS_JSON,
    KEY_DESCRIPTION_JSON,
    KEY_ID_ENTRY,
)
from app.validators.data_load_validators import (
    flash_custom_error,
    validate_entry_can_be_loaded,
    validate_entry_has_required_keys,
    validate_json_has_required_key,
)

KEYS_REQUIRED_JSON = [
    KEY_DESCRIPTION_JSON,
    KEY_CODE_JSON,
    KEY_ID_ENTRY,
    KEY_CREDITS_JSON,
]


def get_all_courses():
    """Return all courses."""
    courses = Course.query.all()
    return courses


def get_course(course_id):
    """Return a course by its ID."""
    course = Course.query.get(course_id)
    return course


def create_course(data):
    """Create a new course with the given data."""
    course_credits = int(data.get("credits", 0))
    code = transform_code_to_valid_format(data)
    course_id = data.get("course_id")

    new_course = Course(
        name=data.get("name"),
        description=data.get("description"),
        credits=course_credits,
        code=code,
        state=data.get("state", "Open"),
    )

    if course_id is not None:
        new_course.id = course_id

    db.session.add(new_course)
    db.session.commit()

    return new_course


def update_course(course, data):
    """Update an existing course with new data."""
    if not course:
        return None

    previous_state = course.state
    course.name = data.get("name", course.name)
    course.description = data.get("description", course.description)
    course.credits = data.get("credits", course.credits)
    course.code = format_course_code(
        data.get("code", get_raw_code_from_course(course))
    )
    course.state = data.get("state", course.state)
    db.session.commit()

    if has_course_been_closed(previous_state, course.state):
        close_all_sections_for_course(course.id)

    return course


def format_course_code(raw_code):
    """Format the raw course code with prefix and zero-padding."""
    code_str = str(raw_code or "").zfill(CODE_LENGTH)
    return f"{COURSE_CODE_PREFIX}{code_str}"


def get_raw_code_from_course(course):
    """Extract the raw numeric part from a course code."""
    return str(course.code)[len(COURSE_CODE_PREFIX) :]


def has_course_been_closed(old_state, new_state):
    """Return True if course state changed from 'Open' to 'Closed'."""
    return old_state == "Open" and new_state == "Closed"


def delete_course(course):
    """Delete a course from the database."""
    if not course:
        return False

    db.session.delete(course)
    db.session.commit()
    return True


def transform_code_to_valid_format(data):
    """Ensure course code has correct prefix and length."""
    raw_code = data.get("code", "")
    if raw_code.startswith(COURSE_CODE_PREFIX):
        return raw_code
    raw_code = raw_code.zfill(CODE_LENGTH)
    return f"{COURSE_CODE_PREFIX}{raw_code}"


def create_courses_from_json(data):
    """Create courses from JSON data after validation."""
    if not validate_json_has_required_key(data, KEY_COURSE_JSON):
        return None

    # Validate each course entry
    courses = data.get("cursos", [])
    for course in courses:
        if not validate_entry_has_required_keys(course, KEYS_REQUIRED_JSON):
            return None

        is_valid_entry = validate_entry_can_be_loaded(
            transform_json_entry_into_processable_course_format(course),
            "course",
        )

        if not is_valid_entry:
            return None

    # Create courses if all validations pass
    for course in courses:
        course_id = course.get("id")
        prerequisites = course.get("requisitos")
        course_data = transform_json_entry_into_processable_course_format(
            course
        )

        if check_if_course_with_id_exists(course_id):
            handle_course_with_existing_id(course_id)

        create_course(course_data)

        if prerequisites != []:
            generate_prerequisites(course_id, prerequisites)

    db.session.commit()


def transform_json_entry_into_processable_course_format(course):
    """Convert JSON course entry into internal course data format."""
    data = {
        "name": course.get("descripcion"),
        # Simply a duplication, not required technically,
        # but added in our model.
        "description": course.get("descripcion"),
        "code": course.get("codigo"),
        "credits": course.get("creditos"),
        "course_id": course.get("id"),
    }
    return data


def check_if_course_with_id_exists(id):
    """Return True if a course with the given ID exists."""
    course = Course.query.filter_by(id=id).first()
    if course:
        return True
    else:
        return False


def handle_course_with_existing_id(id):
    """Assign a new ID to a course if the ID already exists."""
    course = Course.query.filter_by(id=id).first()
    max_id = db.session.query(func.max(Course.id)).scalar() or 0
    new_id = max_id + 1

    course.id = new_id
    db.session.commit()


def generate_prerequisites(id, prerequisites):
    """Create course prerequisites from a list of prerequisite codes."""
    # Since the creation of prerequisites is sequential in the JSON file, there
    # is no simple way to avoid the creation of failed prerequisite JSON files
    # Since it's a mistake that can be fixed in the front_end, this solution
    # only avoids page collapsing, yet does not provide real work
    for prerequisite in prerequisites:
        course = Course.query.filter_by(code=prerequisite).first()
        if not course:
            flash_custom_error(
                f"prerequisito {prerequisite} no existe,"
                f" curso creado sin prerequisito dado."
            )
        else:
            prerequisite_id = course.id
            create_course_prerequisite(id, prerequisite_id)
