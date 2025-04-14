from app.models.course_instance import CourseInstance
from app import db

def getAllCourseInstances():
    course_instances = CourseInstance.query.all()
    return course_instances

def getCourseInstance(course_instance_id):
    course_instance = CourseInstance.query.get(course_instance_id)
    return course_instance

def createCourseInstance(data):
    new_course_instance = CourseInstance(
        year = data.get('year'),
        semester = data.get('semester'),
        course_id = data.get('course_id')
    )
    db.session.add(new_course_instance)
    db.session.commit()

    return new_course_instance

def updateCourseInstance(course_instance, data):
    if not course_instance:
        return None
    
    course_instance.year = data.get('year', course_instance.year)
    course_instance.semester = data.get('semester', course_instance.semester)

    db.session.commit()
    return course_instance

def deleteCourseInstance(course_instance):
    if not course_instance:
        return False
    
    db.session.delete(course_instance)
    db.session.commit()
    return True