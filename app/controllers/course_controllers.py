from app.models.course import Course
from app import db

def getAllCourses():
    courses = Course.query.all()
    return [serializeCourse(s) for s in courses]

def getCourse(course_id):
    course = Course.query.get(course_id)
    return course

def createCourse(data):
    new_course = Course(
        name = data.get('name')
    )
    db.session.add(new_course)
    db.session.commit()

    return serializeCourse(new_course)

def updateCourse(course, data):
    if not course:
        return None

    course.name = data.get('name', course.name)

    db.session.commit()
    return serializeCourse(course)

def deleteCourse(course):
    if not course:
        return False

    db.session.delete(course)
    db.session.commit()
    return True

def serializeCourse(course):
    return {
        "id": course.id,
        "name": course.name,
    }