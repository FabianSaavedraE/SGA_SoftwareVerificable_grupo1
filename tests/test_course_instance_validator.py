from unittest.mock import patch, MagicMock
from datetime import datetime
from app.validators import course_instance_validator as validator

def test_get_stripped_field_returns_stripped_string():
    data = {'year': ' 2020 '}
    result = validator.get_stripped_field(data, 'year')
    assert result == '2020'

def test_validate_year_missing():
    errors = {}
    validator.validate_year('', errors)
    assert 'year' in errors

def test_validate_year_invalid_low():
    errors = {}
    validator.validate_year('1970', errors)
    assert 'year' in errors

def test_validate_year_invalid_high():
    errors = {}
    future_year = str(datetime.now().year + 1)
    validator.validate_year(future_year, errors)
    assert 'year' in errors

def test_validate_year_valid():
    errors = {}
    current_year = str(datetime.now().year)
    validator.validate_year(current_year, errors)
    assert 'year' not in errors

def test_validate_semester_missing():
    errors = {}
    validator.validate_semester('', errors)
    assert 'semester' in errors

@patch('app.validators.course_instance_validator.get_course_instance')
@patch('app.validators.course_instance_validator.CourseInstance')
def test_validate_course_instance_uniqueness_exists(
    mock_course_instance_model, mock_get_course_instance
):
    errors = {}
    mock_get_course_instance.return_value = MagicMock(course_id=1)
    query = mock_course_instance_model.query.filter_by.return_value
    query.filter.return_value.first.return_value = MagicMock()

    validator.validate_course_instance_uniqueness('2023', '1', 1, None, errors)
    assert 'exists' in errors

@patch('app.validators.course_instance_validator.get_course_instance')
@patch('app.validators.course_instance_validator.CourseInstance')
def test_validate_course_instance_uniqueness_no_conflict(
    mock_course_instance_model, mock_get_course_instance
):
    errors = {}
    mock_get_course_instance.return_value = MagicMock(course_id=1)
    query = mock_course_instance_model.query.filter_by.return_value
    query.filter.return_value.first.return_value = None

    validator.validate_course_instance_uniqueness('2023', '1', 1, None, errors)
    assert 'exists' not in errors

@patch('app.validators.course_instance_validator.CourseInstance')
@patch('app.validators.course_instance_validator.get_course_instance')
def test_validate_course_instance_all_validations(
    mock_get_course_instance, mock_course_instance_model
):
    data = {'year': '2023', 'semester': '1', 'course_id': '2'}

    mock_get_course_instance.return_value = MagicMock(course_id=2)
    query = mock_course_instance_model.query.filter_by()
    query = query.filter()
    query.first.return_value = None

    errors = validator.validate_course_instance(data)
    assert errors == {}

def test_is_valid_year():
    current_year = datetime.now().year
    assert validator.is_valid_year(str(current_year))
    assert not validator.is_valid_year('1970')
    assert not validator.is_valid_year(str(current_year + 1))
