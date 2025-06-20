from unittest.mock import MagicMock, patch

from app.validators import schedule_validator as validator


def test_all_sections_have_students_returns_false():
    """Return False if any section has no students assigned."""
    sections = [{"section": MagicMock(students=[])}]
    valid, message = validator.all_sections_have_students(sections)

    assert not valid
    assert "no tiene estudiantes" in message


def test_all_sections_have_students_returns_true():
    """Return True if all sections have at least one student."""
    sections = [{"section": MagicMock(students=[1, 2])}]
    valid, message = validator.all_sections_have_students(sections)

    assert valid
    assert message is None


def test_all_sections_have_teacher_returns_false():
    """Return False if any section has no teacher assigned."""
    section = MagicMock(teacher=None, nrc="1234")
    sections = [{"section": section}]
    valid, message = validator.all_sections_have_teacher(sections)

    assert not valid
    assert "no tiene un profesor asignado" in message


def test_all_sections_have_teacher_returns_true():
    """Return True if all sections have a teacher assigned."""
    section = MagicMock(teacher=MagicMock())
    sections = [{"section": section}]
    valid, message = validator.all_sections_have_teacher(sections)

    assert valid
    assert message is None


@patch("app.validators.schedule_validator.get_all_classrooms")
def test_validate_classroom_capacity_fails(mock_get_all):
    """Fail validation if no classrooms are available."""
    mock_get_all.return_value = []
    valid, message = validator.validate_classroom_capacity(
        [{"num_students": 10}]
    )

    assert not valid
    assert "No hay salas disponibles" in message


@patch("app.validators.schedule_validator.get_all_classrooms")
def test_validate_classroom_capacity_succeeds(mock_get_all):
    """Pass validation if classrooms have enough capacity."""
    classrooms = [MagicMock(capacity=30)]
    sections = [{"num_students": 25}]
    mock_get_all.return_value = classrooms
    valid, message = validator.validate_classroom_capacity(sections)

    assert valid
    assert message is None


def test_validate_max_credits_per_section_fails():
    """Fail if section credits exceed the maximum allowed."""
    course = MagicMock(credits=5)
    course_instance = MagicMock(course=course)
    section = MagicMock(course_instance=course_instance, nrc="1234")
    valid, message = validator.validate_max_credits_per_section(
        [{"section": section}]
    )

    assert not valid
    assert "No se le puede asignar" in message


def test_validate_max_credits_per_section_passes():
    """Pass if section credits are within the allowed maximum."""
    course = MagicMock(credits=4)
    course_instance = MagicMock(course=course)
    section = MagicMock(course_instance=course_instance, nrc="1234")
    valid, message = validator.validate_max_credits_per_section(
        [{"section": section}]
    )

    assert valid
    assert message is None


@patch("app.validators.schedule_validator.get_all_classrooms")
def test_validate_classroom_capacity_with_blocks_fails(mock_get_all):
    """Fail if classrooms are insufficient for sections and timeslots."""
    mock_get_all.return_value = [MagicMock(), MagicMock()]
    course = MagicMock(credits=3)
    course_instance = MagicMock(course=course)
    section = {"section": MagicMock(course_instance=course_instance)}
    timeslots = [1]
    valid, message = validator.validate_classroom_capacity_with_blocks(
        [section, section, section], timeslots
    )

    assert not valid
    assert "No hay suficientes salas" in message


@patch("app.validators.schedule_validator.get_all_classrooms")
def test_validate_classroom_capacity_with_blocks_passes(mock_get_all):
    """Pass if enough classrooms are available for all blocks."""
    mock_get_all.return_value = [MagicMock(), MagicMock()]
    course = MagicMock(credits=1)
    course_instance = MagicMock(course=course)
    section = {"section": MagicMock(course_instance=course_instance)}
    timeslots = [1, 2, 3]
    valid, message = validator.validate_classroom_capacity_with_blocks(
        [section, section], timeslots
    )

    assert valid
    assert message is None
