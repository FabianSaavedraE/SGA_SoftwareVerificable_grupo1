from app import db
from app.models.course_section import CourseSection
from app.models.teacher import Teacher
from app.controllers.course_instance_controller import (
    get_course_instance_by_parameters
)
from app.controllers.evaluation_type_controller import (
    create_evaluation_type
)
from app.controllers.evaluation_controller import(
    create_evaluation
)

from sqlalchemy import func

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
    nrc = f"NRC{raw_nrc}"

    new_section = CourseSection(
        nrc = nrc,
        overall_ponderation_type = data.get('overall_ponderation_type'),
        course_instance_id = data.get('course_instance_id'),
        teacher_id = data.get('teacher_id') or None,
        state = data.get('state', 'Open')
    )
    db.session.add(new_section)
    db.session.commit()

    return new_section

def update_section(course_section, data):
    if not course_section:
        return None
    
    
    raw_nrc = data.get('nrc', str(course_section.nrc)[NRC_LENGTH:])
    print("RAW NRC:", raw_nrc)



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

def data_validation(data, course_section_id=None):
    errors = {}

    nrc = (data.get('nrc') or '').strip()

    if not nrc:
        errors['nrc'] = "El NRC es obligatorio."
    elif len(nrc) != NRC_LENGTH:
        errors['nrc'] = (f"El NRC debe ser un número de {NRC_LENGTH} dígitos.")
    else:
        existing_section = CourseSection.query.filter_by(
            nrc=f"NRC{nrc}"
        ).first()

        if existing_section and (
            course_section_id is None or
            existing_section.id != course_section_id
        ):
            errors['nrc'] = f"El NRC ({nrc}) ya está en uso por otra sección."

    return errors

def create_course_sections_from_json(data):   
    course_sections = data.get('secciones', [])
    for course_section in course_sections:
        id = course_section.get('id')
        course_instance_id = course_section.get('instancia_curso')
        nrc = f"NRC{str(id).zfill(NRC_LENGTH)}"
        evaluations = course_section.get('evaluacion')
        evaluation_instances = evaluations.get('combinacion_topicos')
        evaluation_instances_topics = evaluations.get('topicos')
        overall_ponderation_type = capitalize_first_character(evaluations.get('tipo')) #It's required to have the name of the
        #ponderation type capitalized as part of the format implemented by ourselves.
        state = "Open" #As default, since isn't given in JSON files.
        teacher_id = course_section.get('profesor_id')
    
        if check_if_course_section_with_id_exists(id): 
            handle_course_section_with_existing_id(id)
        
        new_section = CourseSection(
            id=id,
            nrc=nrc,
            overall_ponderation_type=overall_ponderation_type,
            state=state,
            course_instance_id=course_instance_id,
            teacher_id=teacher_id
        )

        db.session.add(new_section)

        add_evaluation_topics_and_evaluations_to_section(id, evaluation_instances, evaluation_instances_topics)
 
    db.session.commit()

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

def add_evaluation_topics_and_evaluations_to_section(id, evaluation_instances, evaluation_instances_topics):
    for evaluation_instance in evaluation_instances:
        evaluation_instance_id = evaluation_instance.get('id')
        evaluation_instance_name = evaluation_instance.get('nombre')
        evaluation_ponderation = evaluation_instance.get('valor')
        topic = evaluation_instances_topics.get(str(evaluation_instance_id))
        processable_data_format_for_evaluation_type = {'ponderation_type' : capitalize_first_character(topic.get('tipo')),
                                   'topic' : evaluation_instance_name,
                                   'overall_ponderation' : evaluation_ponderation,
                                   'course_section_id' : id,
                                   'evaluation_instance_id' : evaluation_instance_id}
        
        create_evaluation_type(processable_data_format_for_evaluation_type)
        evaluation_values = topic.get('valores')
        evaluation_id = topic.get('id')
        is_evaluation_required_list = topic.get('obligatorias')
        for valor, is_evaluation_required in zip(evaluation_values, is_evaluation_required_list):
            processable_data_format_for_evaluation = {'evaluation_id' : evaluation_id,
                                                      'evaluation_type_id' : evaluation_instance_id,
                                                      'name' : 'placeholder',
                                                      'ponderation' : valor,
                                                      'optional' : bool(is_evaluation_required)
                                                      }
            create_evaluation(processable_data_format_for_evaluation)
        pass
