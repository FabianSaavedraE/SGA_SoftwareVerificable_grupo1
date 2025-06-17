from unittest.mock import MagicMock, patch

import pytest

from app.validators import course_validator as validator
from app.validators.constants import (
    ALREADY_EXISTS,
    KEY_CODE_ENTRY,
    KEY_CREDITS_ENTRY,
    KEY_DESCRIPTION_ENTRY,
    KEY_NAME_ENTRY,
)


@patch("app.validators.course_validator.Course")
def test_validate_course_data_duplicate_code(mock_course_model):
    existing_course = MagicMock(id=2)
    mock_course_model.query.filter_by.return_value.first.return_value = (
        existing_course
    )

    valid_data = {
        KEY_NAME_ENTRY: "Diseño de Software Verificable",
        KEY_DESCRIPTION_ENTRY: "Descripción Verificables",
        KEY_CODE_ENTRY: "1234",
        KEY_CREDITS_ENTRY: "3",
    }

    errors = validator.validate_course_data_and_return_errors(
        valid_data, course_id=1
    )

    assert KEY_CODE_ENTRY in errors
    assert ALREADY_EXISTS in errors[KEY_CODE_ENTRY]


@patch("app.validators.course_validator.Course")
def test_validate_course_data_valid_input(mock_course_model):
    mock_course_model.query.filter_by.return_value.first.return_value = None

    valid_data = {
        KEY_NAME_ENTRY: "Diseño de Software Verificable",
        KEY_DESCRIPTION_ENTRY: "Descripción Verificables",
        KEY_CODE_ENTRY: "1234",
        KEY_CREDITS_ENTRY: "3",
    }

    errors = validator.validate_course_data_and_return_errors(valid_data)

    assert errors == {}


@pytest.mark.parametrize(
    "field, value, max_length",
    [
        (KEY_NAME_ENTRY, "", 100),
        (KEY_DESCRIPTION_ENTRY, "x" * 101, 100),
    ],
)
def test_return_text_field_errors(field, value, max_length):
    result = validator.return_text_field_errors(field, value)
    assert field in result


@pytest.mark.parametrize(
    "input_credits",
    ["abc", "0", "5"],
)
def test_return_credits_errors_invalid(input_credits):
    result = validator.return_credits_errors(input_credits)
    assert KEY_CREDITS_ENTRY in result


@patch("app.validators.course_validator.Course")
def test_validate_and_return_prerequisite_if_course_exists(mock_course_model):
    course = MagicMock()
    mock_course_model.query.filter_by.return_value.first.return_value = course

    result = validator.validate_and_return_prerequisite_if_course_exists(
        "1234"
    )
    assert result == course


@patch("app.validators.course_validator.Course")
def test_validate_and_return_prerequisite_if_course_does_not_exist(
    mock_course_model,
):
    mock_course_model.query.filter_by.return_value.first.return_value = None

    result = validator.validate_and_return_prerequisite_if_course_exists(
        "9999"
    )
    assert result is False
