from app.models import Classroom
from app.validators.constants import (
    ALREADY_EXISTS,
    CHARACTERS,
    KEY_CAPACITY_ENTRY,
    KEY_ID_ENTRY,
    KEY_NAME_ENTRY,
    MAX_CAPACITY,
    MAX_NAME_LENGTH,
    MIN_CAPACITY,
    MUST_BE,
    MUST_BE_INT,
    MUST_BE_STRING,
    MUST_BE_STRING_OR_INT,
    OVERFLOWS,
)


def validate_classroom_data_and_return_errors(data, classroom_id=None):
    """Validate classroom data and returns typing or attribute errors."""
    typing_errors = return_classroom_typing_errors(data)

    if typing_errors:
        return typing_errors

    attribute_errors = return_classroom_attribute_errors(data, classroom_id)

    return attribute_errors


def return_classroom_typing_errors(data):
    """Return typing errors for classroom fields."""
    errors = {}
    name = data.get(KEY_NAME_ENTRY) or ""
    capacity = data.get(KEY_CAPACITY_ENTRY) or ""
    classroom_id = data.get(KEY_ID_ENTRY) or ""

    if not (isinstance(classroom_id, int) or (classroom_id == "")):
        errors[KEY_ID_ENTRY] = f"{KEY_ID_ENTRY} {MUST_BE_INT}"

    if not isinstance(name, str):
        errors[KEY_NAME_ENTRY] = f"{KEY_NAME_ENTRY} {MUST_BE_STRING}"

    if not (isinstance(capacity, str) or isinstance(capacity, int)):
        errors[KEY_CAPACITY_ENTRY] = (
            f"{KEY_CAPACITY_ENTRY} {MUST_BE_STRING_OR_INT}"
        )

    return errors


def return_classroom_attribute_errors(data, classroom_id):
    """Return attribute errors for classroom fields."""
    name = (data.get(KEY_NAME_ENTRY) or "").strip()
    capacity = data.get(KEY_CAPACITY_ENTRY) or ""
    if isinstance(capacity, str):
        capacity = capacity.strip()

    name_errors = return_classroom_name_errors(name, classroom_id)
    capacity_errors = return_classroom_capacity_errors(capacity)

    errors = {}
    errors.update(name_errors)
    errors.update(capacity_errors)
    return errors


def return_classroom_name_errors(name, classroom_id):
    """Return errors for classroom name field."""
    errors = {}
    if not name:
        errors[KEY_NAME_ENTRY] = f"{KEY_NAME_ENTRY} {MUST_BE}"
    elif len(name) > MAX_NAME_LENGTH:
        errors[KEY_NAME_ENTRY] = (
            f"{KEY_NAME_ENTRY} {OVERFLOWS} 1 - {MAX_NAME_LENGTH} {CHARACTERS}"
        )
    else:
        existing_classroom = Classroom.query.filter_by(name=name).first()

        if existing_classroom and (
            classroom_id is None or existing_classroom.id != classroom_id
        ):
            errors[KEY_NAME_ENTRY] = f"{KEY_NAME_ENTRY} {ALREADY_EXISTS}"

    return errors


def return_classroom_capacity_errors(capacity):
    """Return errors for classroom capacity field."""
    errors = {}
    if not capacity:
        errors[KEY_CAPACITY_ENTRY] = f"{KEY_CAPACITY_ENTRY} {MUST_BE}"
    else:
        try:
            capacity = int(capacity)
            if capacity < MIN_CAPACITY or capacity > MAX_CAPACITY:
                errors[KEY_CAPACITY_ENTRY] = (
                    f"{KEY_CAPACITY_ENTRY} {OVERFLOWS} "
                    f"{MIN_CAPACITY} - {MAX_CAPACITY}."
                )
        except ValueError:
            errors[KEY_CAPACITY_ENTRY] = (
                f"{KEY_CAPACITY_ENTRY} {MUST_BE_STRING_OR_INT}"
            )
    return errors
