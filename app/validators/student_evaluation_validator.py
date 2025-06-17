from app.models import Evaluation, EvaluationType, Student, StudentEvaluations
from app.validators.constants import (
    ALREADY_EXISTS,
    DOESNT_EXIST,
    DUPLICATED,
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

MAX_GRADE = 7.0
MIN_GRADE = 1.0


def validate_student_evaluation_data(
    data, original_student_id=None, original_evaluation_id=None
):
    errors = {}
    errors.update(validate_typing(data))

    if errors:
        return errors

    errors.update(validate_attributes(data))
    if errors:
        return errors

    errors.update(validate_student_exists_in_evaluation_course(data))
    if errors:
        return errors

    errors.update(
        validate_uniqueness(
            data,
            original_student_id=original_student_id,
            original_evaluation_id=original_evaluation_id,
        )
    )

    return errors


def validate_typing(data):
    errors = {}
    normalized_data = get_normalized_data(data)

    student_id = parse_int(normalized_data[KEY_STUDENT_ID_ENTRY])
    if student_id is None:
        errors[KEY_STUDENT_ID_ENTRY] = f"{KEY_STUDENT_ID_ENTRY} {MUST_BE_INT}"

    evaluation_type_id = parse_int(normalized_data[KEY_TOPIC_ID_ENTRY])
    if evaluation_type_id is None:
        errors[KEY_TOPIC_ID_ENTRY] = f"{KEY_TOPIC_ID_ENTRY} {MUST_BE_INT}"

    evaluation_id = parse_int(normalized_data[KEY_INSTANCE_ID_ENTRY])
    if evaluation_id is None:
        errors[KEY_INSTANCE_ID_ENTRY] = f"{KEY_INSTANCE_ID_ENTRY} {MUST_BE_INT}"

    grade = parse_float(normalized_data[KEY_GRADE_ENTRY])
    if grade is None:
        errors[KEY_GRADE_ENTRY] = f"{KEY_GRADE_ENTRY} {MUST_BE_FLOAT}"

    return errors


def validate_attributes(data):
    errors = {}
    normalized_data = get_normalized_data(data)

    student = get_entity_by_id(Student, normalized_data[KEY_STUDENT_ID_ENTRY])
    if not student:
        errors[KEY_STUDENT_ENTRY] = (
            f"{KEY_STUDENT_ENTRY} {normalized_data[KEY_STUDENT_ID_ENTRY]} "
            f"{DOESNT_EXIST}"
        )

    evaluation_type = get_entity_by_id(
        EvaluationType, normalized_data[KEY_TOPIC_ID_ENTRY]
    )
    if not evaluation_type:
        errors[KEY_EVALUATION_TYPE] = (
            f"{KEY_EVALUATION_TYPE} {normalized_data[KEY_TOPIC_ID_ENTRY]} "
            f"{DOESNT_EXIST}"
        )

    evaluation = get_entity_by_id(Evaluation, normalized_data[KEY_INSTANCE_ID_ENTRY])
    if not evaluation:
        errors[KEY_INSTANCE_ID_JSON] = (
            f"{KEY_INSTANCE_ID_JSON} {normalized_data[KEY_INSTANCE_ID_ENTRY]} "
            f"{DOESNT_EXIST}"
        )

    grade_errors = validate_grade(normalized_data[KEY_GRADE_ENTRY])
    if grade_errors:
        errors[KEY_GRADE_ENTRY] = grade_errors

    return errors


def validate_grade(grade):
    grade = parse_float(grade)
    if grade < MIN_GRADE or grade > MAX_GRADE:
        return f"{KEY_GRADE_JSON} {OVERFLOWS} {MIN_GRADE} y {MAX_GRADE}"

    return None


def validate_student_exists_in_evaluation_course(data):
    """
    Validates if student is enrolled in the course section associated with
    the evaluation type.
    """
    errors = {}
    normalized_data = get_normalized_data(data)

    student = get_entity_by_id(Student, normalized_data[KEY_STUDENT_ID_ENTRY])
    evaluation_type = get_entity_by_id(
        EvaluationType, normalized_data[KEY_TOPIC_ID_ENTRY]
    )

    if not student or not evaluation_type:
        return errors

    student_section_ids = {sc.course_section_id for sc in student.student_courses}
    eval_section_id = evaluation_type.course_section_id

    if eval_section_id not in student_section_ids:
        errors[KEY_STUDENT_ENTRY] = (
            f"{student.first_name} {student.last_name} (ID: {student.id}) "
            f"{NOT_ENROLLED_IN_SECTION}"
        )

    return errors


def validate_uniqueness(data, original_student_id=None, original_evaluation_id=None):
    errors = {}
    normalized_data = get_normalized_data(data)

    existing = StudentEvaluations.query.filter_by(
        student_id=normalized_data[KEY_STUDENT_ID_ENTRY],
        evaluation_id=normalized_data[KEY_INSTANCE_ID_ENTRY],
    ).first()

    if existing and (
        (normalized_data[KEY_STUDENT_ID_ENTRY] != original_student_id)
        or (normalized_data[KEY_INSTANCE_ID_ENTRY] != original_evaluation_id)
    ):
        student = get_entity_by_id(Student, normalized_data[KEY_STUDENT_ID_ENTRY])
        evaluation = get_entity_by_id(
            Evaluation, normalized_data[KEY_INSTANCE_ID_ENTRY]
        )

        if student and evaluation:
            errors[DUPLICATED] = (
                f"{student.first_name} {student.last_name} {ALREADY_EXISTS} en"
                f" {evaluation.evaluation_type.topic} - {evaluation.name}"
            )

    return errors


def parse_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def parse_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def get_normalized_data(data):
    return {
        KEY_STUDENT_ID_ENTRY: (
            (data.get(KEY_STUDENT_ID_JSON) if data else "")
            or (data.get(KEY_STUDENT_ID_ENTRY) if data else "")
            or ""
        ),
        KEY_INSTANCE_ID_ENTRY: (
            (data.get(KEY_INSTANCE_ID_JSON) if data else "")
            or (data.get(KEY_INSTANCE_ID_ENTRY) if data else "")
            or ""
        ),
        KEY_TOPIC_ID_ENTRY: (
            (data.get(KEY_TOPIC_ID_JSON) if data else "")
            or (data.get(KEY_TOPIC_ID_ENTRY) if data else "")
            or ""
        ),
        KEY_GRADE_ENTRY: (
            (data.get(KEY_GRADE_JSON) if data else "")
            or (data.get(KEY_GRADE_ENTRY) if data else "")
            or ""
        ),
    }


def get_entity_by_id(model, id_value):
    return model.query.get(id_value)
