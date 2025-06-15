from unittest.mock import patch, MagicMock

from app.validators import student_course_validator as validator

@patch('app.validators.student_course_validator.has_approved_course')
def test_has_met_prerequisites_fails(mock_has_approved):
    course = MagicMock(prerequisites=[MagicMock(prerequisite=MagicMock(id=1))])
    section = MagicMock(course_instance=MagicMock(course=course))
    mock_has_approved.return_value = False
    result, message = validator.has_met_prerequisites(1, section)

    assert not result
    assert 'no ha aprobado' in message

@patch('app.validators.student_course_validator.has_approved_course')
def test_has_met_prerequisites_succeeds(mock_has_approved):
    course = MagicMock(prerequisites=[MagicMock(prerequisite=MagicMock(id=1))])
    section = MagicMock(course_instance=MagicMock(course=course))
    mock_has_approved.return_value = True
    result, message = validator.has_met_prerequisites(1, section)

    assert result
    assert message is None
