from unittest.mock import MagicMock, patch

from app.validators import student_validator as validator


def test_return_student_name_errors_first_name_required():
    """Test error when first name is missing in student data."""
    errors = validator.return_student_name_errors("first_name", "")
    assert "first_name" in errors
    assert "obligatorio" in errors["first_name"]


def test_return_entry_year_errors_valid_input():
    """Test no errors for a valid entry year."""
    errors = validator.return_entry_year_errors(2020)
    assert errors == {}


@patch("app.validators.student_validator.Student")
def test_return_student_email_errors_required_field(mock_student):
    """Test error when email field is missing or empty."""
    errors = validator.return_student_email_errors("", None)
    assert "email" in errors
    assert "obligatorio" in errors["email"]


@patch("app.validators.student_validator.Student")
def test_return_student_email_errors_valid_and_unique(mock_student):
    """Test no error for valid and unique email."""
    mock_student.query.filter_by.return_value.first.return_value = None
    errors = validator.return_student_email_errors("test@example.com", None)
    assert errors == {}


def test_get_stripped_field_removes_whitespace():
    """Test that leading/trailing whitespace is removed from a field."""
    data = {"first_name": "  Ana "}
    assert validator.get_stripped_field(data, "first_name") == "Ana"


@patch("app.validators.student_validator.Student")
def test_validate_student_data_with_multiple_errors(mock_student):
    """Test multiple validation errors returned for invalid data."""
    mock_student.query.filter_by.return_value.first.return_value = MagicMock()
    data = {
        "first_name": "",
        "last_name": "",
        "email": "x" * 60,
        "entry_year": "1970",
    }
    errors = validator.validate_student_data_and_return_errors(data)

    assert "first_name" in errors
    assert "last_name" in errors
    assert "email" in errors
    assert "entry_year" in errors
