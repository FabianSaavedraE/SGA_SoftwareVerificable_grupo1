from app import db
from app.models import Evaluation, StudentEvaluations
from app.validators.data_load_validators import validate_json_has_required_key

STUDENT_EVALUATION_JSON_KEY = "notas"

from app.validators.data_load_validators import (
    validate_entry_can_be_loaded,
    validate_entry_has_required_keys,
)

STUDENT_EVALUATION_JSON_KEY = "notas"
KEYS_IN_JSON = ["alumno_id", "topico_id", "instancia", "nota"]


def get_student_evaluation(student_id, evaluation_id):
    student_evaluation = StudentEvaluations.query.get((student_id, evaluation_id))
    return student_evaluation


def create_student_evaluation(data):
    new_student_evaluation = StudentEvaluations(
        student_id=data.get("student_id"),
        evaluation_id=data.get("evaluation_id"),
        grade=data.get("grade"),
    )
    db.session.add(new_student_evaluation)
    db.session.commit()

    return new_student_evaluation


def update_student_evaluation(student_evaluation, data):
    if not student_evaluation:
        return None

    student_evaluation.grade = data.get("grade", student_evaluation.grade)

    db.session.commit()
    return student_evaluation


def create_student_evaluation_json(data):
    if not validate_json_has_required_key(data, STUDENT_EVALUATION_JSON_KEY):
        return None

    student_evaluations = data.get(STUDENT_EVALUATION_JSON_KEY, [])

    for evaluation in student_evaluations:
        if not validate_entry_has_required_keys(evaluation, KEYS_IN_JSON):
            return None

        if not validate_entry_can_be_loaded(
            transform_json_entry_into_processable_student_evaluation_format(evaluation),
            "student_evaluation",
        ):
            return None

    create_all_student_evaluation_entries(student_evaluations)


def create_all_student_evaluation_entries(student_evaluations):
    for entry in student_evaluations:
        transformed_data = (
            transform_json_entry_into_processable_student_evaluation_format(entry)
        )

        if transformed_data:
            create_student_evaluation(transformed_data)
        else:
            break


def get_evaluation_id_by_topic_and_instance(evaluation_type_id, instance):
    instance = parse_int(instance)

    if instance is None or instance < 1:
        return None

    evaluations = (
        Evaluation.query.filter_by(evaluation_type_id=evaluation_type_id)
        .order_by(Evaluation.id)
        .all()
    )

    if instance > len(evaluations):
        return None

    selected_evaluation_id = evaluations[instance - 1].id
    return selected_evaluation_id


def transform_json_entry_into_processable_student_evaluation_format(
    student_evaluation,
):
    evaluation_type_id = student_evaluation.get("topico_id")
    instance_id = student_evaluation.get("instancia")
    evaluation_id = get_evaluation_id_by_topic_and_instance(
        evaluation_type_id, instance_id
    )

    data = {
        "student_id": student_evaluation.get("alumno_id"),
        "grade": student_evaluation.get("nota"),
        "evaluation_id": evaluation_id,
        "evaluation_type_id": evaluation_type_id,
    }

    return data


def parse_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None
