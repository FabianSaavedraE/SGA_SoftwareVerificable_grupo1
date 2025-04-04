from app.models.course import Course
from app import db

def getAllCourses():
    courses = Course.query.all()
    return [serializeCourse(s) for s in courses]

def serializeCourse(course):
    return {
        "id": course.id,
        "name": course.name,
    }