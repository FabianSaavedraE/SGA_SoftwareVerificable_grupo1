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

    new_course = Course(
        name = data.get('name'),
        description = data.get('description'),
        code = code,
        credits=credits
    )
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
    raw_code = data.get('code', '').zfill(CODE_LENGTH)
    return f"ICC{raw_code}"

def create_courses_from_json(data):   
    courses = data.get('cursos', [])
    for course in courses:
        id = course.get('id')
        name = course.get('descripcion')
        description = name #This it's defined in our model, but doesn't seem to be necessary according to the JSON.
        #So I will keep it as a duplicate, since it would be usefull to have anyways
        code = course.get('codigo')
        credits = int(course.get('creditos'))
        prerequisites = course.get('requisitos')
       
        if check_if_course_with_id_exists(id): 
            handle_course_with_existing_id(id)
        
        new_course = Course(
            id = id,
            name=name,
            description=description,
            code=code,
            credits=credits
        )
        db.session.add(new_course)

        generate_prerequisites(id, prerequisites)

    db.session.commit()


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
        #processable_data = {'course_id' : id, 'prerequisite_id' : prerequisite_id}
        create_course_prerequisite(id, prerequisite_id)
