MAX_GRADE = 7.0
MIN_GRADE = 1.0


def validate_student_evaluation_data(data, student_evaluation_id=None):
    errors = {}

    grade = float((data.get('grade') or '').strip())
    validate_grade(grade, errors)

    return errors


def validate_grade(grade, errors):
    if grade < MIN_GRADE or grade > MAX_GRADE:
        errors['grade'] = f'La nota debe estar entre {MIN_GRADE} y {MAX_GRADE}'

    return errors
