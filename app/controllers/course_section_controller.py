from app.models.course_section import CourseSection
from app.models.student_course import StudentCourses
from app import db
from app.controllers.student_course_controller import deleteStudentCourse

def getAllSections():
    sections = CourseSection.query.all()
    return sections

def getAllCourseSections(course_instance_id):
    sections = CourseSection.query.find_by(course_instance_id=course_instance_id).all()
    return sections

def getSection(course_section_id):
    course_section = CourseSection.query.get(course_section_id)
    return course_section

def createSection(data):
    new_section = CourseSection(
        nrc = data.get('nrc'),
        overall_ponderation_type = data.get('overall_ponderation_type'),
        course_instance_id = data.get('course_instance_id'),
        teacher_id = data.get('teacher_id')
    )
    db.session.add(new_section)
    db.session.commit()

    return new_section

def updateSection(course_section, data):
    if not course_section:
        return None

    course_section.nrc = data.get('nrc', course_section.nrc)
    course_section.overall_ponderation_type = data.get('overall_ponderation_type', course_section.overall_ponderation_type)
    course_section.teacher_id = data.get('teacher_id', course_section.teacher_id)

    db.session.commit()
    return course_section

def deleteSection(course_section_id):
    course_section = getSection(course_section_id)
    
    if course_section:
        db.session.delete(course_section)
        db.session.commit()
        return True
    return False

    