from app.models.evaluation_type import EvaluationType
from app import db

def getEvaluationTypesByCourse(course_id):
    evaluation_types = EvaluationType.query.find_by(course_id=course_id).all()
    return evaluation_types

def getEvaluationType(evaluation_type_id):
    evaluation_type = EvaluationType.query.get(evaluation_type_id)
    return evaluation_type

def createEvaluationType(data):
    new_evaluation_type = EvaluationType(
        topic = data.get('topic'),
        ponderation_type = data.get('ponderation_type'),
        overall_ponderation = data.get('overall_ponderation'),
        course_section_id = data.get('course_section_id')
    )

    db.session.add(new_evaluation_type)
    db.session.commit()

    return new_evaluation_type

def updateEvaluationType(evaluation_type, data):
    if not evaluation_type:
        return None

    evaluation_type.topic = data.get('topic', evaluation_type.topic)
    evaluation_type.ponderation_type = data.get('ponderation_type', evaluation_type.ponderation_type)
    evaluation_type.overall_ponderation = data.get('overall_ponderation', evaluation_type.overall_ponderation)

    db.session.commit()
    return evaluation_type
