from app import db
from app.models.course_prerequisite import CoursePrerequisite

def get_all_course_prerequisites():
    return CoursePrerequisite.query.all()


def get_course_prerequisite(course_id, prerequisite_id):
    return CoursePrerequisite.query.filter_by(
        course_id=course_id,
        prerequisite_id=prerequisite_id
    ).first()

def create_course_prerequisites(course_id, prerequisite_ids):
    for prereq_id in prerequisite_ids:
        new_prerequisite = CoursePrerequisite(
            course_id=course_id,
            prerequisite_id=prereq_id
        )
        db.session.add(new_prerequisite)

    db.session.commit()

def update_course_prerequisite(course_id, prerequisite_id, data):
    prerequisite = get_course_prerequisite(course_id, prerequisite_id)
    if prerequisite:
        prerequisite.course_id = data.get('course_id', prerequisite.course_id)
        prerequisite.prerequisite_id = data.get(
            'prerequisite_id',
            prerequisite.prerequisite_id
        )
        db.session.commit()

def delete_course_prerequisite(course_id, prerequisite_id):
    prerequisite = get_course_prerequisite(course_id, prerequisite_id)
    if prerequisite:
        db.session.delete(prerequisite)
        db.session.commit()
