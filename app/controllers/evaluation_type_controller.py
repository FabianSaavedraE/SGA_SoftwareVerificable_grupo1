from app import db
from app.models.evaluation_type import EvaluationType

def get_evaluation_types_by_course(course_id):
    evaluation_types = EvaluationType.query.filter_by(course_id=course_id).all()
    return evaluation_types

def get_evaluation_type(evaluation_type_id):
    evaluation_type = EvaluationType.query.get(evaluation_type_id)
    return evaluation_type

def create_evaluation_type(data):
    new_evaluation_type = EvaluationType(
        topic = data.get('topic'),
        ponderation_type = data.get('ponderation_type'),
        overall_ponderation = data.get('overall_ponderation'),
        course_section_id = data.get('course_section_id')
    )

    db.session.add(new_evaluation_type)
    db.session.commit()

    return new_evaluation_type

def update_evaluation_type(evaluation_type, data):
    if not evaluation_type:
        return None

    evaluation_type.topic = data.get('topic', evaluation_type.topic)
    evaluation_type.ponderation_type = data.get(
        'ponderation_type',
        evaluation_type.ponderation_type
    )
    evaluation_type.overall_ponderation = data.get(
        'overall_ponderation',
        evaluation_type.overall_ponderation
    )

    db.session.commit()
    return evaluation_type

def delete_evaluation_type(evaluation_type):
    if not evaluation_type:
        return False

    db.session.delete(evaluation_type)
    db.session.commit()
    return True
