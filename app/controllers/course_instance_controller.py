from datetime import datetime

from app import db
from app.models.course_instance import CourseInstance
from sqlalchemy import func

MIN_YEAR = 1980

def get_all_course_instances():
    course_instances = CourseInstance.query.all()
    return course_instances

def get_course_instance(course_instance_id):
    course_instance = CourseInstance.query.get(course_instance_id)
    return course_instance

def get_course_instance_by_parameters(year, semester):
    course_instances = CourseInstance.query.filter_by(
        year=year, semester=semester
    ).all()

    return course_instances

def create_course_instance(data):
    instance_id = data.get('instance_id')
    new_course_instance = CourseInstance(
        year = data.get('year'),
        semester = data.get('semester'),
        course_id = data.get('course_id')
    )
    db.session.add(new_course_instance)
    db.session.commit()

    if instance_id is not None:
        new_course_instance.id = instance_id

    return new_course_instance

def update_course_instance(course_instance, data):
    if not course_instance:
        return None

    course_instance.year = data.get('year', course_instance.year)
    course_instance.semester = data.get('semester', course_instance.semester)

    db.session.commit()
    return course_instance

def delete_course_instance(course_instance):
    if not course_instance:
        return False

    db.session.delete(course_instance)
    db.session.commit()
    return True

def validate_course_instance(data, course_instance_id=None):
    errors = {}

    year = (data.get('year') or '').strip()
    semester = (data.get('semester') or '').strip()
    course_id = data.get('course_id')

    if not course_id and course_instance_id:
        course_instance = get_course_instance(course_instance_id)
        if course_instance:
            course_id = course_instance.course_id

    if not year:
        errors['year'] = "El año es obligatorio."
    elif not is_valid_year(year):
        errors['year'] = (f"El año debe estar entre {MIN_YEAR} y "
                          f"{datetime.now().year}")

    if not semester:
        errors['semester'] = "El semestre es obligatorio."

    if not errors.get('year') and not errors.get('semester') and course_id:
        existing_instance = CourseInstance.query.filter_by(
            course_id=course_id,
            year=year,
            semester=semester
        ).filter(CourseInstance.id != course_instance_id).first()

        if existing_instance:
            errors['exists'] = (f"Ya existe una instancia de este curso para "
                                f"{year}-{semester}.")

    return errors

def is_valid_year(year):
    current_year = datetime.now().year
    return MIN_YEAR <= int(year) <= int(current_year)

def create_course_instances_from_json(data):
    year = data.get('año')
    semester = data.get('semestre')
    instances = data.get('instancias', [])

    for instance in instances:
        instance_id = instance.get('id')
        instance_data = transform_json_entry_into_processable_course_instance_format(year, semester, instance)
        
        if check_if_course_instancewith_id_exists(instance_id):
            handle_course_instance_with_existing_id(instance_id)
        
        create_course_instance(instance_data)
        
    
def transform_json_entry_into_processable_course_instance_format(year, semester, instance):
    data = {
        'year' : year,
        'semester' : semester,
        'instance_id' : instance.get('id'),
        'course_id' : instance.get('curso_id')
    }
    return(data)

def check_if_course_instancewith_id_exists(id):
    course_instance = CourseInstance.query.filter_by(id=id).first()
    if course_instance:
        return True
    else:
        return False
    
def handle_course_instance_with_existing_id(id):
    course_instance = CourseInstance.query.filter_by(id=id).first()
    max_id = db.session.query(func.max(CourseInstance.id)).scalar() or 0
    new_id = max_id + 1

    course_instance.id = new_id
    db.session.commit()
