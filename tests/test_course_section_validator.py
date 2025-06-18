from unittest.mock import MagicMock, patch

import pytest

from app.validators import course_section_validator as validator


@pytest.mark.parametrize(
    "nrc, expected_error",
    [
        ("", "El NRC es obligatorio."),
        ("123", "El NRC debe ser un número de 4 dígitos."),
    ],
)
def test_validate_nrc_invalid_inputs(nrc, expected_error):
    """Tests NRC validation with invalid inputs."""
    errors = {}
    validator.validate_nrc(nrc, None, errors)

    assert "nrc" in errors
    assert errors["nrc"] == expected_error


@patch("app.validators.course_section_validator.CourseSection")
def test_validate_nrc_duplicate(mock_course_section_model):
    """Tests NRC validation when NRC is duplicated."""
    errors = {}
    mock_instance = MagicMock()
    mock_instance.id = 2

    query = mock_course_section_model.query
    filtered = query.filter_by.return_value
    filtered.first.return_value = mock_instance

    validator.validate_nrc("1234", 1, errors)

    assert "nrc" in errors
    assert "ya está en uso" in errors["nrc"]


@patch("app.validators.course_section_validator.CourseSection")
def test_validate_nrc_valid(mock_course_section_model):
    """Tests NRC validation with valid, unique NRC."""
    errors = {}

    query = mock_course_section_model.query
    filtered = query.filter_by.return_value
    filtered.first.return_value = None

    validator.validate_nrc("1234", None, errors)

    assert errors == {}


def test_validate_evaluation_types_warning_below_100():
    """Tests warning when total ponderation is below 100%."""
    course_section = MagicMock()
    course_section.overall_ponderation_type = "Porcentaje"
    eval_type = MagicMock()
    eval_type.overall_ponderation = 30.0
    course_section.evaluation_types = [eval_type, eval_type]
    warning = validator.validate_evaluation_types_warning(course_section)

    assert "Falta completar hasta 100%" in warning


def test_validate_evaluation_types_warning_not_percentage():
    """Tests no warning for ponderation type not being percentage."""
    course_section = MagicMock()
    course_section.overall_ponderation_type = "Peso"
    warning = validator.validate_evaluation_types_warning(course_section)

    assert warning is None


def test_validate_evaluations_warning_below_100():
    """Tests warning when evaluations do not sum to 100%."""
    evaluation = MagicMock()
    evaluation.ponderation = 30
    eval_type = MagicMock()
    eval_type.id = 1
    eval_type.topic = "Parcial"
    eval_type.ponderation_type = "Porcentaje"
    eval_type.evaluations = [evaluation, evaluation]
    course_section = MagicMock()
    course_section.evaluation_types = [eval_type]
    warnings = validator.validate_evaluations_warning(course_section)

    assert 1 in warnings
    assert "Falta ponderar instancias" in warnings[1]


def test_validate_course_section_wrapper_valid():
    """Tests course section validation returns no errors."""
    data = {"nrc": "1234"}
    with patch(
        "app.validators.course_section_validator.CourseSection"
    ) as mock_model:
        mock_model.query.filter_by.return_value.first.return_value = None
        errors = validator.validate_course_section(data)

        assert errors == {}
