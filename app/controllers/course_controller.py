from app import db
from app.models.course import Course

def get_all_courses():
    courses = Course.query.all()
    return courses

def get_course(course_id):
    course = Course.query.get(course_id)
    return course

def create_course(data):
    credits = int(data.get('credits', 0))
    code = transform_code_to_valid_format(data)

    new_course = Course(
        name = data.get('name'),
        description = data.get('description'),
        code = code,
        credits=credits
    )
    db.session.add(new_course)
    db.session.commit()

    return new_course

def update_course(course, data):
    if not course:
        return None

    raw_code = data.get('code', str(course.code)[4:])
    full_code = f"ICC-{raw_code.zfill(4)}"

    course.name = data.get('name', course.name)
    course.description = data.get('description', course.description)
    course.code = full_code
    course.credits = data.get('credits', course.credits)

    db.session.commit()
    return course

def delete_course(course):
    if not course:
        return False

    db.session.delete(course)
    db.session.commit()
    return True

def transform_code_to_valid_format(data):
    raw_code = data.get('code', '').zfill(4)
    return f"ICC-{raw_code}"
