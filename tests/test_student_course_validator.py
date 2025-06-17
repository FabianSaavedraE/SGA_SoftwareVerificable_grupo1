from unittest.mock import patch

from app.validators import student_course_validator as validator
from app.validators.constants import (
    DOESNT_EXIST,
    KEY_SECTION_ENTRY,
    KEY_SECTION_ID_JSON,
    KEY_STUDENT_ENTRY,
    KEY_STUDENT_ID_JSON,
    MUST_BE_INT,
)


def make_base_data(student_id="1", section_id="1"):
    return {
        KEY_STUDENT_ID_JSON: student_id,
        KEY_SECTION_ID_JSON: section_id,
    }


def test_typing_errors_returned():
    data = make_base_data(student_id="abc", section_id=None)
    errors = validator.validate_student_course_and_return_errors(data)

    assert KEY_STUDENT_ENTRY in errors
    assert KEY_SECTION_ENTRY in errors
    assert MUST_BE_INT in errors[KEY_STUDENT_ENTRY]


@patch(
    "app.validators.student_course_validator.get_student", return_value=None
)
@patch(
    "app.validators.student_course_validator.get_section", return_value=None
)
def test_attribute_errors_for_nonexistent_records(mock_section, mock_student):
    data = make_base_data()
    errors = validator.validate_student_course_and_return_errors(data)

    assert KEY_STUDENT_ENTRY in errors
    assert KEY_SECTION_ENTRY in errors
    assert DOESNT_EXIST in errors[KEY_STUDENT_ENTRY]
