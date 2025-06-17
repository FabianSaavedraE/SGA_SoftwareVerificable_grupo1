from unittest.mock import MagicMock, patch

from app.validators import student_evaluation_validator as validator
from app.validators.constants import (
    KEY_EVALUATION_TYPE,
    KEY_GRADE_ENTRY,
    KEY_GRADE_JSON,
    KEY_INSTANCE_ID_ENTRY,
    KEY_INSTANCE_ID_JSON,
    KEY_STUDENT_ENTRY,
    KEY_STUDENT_ID_ENTRY,
    KEY_STUDENT_ID_JSON,
    KEY_TOPIC_ID_ENTRY,
    KEY_TOPIC_ID_JSON,
    MUST_BE_FLOAT,
    MUST_BE_INT,
    NOT_ENROLLED_IN_SECTION,
    OVERFLOWS,
)


def make_valid_data():
    return {
        KEY_STUDENT_ID_JSON: "1",
        KEY_TOPIC_ID_JSON: "2",
        KEY_INSTANCE_ID_JSON: "3",
        KEY_GRADE_JSON: "6.5",
    }


def test_validate_grade_out_of_bounds():
    assert validator.validate_grade(0.5) is not None
    assert validator.validate_grade(8.0) is not None


def test_validate_grade_in_bounds():
    assert validator.validate_grade(5.5) is None


def test_validate_student_evaluation_data_invalid_grade_type():
    data = make_valid_data()
    data[KEY_GRADE_JSON] = "not_a_number"
    errors = validator.validate_student_evaluation_data(data)

    assert KEY_GRADE_ENTRY in errors
    assert MUST_BE_FLOAT in errors[KEY_GRADE_ENTRY]


def test_validate_student_evaluation_data_invalid_ids():
    data = {
        KEY_STUDENT_ID_JSON: "abc",
        KEY_TOPIC_ID_JSON: "xyz",
        KEY_INSTANCE_ID_JSON: None,
        KEY_GRADE_JSON: "6.5",
    }

    errors = validator.validate_student_evaluation_data(data)

    assert KEY_STUDENT_ID_ENTRY in errors
    assert KEY_TOPIC_ID_ENTRY in errors
    assert KEY_INSTANCE_ID_ENTRY in errors
    assert MUST_BE_INT in errors[KEY_STUDENT_ID_ENTRY]


@patch("app.validators.student_evaluation_validator.get_entity_by_id")
def test_validate_attributes_entities_not_found(mock_get_entity):
    mock_get_entity.return_value = None
    data = make_valid_data()
    errors = validator.validate_student_evaluation_data(data)

    assert KEY_STUDENT_ENTRY in errors
    assert KEY_EVALUATION_TYPE in errors
    assert KEY_INSTANCE_ID_JSON in errors


@patch("app.validators.student_evaluation_validator.get_entity_by_id")
def test_validate_grade_too_high(mock_get_entity):
    mock_get_entity.side_effect = lambda model, id: MagicMock()
    data = make_valid_data()
    data[KEY_GRADE_JSON] = "10.0"

    errors = validator.validate_student_evaluation_data(data)

    assert KEY_GRADE_ENTRY in errors
    assert OVERFLOWS in errors[KEY_GRADE_ENTRY]


@patch("app.validators.student_evaluation_validator.get_entity_by_id")
def test_student_not_enrolled_in_section(mock_get_entity):
    student = MagicMock()
    student.id = 1
    student.first_name = "Carlos"
    student.last_name = "Gómez"
    student.student_courses = [MagicMock(course_section_id=999)]

    evaluation_type = MagicMock()
    evaluation_type.course_section_id = 123

    def side_effect(model, id):
        if model.__name__ == "Student":
            return student
        elif model.__name__ == "EvaluationType":
            return evaluation_type
        return MagicMock()

    mock_get_entity.side_effect = side_effect

    data = make_valid_data()
    errors = validator.validate_student_evaluation_data(data)

    assert KEY_STUDENT_ENTRY in errors
    assert NOT_ENROLLED_IN_SECTION in errors[KEY_STUDENT_ENTRY]
