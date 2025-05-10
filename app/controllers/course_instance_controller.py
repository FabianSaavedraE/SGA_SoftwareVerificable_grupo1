from app import db
from app.models.course_instance import CourseInstance

def get_all_course_instances():
    course_instances = CourseInstance.query.all()
    return course_instances

def get_course_instance(course_instance_id):
    course_instance = CourseInstance.query.get(course_instance_id)
    return course_instance

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
