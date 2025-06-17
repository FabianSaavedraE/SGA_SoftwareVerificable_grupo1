from sqlalchemy import func

from app import db
from app.models import CourseInstance

from app.validators.data_load_validators import (
    validate_json_has_required_key,
    validate_entry_can_be_loaded,
    validate_entry_has_required_keys
    )
from app.validators.constants import (
    KEY_INSTANCE_JSON, KEY_SEMESTER_JSON, KEY_YEAR_JSON,
    KEY_COURSE_ID_JSON, KEY_ID_ENTRY
)

KEYS_NEEDED_FOR_INSTANCE_JSON = (
    [KEY_INSTANCE_JSON, KEY_SEMESTER_JSON, KEY_YEAR_JSON]
)
KEYS_NEEDED_FOR_INSTANCE_ENTRY=(
    [KEY_COURSE_ID_JSON, KEY_ID_ENTRY]
)
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

def create_course_instances_from_json(data):

    if not validate_entry_has_required_keys(
        data, KEYS_NEEDED_FOR_INSTANCE_JSON
    ):
        return None
    
    year = data.get(KEY_YEAR_JSON)
    semester = data.get(KEY_SEMESTER_JSON)
    instances = data.get(KEY_INSTANCE_JSON, [])

    #First cicle, checks validations ------------------------------------------
    for instance in instances:

        if not validate_entry_has_required_keys(
            instance, KEYS_NEEDED_FOR_INSTANCE_ENTRY
            ):
            return None
        
        is_instance_valid = validate_entry_can_be_loaded(
            transform_json_entry_into_processable_course_instance_format(
                year, semester, instance), 'instance'
        )

        if not is_instance_valid:
            return None
        
    #Second cicle, after validation of every entry creates -------------------- 
    for instance in instances:

        instance_data = (
            transform_json_entry_into_processable_course_instance_format(
                year, semester, instance)
            )
        
        if check_if_course_instance_with_id_exists(instance_id):
            handle_course_instance_with_existing_id(instance_id)
        
        create_course_instance(instance_data)
        
def transform_json_entry_into_processable_course_instance_format(
    year, semester, instance
):
    data = {
        'year' : year,
        'semester' : semester,
        'instance_id' : instance.get('id'),
        'course_id' : instance.get('curso_id')
    }
    return(data)

def check_if_course_instance_with_id_exists(id):
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
