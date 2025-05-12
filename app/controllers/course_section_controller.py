from app import db
from app.models.course_section import CourseSection

def get_all_sections():
    sections = CourseSection.query.all()
    return sections

def get_all_course_sections(course_instance_id):
    sections = CourseSection.query.find_by(
        course_instance_id=course_instance_id
    ).all()
    return sections

def get_section(course_section_id):
    course_section = CourseSection.query.get(course_section_id)
    return course_section

def create_section(data):
    new_section = CourseSection(
        nrc = data.get('nrc'),
        overall_ponderation_type = data.get('overall_ponderation_type'),
        course_instance_id = data.get('course_instance_id'),
        teacher_id = data.get('teacher_id') or None,
        state = data.get('state', 'Open')
    )
    db.session.add(new_section)
    db.session.commit()

    return new_section

def update_section(course_section, data):
    if not course_section:
        return None

    course_section.nrc = data.get('nrc', course_section.nrc)
    course_section.overall_ponderation_type = data.get(
        'overall_ponderation_type',
        course_section.overall_ponderation_type
    )
    course_section.teacher_id = data.get(
        'teacher_id',
        course_section.teacher_id
    ) or None
    course_section.state = data.get('state', course_section.state)

    db.session.commit()
    return course_section

def delete_section(course_section):
    if not course_section:
        return False

    db.session.delete(course_section)
    db.session.commit()
    return True
