from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from app.validators import course_instance_validator as validator
from app.validators.constants import (
    KEY_INSTANCE_COURSE_ID_ENTRY,
    KEY_INSTANCE_JSON,
    KEY_SEMESTER_ENTRY,
    KEY_YEAR_ENTRY,
)


@pytest.fixture(autouse=True)
def patch_models():
    """Patches Course and CourseInstance models for all tests."""
    with (
        patch(
            "app.validators.course_instance_validator.Course"
        ) as mock_course,
        patch(
            "app.validators.course_instance_validator.CourseInstance"
        ) as mock_instance,
    ):
        yield mock_course, mock_instance


def test_get_stripped_field_returns_stripped_string():
    """Tests if get_stripped_field returns a stripped string."""
    data = {"year": " 2020 "}
    result = validator.get_stripped_field(data, "year")
    assert result == "2020"


def test_attribute_errors_invalid_semester(patch_models):
    """Tests error returned when semester value is invalid."""
    patch_models[0].query.get.return_value = True
    data = {
        KEY_YEAR_ENTRY: "2023",
        KEY_SEMESTER_ENTRY: "3",
        KEY_INSTANCE_COURSE_ID_ENTRY: "1",
    }
    errors = validator.return_instance_attributes_errors(data)
    assert KEY_SEMESTER_ENTRY in errors


def test_attribute_errors_nonexistent_course(patch_models):
    """Tests error when the course does not exist."""
    patch_models[0].query.get.return_value = None
    data = {
        KEY_YEAR_ENTRY: "2023",
        KEY_SEMESTER_ENTRY: "1",
        KEY_INSTANCE_COURSE_ID_ENTRY: "99",
    }
    errors = validator.return_instance_attributes_errors(data)
    assert KEY_INSTANCE_COURSE_ID_ENTRY in errors


def test_validate_course_instance_uniqueness_conflict(patch_models):
    """Tests error when course instance uniqueness is violated."""
    mock_course, mock_instance = patch_models
    mock_course.query.get.return_value = MagicMock(
        __str__=lambda self: "Course X"
    )

    query = mock_instance.query.filter_by.return_value
    filtered = query.filter.return_value
    filtered.first.return_value = MagicMock()

    data = {
        KEY_YEAR_ENTRY: "2024",
        KEY_SEMESTER_ENTRY: "1",
        KEY_INSTANCE_COURSE_ID_ENTRY: "1",
    }
    errors = validator.validate_course_instance_uniqueness_and_return_errors(
        data, course_instance_id=999
    )

    assert KEY_INSTANCE_JSON in errors


def test_validate_course_instance_uniqueness_no_conflict(patch_models):
    """Tests that no error is returned if instance is unique."""
    mock_course, mock_instance = patch_models
    mock_course.query.get.return_value = MagicMock()

    query = mock_instance.query.filter_by.return_value
    filtered = query.filter.return_value
    filtered.first.return_value = None

    data = {
        KEY_YEAR_ENTRY: "2024",
        KEY_SEMESTER_ENTRY: "1",
        KEY_INSTANCE_COURSE_ID_ENTRY: "1",
    }
    errors = validator.validate_course_instance_uniqueness_and_return_errors(
        data, course_instance_id=999
    )

    assert KEY_INSTANCE_JSON not in errors


def test_validate_course_instance_and_return_errors_all_valid(patch_models):
    """Tests full validation returns no errors for valid data."""
    mock_course, mock_instance = patch_models
    mock_course.query.get.return_value = MagicMock()

    query = mock_instance.query.filter_by.return_value
    filtered = query.filter.return_value
    filtered.first.return_value = None

    data = {
        KEY_YEAR_ENTRY: str(datetime.now().year),
        KEY_SEMESTER_ENTRY: "1",
        KEY_INSTANCE_COURSE_ID_ENTRY: "1",
    }

    errors = validator.validate_course_instance_and_return_errors(
        data, course_instance_id=None
    )
    assert errors == {}
