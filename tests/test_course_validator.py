from unittest.mock import MagicMock, patch

from app.validators import course_validator as validator


def test_validate_text_field_empty():
    errors = {}
    validator.validate_text_field('name', '', 10, errors)

    assert 'name' in errors


def test_validate_text_field_too_long():
    errors = {}
    validator.validate_text_field('description', 'x' * 101, 100, errors)

    assert 'description' in errors


@patch('app.validators.course_validator.Course')
def test_validate_course_code_duplicate(mock_course_model):
    errors = {}
    mock_instance = MagicMock()
    mock_instance.id = 2
    mock_course_model.query.filter_by.return_value.first.return_value = (
        mock_instance
    )

    validator.validate_course_code('1234', 1, errors)

    assert 'code' in errors
    assert 'ya está en uso' in errors['code']


@patch('app.validators.course_validator.Course')
def test_validate_course_code_valid(mock_course_model):
    errors = {}
    mock_course_model.query.filter_by.return_value.first.return_value = None
    validator.validate_course_code('1234', None, errors)

    assert errors == {}


def test_validate_credits_non_integer():
    errors = {}
    validator.validate_credits('abc', errors)

    assert 'credits' in errors


def test_validate_credits_out_of_bounds():
    errors = {}
    validator.validate_credits('0', errors)
    assert 'credits' in errors

    errors = {}
    validator.validate_credits('5', errors)
    assert 'credits' in errors


def test_validate_course_data_valid():
    data = {
        'name': 'Algoritmos',
        'description': 'Curso básico',
        'code': '1234',
        'credits': '3',
    }
    with patch('app.validators.course_validator.Course') as mock_model:
        mock_model.query.filter_by.return_value.first.return_value = None
        errors = validator.validate_course_data(data)

        assert errors == {}
