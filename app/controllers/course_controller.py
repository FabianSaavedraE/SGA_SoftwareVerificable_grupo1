from app import db
from app.models.course import Course

def get_all_courses():
    courses = Course.query.all()
    return courses

def get_course(course_id):
    course = Course.query.get(course_id)
    return course

def create_course(data):
    new_course = Course(
        name = data.get('name'),
        description = data.get('description'),
        code = data.get('code')
    )
    db.session.add(new_course)
    db.session.commit()

    return new_course

def update_course(course, data):
    if not course:
        return None

    course.name = data.get('name', course.name)
    course.description = data.get("description", course.description)
    course.code = data.get("code", course.code)

    db.session.commit()
    return course

def delete_course(course):
    if not course:
        return False

    db.session.delete(course)
    db.session.commit()
    return True
