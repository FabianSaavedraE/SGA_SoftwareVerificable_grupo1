from unittest.mock import patch, MagicMock

import pytest

from app.validators import classroom_validator as validator

@pytest.fixture(autouse=True)
def patch_classroom_query():
    with patch('app.validators.classroom_validator.Classroom') as (
        mock_classroom
    ):
        mock_classroom.query.filter_by.return_value.first.return_value = None
        yield mock_classroom

def test_validate_classroom_data_name_required():
    data = {'name': '', 'capacity': '10'}
    errors = validator.validate_classroom_data(data)

    assert 'name' in errors
    assert errors['name'] == 'El nombre es obligatorio.'

def test_validate_classroom_data_name_too_long():
    data = {'name': 'A' * 21, 'capacity': '10'}
    errors = validator.validate_classroom_data(data)

    assert 'name' in errors
    assert 'no puede superar' in errors['name']

def test_validate_classroom_data_name_already_exists(patch_classroom_query):
    existing = MagicMock()
    existing.id = 2
    patch_classroom_query.query.filter_by.return_value.first.return_value = (
        existing
    )

    data = {'name': 'ExistingRoom', 'capacity': '10'}
    errors = validator.validate_classroom_data(data, classroom_id=1)

    assert 'name' in errors
    assert 'ya existe' in errors['name']

def test_validate_classroom_data_name_exists_same_id(patch_classroom_query):
    existing = MagicMock()
    existing.id = 1
    patch_classroom_query.query.filter_by.return_value.first.return_value = (
        existing
    )

    data = {'name': 'ExistingRoom', 'capacity': '10'}
    errors = validator.validate_classroom_data(data, classroom_id=1)

    assert 'name' not in errors

def test_validate_classroom_data_capacity_required():
    data = {'name': 'Room1', 'capacity': ''}
    errors = validator.validate_classroom_data(data)

    assert 'capacity' in errors
    assert errors['capacity'] == 'La capacidad es obligatoria.'

def test_validate_classroom_data_capacity_not_int():
    data = {'name': 'Room1', 'capacity': 'abc'}
    errors = validator.validate_classroom_data(data)

    assert 'capacity' in errors
    assert 'entero' in errors['capacity']

def test_validate_classroom_data_capacity_out_of_range_low():
    data = {'name': 'Room1', 'capacity': '0'}
    errors = validator.validate_classroom_data(data)

    assert 'capacity' in errors
    assert 'entre 1 y 400' in errors['capacity']

def test_validate_classroom_data_capacity_out_of_range_high():
    data = {'name': 'Room1', 'capacity': '1000'}
    errors = validator.validate_classroom_data(data)

    assert 'capacity' in errors
    assert 'entre 1 y 400' in errors['capacity']

def test_validate_classroom_data_valid():
    data = {'name': 'Room1', 'capacity': '100'}
    errors = validator.validate_classroom_data(data)

    assert errors == {}
