from app import db
from app.models.evaluation_type import EvaluationType
from app.models.course_section import CourseSection
from sqlalchemy import func

def get_evaluation_types_by_course(course_id):
    evaluation_types = EvaluationType.query.filter_by(course_id=course_id).all()
    return evaluation_types

def get_evaluation_type(evaluation_type_id):
    evaluation_type = EvaluationType.query.get(evaluation_type_id)
    return evaluation_type

def create_evaluation_type(data):
    section_id = data.get('course_section_id')
    evaluation_type_ponderation = float(data.get('overall_ponderation'))
    
    section = CourseSection.query.get(section_id)
    
    if section.overall_ponderation_type == 'Porcentaje':
        current_total_ponderation_value = db.session.query(
            func.coalesce(func.sum(EvaluationType.overall_ponderation), 0)
        ).filter_by(course_section_id=section_id).scalar()
        if current_total_ponderation_value + evaluation_type_ponderation > 100:
            return None, current_total_ponderation_value 
            #current_total_ponderation_value is returned for error showing purposes
        
    new_evaluation_type = EvaluationType(
        topic = data.get('topic'),
        ponderation_type = data.get('ponderation_type'),
        overall_ponderation = evaluation_type_ponderation,
        course_section_id = section_id
    )

    db.session.add(new_evaluation_type)
    db.session.commit()

    return new_evaluation_type, None

def update_evaluation_type(evaluation_type, data):
    if not evaluation_type:
        return None
    
    new_evaluation_type_ponderation = float(data.get('overall_ponderation', evaluation_type.overall_ponderation))
    section_id = evaluation_type.course_section_id
    
    section = CourseSection.query.get(section_id)
    
    if section.overall_ponderation_type == 'Porcentaje':
        # We add up all of them except the current one, plus the new value
        total = db.session.query(
            func.coalesce(func.sum(EvaluationType.overall_ponderation), 0)
        ).filter(
            EvaluationType.course_section_id==section_id,
            EvaluationType.id!=evaluation_type.id
        ).scalar()
        if total + new_evaluation_type_ponderation > 100:
            return None, total

    evaluation_type.topic = data.get('topic', evaluation_type.topic)
    evaluation_type.ponderation_type = data.get(
        'ponderation_type',
        evaluation_type.ponderation_type
    )
    evaluation_type.overall_ponderation = new_evaluation_type_ponderation

    db.session.commit()
    return evaluation_type, None

def delete_evaluation_type(evaluation_type):
    if not evaluation_type:
        return False

    db.session.delete(evaluation_type)
    db.session.commit()
    return True
