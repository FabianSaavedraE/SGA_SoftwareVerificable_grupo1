from app.validators import student_evaluation_validator as validator


def test_validate_grade_out_of_bounds():
    errors = {}
    validator.validate_grade(8.0, errors)

    assert 'grade' in errors

    errors = {}
    validator.validate_grade(0.5, errors)

    assert 'grade' in errors


def test_validate_grade_in_bounds():
    errors = {}
    validator.validate_grade(5.5, errors)

    assert errors == {}


def test_validate_student_evaluation_data_invalid():
    data = {'grade': '7.5'}
    errors = validator.validate_student_evaluation_data(data)

    assert 'grade' in errors


def test_validate_student_evaluation_data_valid():
    data = {'grade': '6.0'}
    errors = validator.validate_student_evaluation_data(data)

    assert errors == {}
