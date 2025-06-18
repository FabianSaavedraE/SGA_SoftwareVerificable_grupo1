from app import db
from app.models import CoursePrerequisite


def get_all_course_prerequisites():
    """Get all course prerequisites."""
    return CoursePrerequisite.query.all()


def get_course_prerequisite(course_id, prerequisite_id):
    """Get a specific course prerequisite."""
    return CoursePrerequisite.query.filter_by(
        course_id=course_id, prerequisite_id=prerequisite_id
    ).first()


def get_prerequisites_by_course(course_id):
    """Get all prerequisites for a course."""
    return CoursePrerequisite.query.filter_by(course_id=course_id).all()


def create_course_prerequisite(course_id, prerequisite_id):
    """Create one course prerequisite."""
    new_prerequisite = CoursePrerequisite(
        course_id=course_id, prerequisite_id=prerequisite_id
    )
    db.session.add(new_prerequisite)
    db.session.commit()


def create_course_prerequisites(course_id, prerequisite_ids):
    """Create multiple course prerequisites."""
    for prerequisite_id in prerequisite_ids:
        new_prerequisite = CoursePrerequisite(
            course_id=course_id, prerequisite_id=prerequisite_id
        )
        db.session.add(new_prerequisite)

    db.session.commit()


def update_course_prerequisite(course_id, prerequisite_id, data):
    """Update a course prerequisite."""
    prerequisite = get_course_prerequisite(course_id, prerequisite_id)
    if prerequisite:
        prerequisite.course_id = data.get("course_id", prerequisite.course_id)
        prerequisite.prerequisite_id = data.get(
            "prerequisite_id", prerequisite.prerequisite_id
        )
        db.session.commit()


def delete_course_prerequisite(course_id, prerequisite_id):
    """Delete a course prerequisite."""
    prerequisite = get_course_prerequisite(course_id, prerequisite_id)
    if prerequisite:
        db.session.delete(prerequisite)
        db.session.commit()
