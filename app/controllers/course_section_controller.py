from app.models.course_section import CourseSection
from app import db

def getAllSections():
    sections = CourseSection.query.all()
    return [serializeCourseSection(s) for s in sections]

def getAllCourseSections(course_id):
    sections = CourseSection.query.find_by(course_id=course_id).all()
    return [serializeCourseSection(s) for s in sections]

def getSection(course_section_id):
    course_section = CourseSection.query.get(course_section_id)
    return course_section

def createSection(data):
    new_section = CourseSection(
        nrc = data.get('nrc'),
        semester = data.get('semester'),
        course_id = data.get('course_id'),
        teacher_id = data.get('teacher_id')
    )
    db.session.add(new_section)
    db.session.commit()

    return serializeCourseSection(new_section)

def updateSection(course_section, data):
    if not course_section:
        return None

    course_section.nrc = data.get('nrc', course_section.nrc)
    course_section.semester = data.get('semester', course_section.semester)
    course_section.teacher_id = data.get('teacher_id', course_section.teacher_id)

    db.session.commit()
    return serializeCourseSection(course_section)

def serializeCourseSection(course_section):
    return {
        "id": course_section.id,
        "nrc": course_section.nrc,
        "semester": course_section.semester,
        "course_id": course_section.course_id,
        "teacher_id": course_section.teacher_id
    }
    