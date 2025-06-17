import pandas as pd
from io import BytesIO

from sqlalchemy import func

from app import db
from app.models import CourseSection, CourseInstance
from app.controllers.evaluation_type_controller import create_evaluation_type
from app.controllers.evaluation_controller import create_evaluation
from app.controllers.final_grades_controller import calculate_final_grades
from app.controllers.course_instance_controller import (
    get_course_instance_by_parameters
)
from app.validators.data_load_validators import (
    validate_json_has_required_key, validate_entry_has_required_keys,
    validate_entry_can_be_loaded
)

from app.validators.constants import (
    KEY_COURSE_INSTANCE_JSON, KEY_TEACHER_ID_JSON, KEY_EVALUATION_JSON,
    KEY_EVALUATION_TYPE_JSON, KEY_TOPIC_COMBINATION_JSON, KEY_TOPIC_NAME_JSON,
    KEY_TOPIC_VALUE_JSON, KEY_TOPIC_JSON, KEY_TOPIC_QUANTITY_JSON,
    KEY_TOPIC_TYPE_JSON, KEY_TOPIC_VALUES_JSON, KEY_MANDATORY_EVALUATIONS_JSON,
    KEY_ID_ENTRY
)

#Since the JSON structure for loading comprises multiple dictionaries, a lot
#of constants need to be correctly validated, hence the many lists creation:

KEYS_NEEDED_FOR_SECTION_ENTRY = (
    [KEY_ID_ENTRY, KEY_COURSE_INSTANCE_JSON, KEY_TEACHER_ID_JSON,
    KEY_EVALUATION_JSON]
)
KEYS_NEEDED_FOR_EVALUATION_ENTRY= (
    [KEY_TOPIC_TYPE_JSON, KEY_TOPIC_COMBINATION_JSON,KEY_TOPIC_JSON]
)
KEYS_NEEDED_FOR_TOPIC_COMBINATION = (
    [KEY_ID_ENTRY, KEY_TOPIC_NAME_JSON, KEY_TOPIC_VALUE_JSON]
)
KEYS_NEEDED_FOR_TOPIC= (
    [KEY_ID_ENTRY, KEY_TOPIC_QUANTITY_JSON, KEY_TOPIC_TYPE_JSON,
    KEY_TOPIC_VALUES_JSON, KEY_MANDATORY_EVALUATIONS_JSON]
)

KEY_COURSE_SECTIONS_JSON = "secciones"
NRC_LENGTH = 4
REPORT_COLUMNS = ['Estudiante', 'Email', 'Nota Final', 'Estado']

def get_all_sections():
    sections = CourseSection.query.all()
    return sections

def get_all_course_sections(course_instance_id):
    sections = CourseSection.query.filter_by(
        course_instance_id=course_instance_id
    ).all()
    return sections

def get_course_sections_by_parameters(year, semester):
    course_instances = get_course_instance_by_parameters(year, semester)
    sections = []

    for course in course_instances:
        course_sections = get_all_course_sections(course.id)
        sections.extend(course_sections)

    return sections
        
def get_section(course_section_id):
    course_section = CourseSection.query.get(course_section_id)
    return course_section

def create_section(data):
    raw_nrc = data.get('nrc', '').zfill(NRC_LENGTH)
    nrc = f'NRC{raw_nrc}'
    section_id = data.get('section_id')

    new_section = CourseSection(
        nrc = nrc,
        overall_ponderation_type = data.get('overall_ponderation_type'),
        course_instance_id = data.get('course_instance_id'),
        teacher_id = data.get('teacher_id') or None,
        state = data.get('state', 'Open')
    )

    if section_id is not None:
        new_section.id = section_id

    db.session.add(new_section)
    db.session.commit()

    return new_section

def update_section(course_section, data):
    if not course_section:
        return None
    
    previous_state = course_section.state
    raw_nrc = data.get('nrc', str(course_section.nrc)[NRC_LENGTH:])
    full_nrc = f"NRC{raw_nrc.zfill(NRC_LENGTH)}"

    course_section.nrc = full_nrc
    course_section.overall_ponderation_type = data.get(
        'overall_ponderation_type',
        course_section.overall_ponderation_type
    )
    course_section.teacher_id = data.get(
        'teacher_id',
        course_section.teacher_id
    ) or None
    course_section.state = data.get('state', course_section.state)

    db.session.commit()

    if has_section_been_closed(previous_state, course_section.state):
        calculate_final_grades(course_section)

    return course_section

def delete_section(course_section):
    if not course_section:
        return False

    db.session.delete(course_section)
    db.session.commit()
    return True

def create_course_sections_from_json(data):
    if not validate_json_has_required_key(data, KEY_COURSE_SECTIONS_JSON):
        return None

    course_sections = data.get('secciones', [])

    #First cicle validates all entries ----------------------------------------

    #Since the structure of the JSON is composed of many dictionaries inside
    #dictionaries, this function CAN'T be refactored into simpler code: All
    #validation processes will be convoluted due to the ammount of validations

    for course_section in course_sections:

        #First dictionary:
        if not validate_entry_has_required_keys(
            course_section, KEYS_NEEDED_FOR_SECTION_ENTRY
            ):
            return None
        
        if not validate_entry_can_be_loaded(
            course_section, 'section'
        ):
            return None
        
        #Second dictionary:
        evaluations = course_section.get(KEY_EVALUATION_JSON)
        if not validate_entry_has_required_keys(
            evaluations, KEYS_NEEDED_FOR_EVALUATION_ENTRY
        ):
            return None

        if not validate_entry_can_be_loaded(
            evaluations, 'evaluations'
        ):
            return None
        
        #Third dictionary:
        evaluation_instances = evaluations.get(KEY_TOPIC_COMBINATION_JSON)
        for evaluation_instance in evaluation_instances:
            if not validate_entry_has_required_keys(
                evaluation_instance, KEYS_NEEDED_FOR_TOPIC_COMBINATION
            ):
                return None
        
        #Fourth dictionary:
        evaluation_instances_topics = evaluations.get(KEY_TOPIC_JSON)
        for key in evaluation_instances_topics.keys():
            if not validate_entry_has_required_keys(
                evaluation_instances_topics[key], KEYS_NEEDED_FOR_TOPIC
            ):
                return None
            
        #Final validation of contents once structure is secured
        if not validate_entry_can_be_loaded(
            evaluations, 'evaluations'
        ):
            return None
        
        
    #After all it's validated, can proceed with creation ----------------------
    for course_section in course_sections:
        section_id = course_section.get(KEY_ID_ENTRY)
        evaluations = course_section.get(KEY_EVALUATION_JSON)
        evaluation_instances = evaluations.get(KEY_TOPIC_COMBINATION_JSON)
        evaluation_instances_topics = evaluations.get(KEY_TOPIC_JSON)

        # overall_ponderation_type is required to have the name of the type 
        # with the first letter capitalized.
        overall_ponderation_type = capitalize_first_character(
            evaluations.get('tipo')
        ) 

        course_section_data = (
            transform_json_entry_into_processable_course_sections_format(
                course_section, overall_ponderation_type, section_id
            )
        )

        if check_if_course_section_with_id_exists(section_id): 
            handle_course_section_with_existing_id(section_id)

        create_section(course_section_data)

        add_evaluation_topics_and_evaluations_to_section(
            section_id, evaluation_instances, evaluation_instances_topics
        )

    db.session.commit()

def transform_json_entry_into_processable_course_sections_format(
    course_section, overall_ponderation_type, section_id
):
    data = {
        'section_id' : section_id,
        'nrc' : str(section_id),  
        'overall_ponderation_type': overall_ponderation_type,
        'course_instance_id' : course_section.get('instancia_curso'),
        'teacher_id' : course_section.get('profesor_id'),
        'state' : 'Open' #As default, since isn't given in JSON files and assumed to be Open.
    }
    return(data)

def check_if_course_section_with_id_exists(id):
    course_section = CourseSection.query.filter_by(id=id).first()
    if course_section:
        return True
    else:
        return False

def handle_course_section_with_existing_id(id):
    course_section = CourseSection.query.filter_by(id=id).first()
    max_id = db.session.query(func.max(CourseSection.id)).scalar() or 0
    new_id = max_id + 1

    course_section.id = new_id
    db.session.commit()

def capitalize_first_character(text):
    if not text:
        return text
    return text[0].upper() + text[1:]

def add_evaluation_topics_and_evaluations_to_section(
    id, evaluation_instances, evaluation_instances_topics
):
    """
    Due to the nature of multiple values in a topic, it's not possible to 
    refactor this function further to make it more readable / simple. 
    So, the following comments are to separate into chunks to make it
    more readable.
    """
    for evaluation_instance in evaluation_instances:
        evaluation_instance_id = evaluation_instance.get('id')
        topic = evaluation_instances_topics.get(str(evaluation_instance_id))
        evaluation_instance_data = (
            transform_json_entry_into_processable_evaluation_type_format(
                id, evaluation_instance, evaluation_instance_id,topic
            )
        )

        create_evaluation_type(evaluation_instance_data)

        # Prepare the data for instanciating an evaluation on a topic.
        topic = evaluation_instances_topics.get(str(evaluation_instance_id))
        evaluation_values = topic.get('valores')
        evaluation_id = topic.get('id')
        is_evaluation_required_list = topic.get('obligatorias')

        # Cycling through values / ponderations on each instance of a topic to 
        # create each one specifically.
        for valor, is_evaluation_required in zip(
            evaluation_values, is_evaluation_required_list
        ):
            # Formating the data.
            processable_data_format_for_evaluation = {
                'evaluation_id' : evaluation_id,
                'evaluation_type_id' : evaluation_instance_id,
                'name' : 'placeholder',
                'ponderation' : valor,
                'optional' : str(is_evaluation_required).lower() == 'false'
            }
            
            # Creating the evaluation.
            create_evaluation(processable_data_format_for_evaluation)

def transform_json_entry_into_processable_evaluation_type_format(
    id, evaluation_instance, evaluation_instance_id,topic
):
    evaluation_instance_name = evaluation_instance.get('nombre')
    evaluation_ponderation = evaluation_instance.get('valor')
    data = {
        'ponderation_type' : capitalize_first_character(topic.get('tipo')),
        'topic' : evaluation_instance_name,
        'overall_ponderation' : evaluation_ponderation,
        'course_section_id' : id,
        'evaluation_instance_id' : evaluation_instance_id
    }

    return data

def has_section_been_closed(old_state, new_state):
    """Returns True if state went from 'Open' to 'Closed'"""
    return old_state == 'Open' and new_state == 'Closed'

def close_all_sections_for_course(course_id):
    course_instances = CourseInstance.query.filter_by(course_id=course_id).all()

    for course_instance in course_instances:
        course_sections = get_all_course_sections(course_instance.id)

        for section in course_sections:
            if section.state == 'Open':
                section.state = 'Closed'
                db.session.commit()
                calculate_final_grades(section)

def export_section_report_to_excel(course_section):
    if course_section.state == 'Open':
        return None

    data = generate_section_report(course_section)
    excel_buffer = convert_data_to_excel(data)

    if excel_buffer is None:
        return None

    filename = f'{course_section.nrc}_reporte_notas.xlsx'
    return excel_buffer, filename


def generate_section_report(course_section):
    student_courses = course_section.student_courses

    data = []
    for course in student_courses:
        student = course.student
        student_name = f'{student.first_name} {student.last_name}'
        final_grade = (
            course.final_grade if course.final_grade is not None else 'N/A'
        )
        state = course.state

        data.append({
            'Estudiante': student_name,
            'Email': student.email,
            'Nota Final': final_grade,
            'Estado': state
        })
    
    return sorted(data, key=lambda r: (r['Estudiante']))

def convert_data_to_excel(data):
    if not data:
        return None

    dataframe = pd.DataFrame(data, columns=REPORT_COLUMNS)
    excel_buffer = BytesIO()
    dataframe.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)

    return excel_buffer
