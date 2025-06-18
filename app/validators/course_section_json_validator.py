import app.validators.constants as constants
from app.models import CourseInstance, Teacher


def validate_section_entry_from_json_and_return_errors(entry):
    """Validate a section entry from JSON data and returns errors."""
    errors = {}

    typing_errors = return_section_typing_errors(entry)
    requirement_errors = return_section_requirements_errors(entry)

    errors.update(typing_errors)
    errors.update(requirement_errors)

    return errors


def validate_evaluations_entry_from_json_and_return_errors(entry):
    """Validate evaluation entries from JSON data and returns errors."""
    errors = {}

    typing_errors = return_evaluations_typing_errors(entry)

    if typing_errors:
        return typing_errors

    entry_type = entry.get(constants.KEY_TOPIC_TYPE_JSON)

    topics = entry.get(constants.KEY_TOPIC_COMBINATION_JSON)

    # First validate all topics don't have errors in formatting:
    topic_errors = {}
    for topic in topics:
        topic_errors.update(return_topics_typing_errors(topic))

    if topic_errors:
        return topic_errors

    # Then we can cicle again, since operations are performed, validation needs
    # to be done.
    if entry_type == constants.PERCENTAGE:
        total_sum_of_percentages = 0
        for topic in topics:
            total_sum_of_percentages += topic.get(
                constants.KEY_TOPIC_VALUE_JSON
            )

        total_sum_of_percentages = round(total_sum_of_percentages or 0, 2)
        if total_sum_of_percentages != 100:
            errors[constants.PERCENTAGE] = (
                f"{constants.PERCENTAGE} {constants.OVERFLOWS} 100 en {topics}"
            )
            return errors

    # Same logic above presents here:
    evaluation_instances = entry.get(constants.KEY_TOPIC_JSON)

    for key in evaluation_instances.keys():
        evaluation_instance = evaluation_instances[key]
        evaluation_instance_typing_errors = (
            return_evaluation_instance_typing_errors(evaluation_instance)
        )

        if evaluation_instance_typing_errors:
            return evaluation_instance_typing_errors

        entry_type = evaluation_instance.get(constants.KEY_TOPIC_TYPE_JSON)
        values = evaluation_instance.get(constants.KEY_TOPIC_VALUES_JSON)
        if entry_type == constants.PERCENTAGE:
            total_sum_of_percentages = 0
            for value in values:
                total_sum_of_percentages += value
            total_sum_of_percentages = round(total_sum_of_percentages or 0, 2)
            if total_sum_of_percentages != 100:
                errors[constants.PERCENTAGE] = (
                    f"{constants.PERCENTAGE} {constants.OVERFLOWS} 100 en "
                    f"{evaluation_instances}"
                )
                return errors

    return errors


def return_section_typing_errors(entry):
    """Check for typing errors in a section entry."""
    errors = {}
    section_id = entry.get(constants.KEY_ID_ENTRY)
    course_id = entry.get(constants.KEY_COURSE_INSTANCE_JSON)
    teacher_id = entry.get(constants.KEY_TEACHER_ID_JSON)

    if not isinstance(section_id, int):
        errors[constants.KEY_ID_ENTRY] = (
            f"{constants.KEY_ID_ENTRY} {constants.MUST_BE_INT}"
        )

    if not isinstance(course_id, int):
        errors[constants.KEY_COURSE_INSTANCE_JSON] = (
            f"{constants.KEY_COURSE_INSTANCE_JSON} {constants.MUST_BE_INT}"
        )

    if not isinstance(teacher_id, int):
        errors[constants.KEY_TEACHER_ID_JSON] = (
            f"{constants.KEY_TEACHER_ID_JSON} {constants.MUST_BE_INT}"
        )

    return errors


def return_section_requirements_errors(entry):
    """Check for missing requirements in a section entry."""
    errors = {}
    course_id = entry.get(constants.KEY_COURSE_INSTANCE_JSON)
    teacher_id = entry.get(constants.KEY_TEACHER_ID_JSON)

    if not CourseInstance.query.get(course_id):
        errors[constants.KEY_COURSE_INSTANCE_JSON] = (
            f"{constants.KEY_COURSE_INSTANCE_JSON} {constants.DOESNT_EXIST}"
        )
    if not Teacher.query.get(teacher_id):
        errors[constants.KEY_TEACHER_ID_JSON] = (
            f"{constants.KEY_TEACHER_ID_JSON} {constants.DOESNT_EXIST}"
        )

    return errors


def return_evaluations_typing_errors(entry):
    """Check for typing errors in evaluation entries."""
    errors = {}
    key_type = entry.get(constants.KEY_TOPIC_TYPE_JSON)
    topic_combinations = entry.get(constants.KEY_TOPIC_COMBINATION_JSON)
    topics = entry.get(constants.KEY_TOPIC_JSON)

    if not isinstance(key_type, str):
        errors[constants.KEY_TOPIC_TYPE_JSON] = (
            f"{constants.KEY_TOPIC_TYPE_JSON} {constants.MUST_BE_STRING}"
        )

    if not isinstance(topic_combinations, list):
        errors[constants.KEY_COURSE_INSTANCE_JSON] = (
            f"{constants.KEY_COURSE_INSTANCE_JSON} {constants.MUST_BE_LIST}"
        )

    if not isinstance(topics, dict):
        errors[constants.KEY_TEACHER_ID_JSON] = (
            f"{constants.KEY_TEACHER_ID_JSON} {constants.MUST_BE_DICT}"
        )

    return errors


def return_topics_typing_errors(entry):
    """Check for typing errors in topic entries."""
    errors = {}
    name = entry.get(constants.KEY_TOPIC_NAME_JSON)
    key_id = entry.get(constants.KEY_ID_ENTRY)
    value = entry.get(constants.KEY_TOPIC_VALUE_JSON)

    if not isinstance(name, str):
        errors[constants.KEY_TOPIC_NAME_JSON] = (
            f"{constants.KEY_TOPIC_NAME_JSON} {constants.MUST_BE_STRING}"
        )
    if not isinstance(key_id, int):
        errors[constants.KEY_ID_ENTRY] = (
            f"{constants.KEY_ID_ENTRY} {constants.MUST_BE_INT}"
        )
    if not (isinstance(value, float) or isinstance(value, int)):
        errors[constants.KEY_TOPIC_VALUE_JSON] = (
            f"{constants.KEY_TOPIC_VALUE_JSON} {constants.MUST_BE_FLOAT}"
        )

    return errors


def return_evaluation_instance_typing_errors(entry):
    """Check for typing errors in an evaluation instance entry."""
    errors = {}
    evaluation_instance_id = entry.get(constants.KEY_ID_ENTRY)
    quantity = entry.get(constants.KEY_TOPIC_QUANTITY_JSON)
    evaluation_type = entry.get(constants.KEY_TOPIC_TYPE_JSON)
    values = entry.get(constants.KEY_TOPIC_VALUES_JSON)
    mandatory = entry.get(constants.KEY_MANDATORY_EVALUATIONS_JSON)

    if not isinstance(evaluation_instance_id, int):
        errors[constants.KEY_ID_ENTRY] = (
            f"{constants.KEY_ID_ENTRY} {constants.MUST_BE_INT}"
        )

    if not isinstance(quantity, int):
        errors[constants.KEY_TOPIC_QUANTITY_JSON] = (
            f"{constants.KEY_TOPIC_QUANTITY_JSON} {constants.MUST_BE_INT}"
        )

    if not isinstance(evaluation_type, str):
        errors[constants.KEY_TOPIC_TYPE_JSON] = (
            f"{constants.KEY_TOPIC_TYPE_JSON} {constants.MUST_BE_STRING}"
        )

    if not isinstance(values, list):
        errors[constants.KEY_TOPIC_VALUES_JSON] = (
            f"{constants.KEY_TOPIC_VALUES_JSON} {constants.MUST_BE_LIST}"
        )
    else:
        for value in values:
            if (
                not (isinstance(value, float) or isinstance(value, int))
                or len(values) == 0
            ):
                errors[constants.KEY_TOPIC_VALUES_JSON] = (
                    f"{constants.KEY_TOPIC_VALUES_JSON} "
                    f"{constants.KEY_MUST_CONTAIN_INTS}"
                )

    if not isinstance(mandatory, list):
        errors[constants.KEY_MANDATORY_EVALUATIONS_JSON] = (
            f"{constants.KEY_MANDATORY_EVALUATIONS_JSON} "
            f"{constants.MUST_BE_LIST}"
        )
    else:
        for boolean in mandatory:
            if not isinstance(boolean, bool) or len(mandatory) == 0:
                errors[constants.KEY_MANDATORY_EVALUATIONS_JSON] = (
                    f"{constants.KEY_MANDATORY_EVALUATIONS_JSON} "
                    f"{constants.MUST_BE_BOOL}"
                )

    return errors
