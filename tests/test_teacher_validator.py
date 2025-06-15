from unittest.mock import patch, MagicMock

from app.validators import teacher_validator as validator

@patch('app.validators.teacher_validator.Teacher')
def test_validate_teacher_data_all_valid(mock_teacher):
    mock_teacher.query.filter_by.return_value.first.return_value = None
    data = {
        'first_name': 'Ana',
        'last_name': 'Pérez',
        'email': 'ana@example.com'
    }
    errors = validator.validate_teacher_data(data)

    assert errors == {}

@patch('app.validators.teacher_validator.Teacher')
def test_validate_teacher_data_missing_fields(mock_teacher):
    data = {
        'first_name': '',
        'last_name': '',
        'email': ''
    }
    errors = validator.validate_teacher_data(data)

    assert 'first_name' in errors
    assert 'last_name' in errors
    assert 'email' in errors

@patch('app.validators.teacher_validator.Teacher')
def test_validate_teacher_data_length_errors(mock_teacher):
    data = {
        'first_name': 'a' * 51,
        'last_name': 'b' * 51,
        'email': 'c' * 51
    }
    mock_teacher.query.filter_by.return_value.first.return_value = None
    errors = validator.validate_teacher_data(data)

    assert 'first_name' in errors
    assert 'last_name' in errors
    assert 'email' in errors

@patch('app.validators.teacher_validator.Teacher')
def test_validate_teacher_data_email_taken(mock_teacher):
    mock_teacher.query.filter_by.return_value.first.return_value = (
        MagicMock(id=2)
    )
    data = {
        'first_name': 'Ana',
        'last_name': 'Pérez',
        'email': 'ana@example.com'
    }
    errors = validator.validate_teacher_data(data, teacher_id=1)

    assert 'email' in errors
    assert 'ya está en uso' in errors['email']
