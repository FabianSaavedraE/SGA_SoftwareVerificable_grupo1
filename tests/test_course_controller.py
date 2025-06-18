from app.controllers.course_controller import (
    format_course_code,
    get_raw_code_from_course,
    has_course_been_closed,
)


def test_format_course_code():
    """Tests that course code is correctly formatted with ICC prefix."""
    assert format_course_code("23") == "ICC0023"
    assert format_course_code("123") == "ICC0123"
    assert format_course_code("0001") == "ICC0001"


def test_get_raw_code_from_course():
    """Tests that raw code is extracted from a course object."""

    class DummyCourse:
        def __init__(self, code):
            self.code = code

    course = DummyCourse("ICC1234")
    assert get_raw_code_from_course(course) == "1234"


def test_has_course_been_closed():
    """Tests if course status changed from Open to Closed."""
    assert has_course_been_closed("Open", "Closed") is True
    assert has_course_been_closed("Closed", "Open") is False
    assert has_course_been_closed("Closed", "Closed") is False
    assert has_course_been_closed("Open", "Open") is False
