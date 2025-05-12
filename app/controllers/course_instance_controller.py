from datetime import datetime

from app import db
from app.models.course_instance import CourseInstance

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
    year = int(data.get('year'))
    semester = int(data.get('semester'))

    if not is_valid_year(year):
        return None
    
    exists = CourseInstance.query.filter_by(
        course_id=data['course_id'],
        year=year,
        semester=semester
    ).first()
    if exists:
        return None
    
    new_course_instance = CourseInstance(
        year = year,
        semester = semester,
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

    if not is_valid_year(new_year):
        return None

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

def is_valid_year(year):
    current_year = datetime.now().year
    return MIN_YEAR <= year <= current_year
