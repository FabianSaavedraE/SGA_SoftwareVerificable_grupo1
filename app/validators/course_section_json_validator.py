from app.models import CourseInstance
from app.models import Teacher
from app.validators.constants import * 

def validate_section_entry_from_json_and_return_errors(entry):
    errors = {}

    typing_errors = return_section_typing_errors(entry)
    requirement_errors = return_section_requirements_errors(entry)

    errors.update(typing_errors)
    errors.update(requirement_errors)

    return errors

def validate_evaluations_entry_from_json_and_return_errors(entry):
    errors = {}

    typing_errors = return_evaluations_typing_errors(entry)
    
    if typing_errors:
        return typing_errors


    type = entry.get(KEY_TOPIC_TYPE_JSON)

    topics = entry.get(KEY_TOPIC_COMBINATION_JSON)

    #First validate all topics don't have errors in formating:
    topic_errors = {}
    for topic in topics:
        topic_errors.update(return_topics_typing_errors(topic))

    if topic_errors:
        return topic_errors
    
    #Then we can cicle again, since operations are performed, validation needs
    #to be done.
    if type == PERCENTAGE:
        total_sum_of_percentages = 0
        for topic in topics:
            total_sum_of_percentages += topic.get(KEY_TOPIC_VALUE_JSON)

        total_sum_of_percentages= round(total_sum_of_percentages or 0, 2)
        if total_sum_of_percentages != 100:
            errors[PERCENTAGE] = (
                f'{PERCENTAGE} {OVERFLOWS} 100 en {topics}'
                )
            return errors
            
    #Same logic above presents here:
    evaluation_instances = entry.get(KEY_TOPIC_JSON)

    for key in evaluation_instances.keys():
        evaluation_instance = evaluation_instances[key]
        evaluation_instance_typing_errors = (
        return_evaluation_instance_typing_errors(evaluation_instance)
        )

        if evaluation_instance_typing_errors:
            return evaluation_instance_typing_errors

        type = evaluation_instance.get(KEY_TOPIC_TYPE_JSON)
        values = evaluation_instance.get(KEY_TOPIC_VALUES_JSON)
        if type == PERCENTAGE:
            total_sum_of_percentages = 0
            for value in values:
                total_sum_of_percentages += value
            total_sum_of_percentages= round(total_sum_of_percentages or 0, 2)
            if total_sum_of_percentages != 100:
                errors[PERCENTAGE] = (
                    f'{PERCENTAGE} {OVERFLOWS} 100 en {evaluation_instances}'
                    )
                return errors


    return errors

def return_section_typing_errors(entry):
    errors = {}
    id = entry.get(KEY_ID_ENTRY)
    course_id = entry.get(KEY_COURSE_INSTANCE_JSON)
    teacher_id = entry.get(KEY_TEACHER_ID_JSON)

    if not isinstance(id, int):
        errors[KEY_ID_ENTRY] = f'{KEY_ID_ENTRY} {MUST_BE_INT}'

    if not isinstance(course_id, int):
        errors[KEY_COURSE_INSTANCE_JSON] = (
            f'{KEY_COURSE_INSTANCE_JSON} {MUST_BE_INT}'
            )
        
    if not isinstance(teacher_id, int):
        errors[KEY_TEACHER_ID_JSON] = f'{KEY_TEACHER_ID_JSON} {MUST_BE_INT}'

    return errors

def return_section_requirements_errors(entry):
    errors = {}
    course_id = entry.get(KEY_COURSE_INSTANCE_JSON)
    teacher_id = entry.get(KEY_TEACHER_ID_JSON)

    if not CourseInstance.query.get(course_id):
        errors[KEY_COURSE_INSTANCE_JSON] = (
            f'{KEY_COURSE_INSTANCE_JSON} {DOESNT_EXIST}'
        ) 
    if not Teacher.query.get(teacher_id):
        errors[KEY_TEACHER_ID_JSON] = (
            f'{KEY_TEACHER_ID_JSON} {DOESNT_EXIST}'
        ) 

    return errors

def return_evaluations_typing_errors(entry):
    errors = {}
    type = entry.get(KEY_TOPIC_TYPE_JSON)
    topic_combinations = entry.get(KEY_TOPIC_COMBINATION_JSON)
    topics = entry.get(KEY_TOPIC_JSON)

    if not isinstance(type, str):
        errors[KEY_TOPIC_TYPE_JSON] = f'{KEY_TOPIC_TYPE_JSON} {MUST_BE_STRING}'

    if not isinstance(topic_combinations, list):
        errors[KEY_COURSE_INSTANCE_JSON] = (
            f'{KEY_COURSE_INSTANCE_JSON} {MUST_BE_LIST}'
            )
        
    if not isinstance(topics, dict):
        errors[KEY_TEACHER_ID_JSON] = f'{KEY_TEACHER_ID_JSON} {MUST_BE_DICT}'

    return errors

def return_topics_typing_errors(entry):
    errors = {}
    name = entry.get(KEY_TOPIC_NAME_JSON)
    id = entry.get(KEY_ID_ENTRY)
    value = entry.get(KEY_TOPIC_VALUE_JSON)

    if not isinstance(name, str):
        errors[KEY_TOPIC_NAME_JSON] = (
            f'{KEY_TOPIC_NAME_JSON} {MUST_BE_STRING}'
        )
    if not isinstance(id, int):
        errors[KEY_ID_ENTRY] = (
            f'{KEY_ID_ENTRY} {MUST_BE_INT}'
        )
    if not (isinstance(value, float) or isinstance(value,int)):
        errors[KEY_TOPIC_VALUE_JSON] = (
            f'{KEY_TOPIC_VALUE_JSON} {MUST_BE_FLOAT}'
        )

    return errors

def return_evaluation_instance_typing_errors(entry):
    errors = {}
    id = entry.get(KEY_ID_ENTRY)
    quantity = entry.get(KEY_TOPIC_QUANTITY_JSON)
    type = entry.get(KEY_TOPIC_TYPE_JSON)
    values = entry.get(KEY_TOPIC_VALUES_JSON)
    mandatory = entry.get(KEY_MANDATORY_EVALUATIONS_JSON)

    if not isinstance(id, int):
        errors[KEY_ID_ENTRY] = (
            f'{KEY_ID_ENTRY} {MUST_BE_INT}'
        )
    
    if not isinstance(quantity, int):
        errors[KEY_TOPIC_QUANTITY_JSON] = (
            f'{KEY_TOPIC_QUANTITY_JSON} {MUST_BE_INT}'
        )
    
    if not isinstance(type, str):
        errors[KEY_TOPIC_TYPE_JSON] = (
            f'{KEY_TOPIC_TYPE_JSON} {MUST_BE_STRING}'
        )
    
    if not isinstance(values, list):
        errors[KEY_TOPIC_VALUES_JSON] = (
            f'{KEY_TOPIC_VALUES_JSON} {MUST_BE_LIST}'
        )
    else:
        for value in values:
            if not (
                isinstance(value, float) or isinstance(value,int)
                ) or len(values) == 0:

                errors[KEY_TOPIC_VALUES_JSON] = (
                    f'{KEY_TOPIC_VALUES_JSON} {KEY_MUST_CONTAIN_INTS}'
                )

    if not isinstance(mandatory, list):
        errors[KEY_MANDATORY_EVALUATIONS_JSON] = (
            f'{KEY_MANDATORY_EVALUATIONS_JSON} {MUST_BE_LIST}'
        )
    else:
        for boolean in mandatory:
            if not isinstance(boolean, bool) or len(mandatory) == 0:
                errors[KEY_MANDATORY_EVALUATIONS_JSON] = (
                    f'{KEY_MANDATORY_EVALUATIONS_JSON} {MUST_BE_BOOL}'
                )
    
    return errors