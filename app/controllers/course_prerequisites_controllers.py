from app import db
from app.models.course_prerequisite import CoursePrerequisite

def getAllCoursePrerequisites():
    return CoursePrerequisite.query.all()


def getCoursePrerequisite(course_id, prerequisite_id):
    return CoursePrerequisite.query.filter_by(course_id=course_id, prerequisite_id=prerequisite_id).first()

def createCoursePrerequisite(data):
    course_id = data.get('course_id')
    prerequisite_id = data.get('prerequisite_id')

    new_prerequisite = CoursePrerequisite(course_id=course_id, prerequisite_id=prerequisite_id)
    db.session.add(new_prerequisite)
    db.session.commit()

def updateCoursePrerequisite(course_id, prerequisite_id, data):
    prerequisite = getCoursePrerequisite(course_id, prerequisite_id)
    if prerequisite:
        prerequisite.course_id = data.get('course_id', prerequisite.course_id)
        prerequisite.prerequisite_id = data.get('prerequisite_id', prerequisite.prerequisite_id)
        db.session.commit()

def deleteCoursePrerequisite(course_id, prerequisite_id):
    prerequisite = getCoursePrerequisite(course_id, prerequisite_id)
    print(prerequisite)
    if prerequisite:
        db.session.delete(prerequisite)
        db.session.commit()
