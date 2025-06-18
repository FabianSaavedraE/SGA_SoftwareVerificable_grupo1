from app import db
from app.models import CourseInstance
from app.validators.constants import *
from app.validators.data_load_validators import (
    flash_custom_error,
    validate_entry_can_be_loaded,
    validate_entry_has_required_keys,
)

KEYS_NEEDED_FOR_INSTANCE_JSON = [
    KEY_INSTANCE_JSON,
    KEY_SEMESTER_JSON,
    KEY_YEAR_JSON,
]
KEYS_NEEDED_FOR_INSTANCE_ENTRY = [KEY_COURSE_ID_JSON, KEY_ID_ENTRY]


def get_all_course_instances():
    """Return all course instances."""
    course_instances = CourseInstance.query.all()
    return course_instances


def get_course_instance(course_instance_id):
    """Return a course instance by its ID."""
    course_instance = CourseInstance.query.get(course_instance_id)
    return course_instance


def get_course_instance_by_parameters(year, semester):
    """Return all course instances for a given year and semester."""
    course_instances = CourseInstance.query.filter_by(
        year=year, semester=semester
    ).all()

    return course_instances


def create_course_instance(data):
    """Create a new course instance with the given data."""
    instance_id = data.get("instance_id")
    new_course_instance = CourseInstance(
        year=data.get("year"),
        semester=data.get("semester"),
        course_id=data.get("course_id"),
    )
    db.session.add(new_course_instance)
    db.session.commit()

    if instance_id is not None:
        new_course_instance.id = instance_id

    return new_course_instance


def update_course_instance(course_instance, data):
    """Update an existing course instance with new data."""
    if not course_instance:
        return None

    course_instance.year = data.get("year", course_instance.year)
    course_instance.semester = data.get("semester", course_instance.semester)

    db.session.commit()
    return course_instance


def delete_course_instance(course_instance):
    """Delete a course instance from the database."""
    if not course_instance:
        return False

    db.session.delete(course_instance)
    db.session.commit()
    return True


def create_course_instances_from_json(data):
    """Validate and create course instances from JSON data."""
    # Due to a circular import and the fact that the JSON has 3 main keys,
    # the general purpose function can't be called, so the individual one
    # has to be called 3 times.

    if not validate_entry_has_required_keys(
        data, KEYS_NEEDED_FOR_INSTANCE_JSON
    ):
        return None

    year = data.get(KEY_YEAR_JSON)
    semester = data.get(KEY_SEMESTER_JSON)
    instances = data.get(KEY_INSTANCE_JSON, [])

    # Validate each instance entry
    for instance in instances:
        if not validate_entry_has_required_keys(
            instance, KEYS_NEEDED_FOR_INSTANCE_ENTRY
        ):
            return None

        is_instance_valid = validate_entry_can_be_loaded(
            transform_json_entry_into_processable_course_instance_format(
                year, semester, instance
            ),
            "instance",
        )

        if get_course_instance(instance.get(KEY_ID_ENTRY)):
            flash_custom_error(f"{instance}: {KEY_ID_ENTRY} {ALREADY_EXISTS}")

            return None

        if not is_instance_valid:
            return None

    # Create entry after validations pass
    for instance in instances:
        instance_data = (
            transform_json_entry_into_processable_course_instance_format(
                year, semester, instance
            )
        )

        create_course_instance(instance_data)


def transform_json_entry_into_processable_course_instance_format(
    year, semester, instance
):
    """Convert JSON entry into internal course instance data format."""
    data = {
        "year": year,
        "semester": semester,
        "instance_id": instance.get("id"),
        "course_id": instance.get("curso_id"),
    }
    return data
