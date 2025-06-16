from datetime import datetime

from app.controllers.course_instance_controller import get_course_instance
from app.models import CourseInstance

MIN_YEAR = 1980


def validate_course_instance(data, course_instance_id=None):
    errors = {}

    year = get_stripped_field(data, 'year')
    semester = get_stripped_field(data, 'semester')
    course_id = get_stripped_field(data, 'course_id')

    validate_year(year, errors)
    validate_semester(semester, errors)
    validate_course_instance_uniqueness(
        year, semester, course_instance_id, course_id, errors
    )

    return errors


def get_stripped_field(data, field):
    return (str(data.get(field) or '')).strip()


def validate_year(year, errors):
    if not year:
        errors['year'] = 'El año es obligatorio.'
    elif not is_valid_year(year):
        errors['year'] = (
            f'El año debe estar entre {MIN_YEAR} y {datetime.now().year}'
        )


def validate_semester(semester, errors):
    if not semester:
        errors['semester'] = 'El semestre es obligatorio.'


def validate_course_instance_uniqueness(
    year, semester, course_instance_id, course_id, errors
):
    if not course_id and course_instance_id:
        course_instance = get_course_instance(course_instance_id)
        if course_instance:
            course_id = course_instance.course_id

    if not errors.get('year') and not errors.get('semester') and course_id:
        existing_instance = (
            CourseInstance.query.filter_by(
                course_id=course_id, year=year, semester=semester
            )
            .filter(CourseInstance.id != course_instance_id)
            .first()
        )

        if existing_instance:
            errors['exists'] = (
                f'Ya existe una instancia de este curso para '
                f'{year}-{semester}.'
            )


def is_valid_year(year):
    current_year = datetime.now().year
    return MIN_YEAR <= int(year) <= int(current_year)
