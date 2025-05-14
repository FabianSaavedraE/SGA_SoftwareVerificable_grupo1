from sqlalchemy import func

from app import db
from app.models import CourseSection
from app.controllers.evaluation_type_controller import create_evaluation_type
from app.controllers.evaluation_controller import create_evaluation
from app.controllers.course_instance_controller import (
    get_course_instance_by_parameters
)

NRC_LENGTH = 4

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
    return course_section

def delete_section(course_section):
    if not course_section:
        return False

    db.session.delete(course_section)
    db.session.commit()
    return True

def create_course_sections_from_json(data): 
    course_sections = data.get('secciones', [])
    for course_section in course_sections:
        section_id = course_section.get('id')
        evaluations = course_section.get('evaluacion')
        evaluation_instances = evaluations.get('combinacion_topicos')
        evaluation_instances_topics = evaluations.get('topicos')

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
