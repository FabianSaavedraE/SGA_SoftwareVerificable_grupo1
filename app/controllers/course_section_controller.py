from app import db
from app.models.course_section import CourseSection
from app.models.teacher import Teacher
from app.controllers.course_instance_controller import (
    get_course_instance_by_parameters
)
from sqlalchemy import func

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
    new_section = CourseSection(
        nrc = data.get('nrc'),
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

    course_section.nrc = data.get('nrc', course_section.nrc)
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
        id = course_section.get('id')
        course_instance_id = course_section.get('instancia_curso')
        nrc = "ICC" + str(id)
        evaluaciones = course_section.get('evaluacion')
        overall_ponderation_type = capitalize_first_character(evaluaciones.get('tipo')) #It's required to have the name of the
        #ponderation type capitalized as part of the format implemented by ourselves.
        state = "Open" #As default, since isn't given in JSON files.
        teacher_id = course_section.get('profesor_id')
    
        teacher = Teacher.query.filter_by(id=teacher_id).first()
        print(f"TEACHER FOUND!: {teacher} searching for {teacher_id}")
     
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
