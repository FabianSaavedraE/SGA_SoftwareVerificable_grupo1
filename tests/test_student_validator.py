from unittest.mock import patch, MagicMock

from app.validators import student_validator as validator

def test_validate_name_required():
    errors = {}
    validator.validate_name('first_name', '', errors)

    assert 'first_name' in errors
    assert 'obligatorio' in errors['first_name']

def test_validate_name_too_long():
    errors = {}
    long_name = 'a' * 51
    validator.validate_name('last_name', long_name, errors)

    assert 'last_name' in errors
    assert 'no puede superar' in errors['last_name']

def test_validate_entry_year_valid():
    errors = {}
    validator.validate_entry_year('2020', errors)

    assert errors == {}

def test_validate_entry_year_invalid_non_digit():
    errors = {}
    validator.validate_entry_year('abcd', errors)

    assert 'entry_year' in errors
    assert 'debe ser un número' in errors['entry_year']

def test_validate_entry_year_out_of_bounds():
    errors = {}
    validator.validate_entry_year('1970', errors)

    assert 'entry_year' in errors
    assert 'debe estar entre' in errors['entry_year']

@patch('app.validators.student_validator.Student')
def test_validate_email_required(mock_student):
    errors = {}
    validator.validate_email('', None, errors)

    assert 'email' in errors
    assert 'obligatorio' in errors['email']

@patch('app.validators.student_validator.Student')
def test_validate_email_too_long(mock_student):
    errors = {}
    email = 'a' * 51
    validator.validate_email(email, None, errors)

    assert 'email' in errors
    assert 'no puede superar' in errors['email']

@patch('app.validators.student_validator.Student')
def test_validate_email_duplicate(mock_student):
    mock_student.query.filter_by.return_value.first.return_value = (
        MagicMock(id=2)
    )
    errors = {}
    validator.validate_email('test@example.com', 1, errors)

    assert 'email' in errors
    assert 'ya está en uso' in errors['email']

@patch('app.validators.student_validator.Student')
def test_validate_email_ok(mock_student):
    mock_student.query.filter_by.return_value.first.return_value = None
    errors = {}
    validator.validate_email('test@example.com', None, errors)

    assert errors == {}

def test_normalize_entry_year_valid():
    assert validator.normalize_entry_year('2010') == 2010

def test_normalize_entry_year_invalid_type():
    assert validator.normalize_entry_year('abc') >= 1980

def test_get_stripped_field_works():
    data = {'first_name': '  Ana '}
    assert validator.get_stripped_field(data, 'first_name') == 'Ana'

@patch('app.validators.student_validator.Student')
def test_validate_student_data_with_errors(mock_student):
    mock_student.query.filter_by.return_value.first.return_value = MagicMock()
    data = {
        'first_name': '',
        'last_name': '',
        'email': 'x' * 60,
        'entry_year': '1970'
    }
    errors = validator.validate_student_data(data)

    assert 'first_name' in errors
    assert 'last_name' in errors
    assert 'email' in errors
    assert 'entry_year' in errors
