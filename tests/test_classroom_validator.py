from unittest.mock import MagicMock, patch

import pytest

from app.validators import classroom_validator as validator
from app.validators.constants import (
    ALREADY_EXISTS,
    KEY_CAPACITY_ENTRY,
    KEY_NAME_ENTRY,
    MAX_CAPACITY,
    MAX_NAME_LENGTH,
    MIN_CAPACITY,
    MUST_BE,
    MUST_BE_STRING,
    MUST_BE_STRING_OR_INT,
    OVERFLOWS,
)


@pytest.fixture(autouse=True)
def patch_classroom_query():
    with patch(
        "app.validators.classroom_validator.Classroom"
    ) as mock_classroom:
        mock_classroom.query.filter_by.return_value.first.return_value = None
        yield mock_classroom


def test_typing_error_invalid_id_type():
    data = {KEY_NAME_ENTRY: "Reloj 101", KEY_CAPACITY_ENTRY: "10", "id": "abc"}
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert "id" in errors


def test_typing_error_invalid_name_type():
    data = {KEY_NAME_ENTRY: 123, KEY_CAPACITY_ENTRY: "10"}
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert KEY_NAME_ENTRY in errors
    assert MUST_BE_STRING in errors[KEY_NAME_ENTRY]


def test_typing_error_invalid_capacity_type():
    data = {KEY_NAME_ENTRY: "Reloj 101", KEY_CAPACITY_ENTRY: {"value": 10}}
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert KEY_CAPACITY_ENTRY in errors
    assert MUST_BE_STRING_OR_INT in errors[KEY_CAPACITY_ENTRY]


def test_name_required():
    data = {KEY_NAME_ENTRY: "", KEY_CAPACITY_ENTRY: "10"}
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert KEY_NAME_ENTRY in errors
    assert MUST_BE in errors[KEY_NAME_ENTRY]


def test_name_too_long():
    data = {
        KEY_NAME_ENTRY: "A" * (MAX_NAME_LENGTH + 1),
        KEY_CAPACITY_ENTRY: "10",
    }
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert KEY_NAME_ENTRY in errors
    assert OVERFLOWS in errors[KEY_NAME_ENTRY]


def test_name_already_exists_other_id(patch_classroom_query):
    existing = MagicMock()
    existing.id = 2
    patch_classroom_query.query.filter_by.return_value.first.return_value = (
        existing
    )

    data = {KEY_NAME_ENTRY: "Reloj 101", KEY_CAPACITY_ENTRY: "10"}
    errors = validator.validate_classroom_data_and_return_errors(
        data, classroom_id=1
    )

    assert KEY_NAME_ENTRY in errors
    assert ALREADY_EXISTS in errors[KEY_NAME_ENTRY]


def test_name_exists_same_id(patch_classroom_query):
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


def test_capacity_required():
    data = {KEY_NAME_ENTRY: "Reloj 101", KEY_CAPACITY_ENTRY: ""}
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert KEY_CAPACITY_ENTRY in errors
    assert MUST_BE in errors[KEY_CAPACITY_ENTRY]


def test_capacity_not_integer():
    data = {KEY_NAME_ENTRY: "Reloj 101", KEY_CAPACITY_ENTRY: "abc"}
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert KEY_CAPACITY_ENTRY in errors
    assert MUST_BE_STRING_OR_INT in errors[KEY_CAPACITY_ENTRY]


def test_capacity_out_of_range_low():
    data = {KEY_NAME_ENTRY: "Reloj 101", KEY_CAPACITY_ENTRY: "0"}
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert KEY_CAPACITY_ENTRY in errors
    assert f"{MIN_CAPACITY} - {MAX_CAPACITY}" in errors[KEY_CAPACITY_ENTRY]


def test_capacity_out_of_range_high():
    data = {
        KEY_NAME_ENTRY: "Reloj 101",
        KEY_CAPACITY_ENTRY: str(MAX_CAPACITY + 100),
    }
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert KEY_CAPACITY_ENTRY in errors
    assert f"{MIN_CAPACITY} - {MAX_CAPACITY}" in errors[KEY_CAPACITY_ENTRY]


def test_valid_classroom_data():
    data = {KEY_NAME_ENTRY: "Reloj 101", KEY_CAPACITY_ENTRY: "100"}
    errors = validator.validate_classroom_data_and_return_errors(data)
    assert errors == {}
