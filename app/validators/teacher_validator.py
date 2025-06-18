from app.models import Teacher
from app.validators.constants import (
    ALREADY_EXISTS,
    CHARACTERS,
    KEY_EMAIL_ENTRY,
    KEY_FIRST_NAME_ENTRY,
    KEY_ID_ENTRY,
    KEY_LAST_NAME_ENTRY,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_USERS_NAME,
    MUST_BE,
    MUST_BE_INT,
    MUST_BE_STRING,
    MUST_CONTAIN,
    OVERFLOWS,
)


def validate_teacher_data_and_return_errors(data, teacher_id=None):
    """Validate teacher data and returns any found errors."""
    typing_errors = return_teacher_typing_errors(data)

    if typing_errors:
        return typing_errors

    attribute_errors = return_teacher_attribute_errors(data, teacher_id)
    return attribute_errors


def return_teacher_typing_errors(data):
    """Return typing errors found in teacher data."""
    errors = {}
    first_name = data.get(KEY_FIRST_NAME_ENTRY, "")
    last_name = data.get(KEY_LAST_NAME_ENTRY, "")
    email = data.get(KEY_EMAIL_ENTRY, "")
    id = data.get(KEY_ID_ENTRY, "")

    if not isinstance(first_name, str):
        errors[KEY_FIRST_NAME_ENTRY] = (
            f"{KEY_FIRST_NAME_ENTRY} {MUST_BE_STRING}"
        )

    if not isinstance(last_name, str):
        errors[KEY_LAST_NAME_ENTRY] = f"{KEY_LAST_NAME_ENTRY} {MUST_BE_STRING}"

    if not isinstance(email, str):
        errors[KEY_EMAIL_ENTRY] = f"{KEY_EMAIL_ENTRY} {MUST_BE_STRING}"

    if not (isinstance(id, int) or (id == "")):
        errors[KEY_ID_ENTRY] = f"{KEY_ID_ENTRY} {MUST_BE_INT}"

    return errors


def return_teacher_attribute_errors(data, teacher_id):
    """Return attribute errors in teacher data."""
    errors = {}

    first_name = data.get(KEY_FIRST_NAME_ENTRY, "").strip()
    last_name = data.get(KEY_LAST_NAME_ENTRY, "").strip()
    email = data.get(KEY_EMAIL_ENTRY, "").strip()

    first_name_errors = return_teacher_name_errors(
        KEY_FIRST_NAME_ENTRY, first_name
    )

    last_name_errors = return_teacher_name_errors(
        KEY_LAST_NAME_ENTRY, last_name
    )

    email_errors = return_teacher_email_errors(email, teacher_id)

    errors.update(first_name_errors)
    errors.update(last_name_errors)
    errors.update(email_errors)

    return errors


def return_teacher_name_errors(key, name):
    """Validate a teacher's name and returns any errors."""
    errors = {}

    if not name or name == "" or name == "":
        errors[key] = f"{key} {MUST_BE}"

    elif len(name) > MAX_LENGTH_USERS_NAME:
        errors[key] = (
            f"{key} {OVERFLOWS} 1 - {MAX_LENGTH_USERS_NAME} {CHARACTERS}."
        )

    return errors


def return_teacher_email_errors(email, teacher_id):
    """Validate teacher email and returns related errors."""
    errors = {}

    if not email:
        errors[KEY_EMAIL_ENTRY] = f"{KEY_EMAIL_ENTRY} {MUST_BE}"

    elif len(email) > MAX_LENGTH_EMAIL:
        errors[KEY_EMAIL_ENTRY] = (
            f"{KEY_EMAIL_ENTRY} {OVERFLOWS}"
            f" 1 - {MAX_LENGTH_EMAIL} {CHARACTERS}"
        )

    elif "@" not in email:
        errors[KEY_EMAIL_ENTRY] = f"{KEY_EMAIL_ENTRY} {MUST_CONTAIN} @"

    else:
        existing_teacher = Teacher.query.filter_by(email=email).first()
        if existing_teacher and (
            teacher_id is None or existing_teacher.id != teacher_id
        ):
            errors[KEY_EMAIL_ENTRY] = f"{KEY_EMAIL_ENTRY} {ALREADY_EXISTS}"

    return errors
