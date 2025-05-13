from app import db
from app.models.course import Course
from sqlalchemy import func
from app.controllers.course_prerequisites_controllers import create_course_prerequisite

CODE_LENGTH = 4

def get_all_courses():
    courses = Course.query.all()
    return courses

def get_course(course_id):
    course = Course.query.get(course_id)
    return course

def create_course(data):
    credits = int(data.get('credits', 0))
    code = transform_code_to_valid_format(data)
    course_id = data.get('course_id')

    new_course = Course(
        name = data.get('name'),
        description = data.get('description'),
        code = code,
        credits=credits
    )

    if course_id is not None:
        new_course.id = course_id

    db.session.add(new_course)
    db.session.commit()

    return new_course

def update_course(course, data):
    if not course:
        return None

    raw_code = data.get('code', str(course.code)[CODE_LENGTH:])
    full_code = f"ICC{raw_code.zfill(CODE_LENGTH)}"

    course.name = data.get('name', course.name)
    course.description = data.get('description', course.description)
    course.code = full_code
    course.credits = data.get('credits', course.credits)

    db.session.commit()
    return course

def delete_course(course):
    if not course:
        return False

    db.session.delete(course)
    db.session.commit()
    return True

def transform_code_to_valid_format(data):
    raw_code = data.get('code', '')
    if raw_code.startswith('ICC'):
        return raw_code
    raw_code = raw_code.zfill(CODE_LENGTH)
    return f"ICC{raw_code}"

def create_courses_from_json(data):   
    courses = data.get('cursos', [])
    for course in courses:
        id = course.get('id')
        prerequisites = course.get('requisitos')
        
        course_data = transform_json_entry_into_processable_course_format(course)
       
        if check_if_course_with_id_exists(id): 
            handle_course_with_existing_id(id)
        
        create_course(course_data)

        if prerequisites != []:
            generate_prerequisites(id, prerequisites)

    db.session.commit()

def transform_json_entry_into_processable_course_format(course):
    data = {
            'name' : course.get('descripcion'),
            'description' : course.get('descripcion'),#Simply a duplication, not required technically but added in our model.
            'code' : course.get('codigo'),
            'credits' : course.get('creditos'),
            'course_id' : course.get('id')
    }
    return data

def check_if_course_with_id_exists(id):
    course = Course.query.filter_by(id=id).first()
    if course:
        return True
    else:
        return False
    
def handle_course_with_existing_id(id):
    course = Course.query.filter_by(id=id).first()
    max_id = db.session.query(func.max(Course.id)).scalar() or 0
    new_id = max_id + 1

    course.id = new_id
    db.session.commit()

def generate_prerequisites(id, prerequisites):
    for prerequisite in prerequisites:
        course = Course.query.filter_by(code = prerequisite).first()
        prerequisite_id = course.id
        create_course_prerequisite(id, prerequisite_id)
