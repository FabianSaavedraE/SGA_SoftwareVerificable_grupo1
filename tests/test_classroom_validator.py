from unittest.mock import MagicMock, patch

import pytest

from app.validators import classroom_validator as validator
from app.validators.constants import (
    KEY_CAPACITY_ENTRY,
    KEY_NAME_ENTRY,
    MUST_BE_STRING,
    MUST_BE_STRING_OR_INT,
)


@pytest.fixture(autouse=True)
def patch_classroom_query():
    """Mock the Classroom model's query for all tests."""
    with patch(
        "app.validators.classroom_validator.Classroom"
    ) as mock_classroom:
        mock_classroom.query.filter_by.return_value.first.return_value = None
        yield mock_classroom


def test_typing_error_invalid_id_type():
    """Tests error when ID is not an integer."""
    data = {KEY_NAME_ENTRY: "Reloj 101", KEY_CAPACITY_ENTRY: "10", "id": "abc"}
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert "id" in errors


def test_typing_error_invalid_name_type():
    """Tests error when name is not a string."""
    data = {KEY_NAME_ENTRY: 123, KEY_CAPACITY_ENTRY: "10"}
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert KEY_NAME_ENTRY in errors
    assert MUST_BE_STRING in errors[KEY_NAME_ENTRY]


def test_typing_error_invalid_capacity_type():
    """Tests error when capacity is neither string nor int."""
    data = {KEY_NAME_ENTRY: "Reloj 101", KEY_CAPACITY_ENTRY: {"value": 10}}
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert KEY_CAPACITY_ENTRY in errors
    assert MUST_BE_STRING_OR_INT in errors[KEY_CAPACITY_ENTRY]


def test_name_exists_same_id(patch_classroom_query):
    """Tests no error when classroom name exists with same ID."""
    existing = MagicMock()
    existing.id = 1
    patch_classroom_query.query.filter_by.return_value.first.return_value = (
        existing
    )

    data = {KEY_NAME_ENTRY: "Reloj 101", KEY_CAPACITY_ENTRY: "10"}
    errors = validator.validate_classroom_data_and_return_errors(
        data, classroom_id=1
    )

    assert KEY_NAME_ENTRY not in errors
