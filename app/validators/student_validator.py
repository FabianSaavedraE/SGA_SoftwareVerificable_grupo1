from app.models import Student
from app.validators.constants import (
    ALREADY_EXISTS,
    CHARACTERS,
    KEY_EMAIL_ENTRY,
    KEY_ENTRY_YEAR,
    KEY_FIRST_NAME_ENTRY,
    KEY_ID_ENTRY,
    KEY_LAST_NAME_ENTRY,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_USERS_NAME,
    MAX_VALID_ENTRY_YEAR,
    MIN_VALID_ENTRY_YEAR,
    MUST_BE,
    MUST_BE_INT,
    MUST_BE_STRING,
    MUST_BE_STRING_OR_INT,
    MUST_CONTAIN,
    OVERFLOWS,
)


def validate_student_data_and_return_errors(data, student_id=None):
    """Validate student data and returns any found errors."""
    typing_errors = return_student_typing_errors(data)

    if typing_errors:
        return typing_errors

    attribute_errors = return_student_attribute_errors(data, student_id)
    return attribute_errors


def return_student_typing_errors(data):
    """Return typing errors found in student data."""
    errors = {}
    first_name = data.get(KEY_FIRST_NAME_ENTRY, "")
    last_name = data.get(KEY_LAST_NAME_ENTRY, "")
    email = data.get(KEY_EMAIL_ENTRY, "")
    student_id = data.get(KEY_ID_ENTRY, "")
    entry_year = data.get(KEY_ENTRY_YEAR, "")

    if not isinstance(first_name, str):
        errors[KEY_FIRST_NAME_ENTRY] = (
            f"{KEY_FIRST_NAME_ENTRY} {MUST_BE_STRING}"
        )

    if not isinstance(last_name, str):
        errors[KEY_LAST_NAME_ENTRY] = f"{KEY_LAST_NAME_ENTRY} {MUST_BE_STRING}"

    if not isinstance(email, str):
        errors[KEY_EMAIL_ENTRY] = f"{KEY_EMAIL_ENTRY} {MUST_BE_STRING}"

    if not (isinstance(student_id, int) or (student_id == "")):
        errors[KEY_ID_ENTRY] = f"{KEY_ID_ENTRY} {MUST_BE_INT}"

    if not (isinstance(entry_year, int) or isinstance(entry_year, str)):
        errors[KEY_ENTRY_YEAR] = f"{KEY_ENTRY_YEAR} {MUST_BE_STRING_OR_INT}"

    return errors


def return_student_attribute_errors(data, student_id):
    """Return attribute errors in student data."""
    errors = {}

    first_name = get_stripped_field(data, KEY_FIRST_NAME_ENTRY)
    last_name = get_stripped_field(data, KEY_LAST_NAME_ENTRY)
    email = get_stripped_field(data, KEY_EMAIL_ENTRY)
    entry_year = data.get(KEY_ENTRY_YEAR, "")

    first_name_errors = return_student_name_errors(
        KEY_FIRST_NAME_ENTRY, first_name
    )

    last_name_errors = return_student_name_errors(
        KEY_LAST_NAME_ENTRY, last_name
    )

    email_errors = return_student_email_errors(email, student_id)
    entry_year_errors = return_entry_year_errors(entry_year)
    errors.update(first_name_errors)
    errors.update(last_name_errors)
    errors.update(email_errors)
    errors.update(entry_year_errors)

    return errors


def return_student_name_errors(key, name):
    """Validate a student's name and returns any errors."""
    errors = {}

    if not name or name == "" or name == "":
        errors[key] = f"{key} {MUST_BE}"

    elif len(name) > MAX_LENGTH_USERS_NAME:
        errors[key] = (
            f"{key} {OVERFLOWS} 0 - {MAX_LENGTH_USERS_NAME} {CHARACTERS}."
        )

    return errors


def return_student_email_errors(email, student_id):
    """Validate student email and returns related errors."""
    errors = {}

    if not email:
        errors[KEY_EMAIL_ENTRY] = f"{KEY_EMAIL_ENTRY} {MUST_BE}"

    elif len(email) > MAX_LENGTH_EMAIL or len(email) <= 1:
        errors[KEY_EMAIL_ENTRY] = (
            f"{KEY_EMAIL_ENTRY} {OVERFLOWS} 1 - "
            f"{MAX_LENGTH_EMAIL} {CHARACTERS}"
        )

    elif "@" not in email:
        errors[KEY_EMAIL_ENTRY] = f"{KEY_EMAIL_ENTRY} {MUST_CONTAIN} @"

    else:
        existing_student = Student.query.filter_by(email=email).first()
        if existing_student and (
            student_id is None or existing_student.id != student_id
        ):
            errors[KEY_EMAIL_ENTRY] = f"{KEY_EMAIL_ENTRY} {ALREADY_EXISTS}"

    return errors


def return_entry_year_errors(entry_year):
    """Validate entry year and returns any errors."""
    errors = {}

    if not entry_year:
        errors[KEY_ENTRY_YEAR] = f"{KEY_ENTRY_YEAR} {MUST_BE}"

    if isinstance(entry_year, str):
        try:
            entry_year = int(entry_year)
        except:
            errors[KEY_ENTRY_YEAR] = f"{KEY_ENTRY_YEAR} {MUST_BE_INT}"
            return errors

    if entry_year < MIN_VALID_ENTRY_YEAR or entry_year > MAX_VALID_ENTRY_YEAR:
        errors[KEY_ENTRY_YEAR] = (
            f"{KEY_ENTRY_YEAR} {OVERFLOWS}"
            f" {MIN_VALID_ENTRY_YEAR} - {MAX_VALID_ENTRY_YEAR}"
        )

    return errors


def get_stripped_field(data, field_name):
    """Return a stripped string value from given data."""
    return (str(data.get(field_name) or "")).strip()
