from app import db
from app.models.course_instance import CourseInstance
from sqlalchemy import func

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
    exists = CourseInstance.query.filter_by(
        course_id=data['course_id'],
        year=data['year'],
        semester=data['semester']
    ).first()
    if exists:
        return None
    
    new_course_instance = CourseInstance(
        year = data.get('year'),
        semester = data.get('semester'),
        course_id = data.get('course_id')
    )
    db.session.add(new_course_instance)
    db.session.commit()

    return new_course_instance

def update_course_instance(course_instance, data):
    if not course_instance:
        return None
    
    new_year = int(data.get('year', course_instance.year))
    new_semester = int(data.get('semester', course_instance.semester))
    exists = CourseInstance.query.filter_by(
        course_id=course_instance.course_id,
        year=new_year,
        semester=new_semester
    ).filter(CourseInstance.id != course_instance.id).first()
    if exists:
        return None

    course_instance.year = new_year
    course_instance.semester = new_semester

    db.session.commit()
    return course_instance

def delete_course_instance(course_instance):
    if not course_instance:
        return False

    db.session.delete(course_instance)
    db.session.commit()
    return True

def create_course_instances_from_json(data):
    year = data.get('año')
    semester = data.get('semestre')
    instances = data.get('instancias', [])

    for instance in instances:
        instance_id = instance.get('id')
        course_id = instance.get('curso_id')
        
        if check_if_course_instancewith_id_exists(instance_id):
            handle_course_instance_with_existing_id(instance_id)
        
        new_instance = CourseInstance(
            id=instance_id,
            year=year,
            semester=semester,
            course_id=course_id
        )
        db.session.add(new_instance)

    db.session.commit()


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
