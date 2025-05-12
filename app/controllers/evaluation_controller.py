from app import db
from app.models.evaluation import Evaluation
from app.models.evaluation_type import EvaluationType
from sqlalchemy import func

def get_all_evaluations():
    evaluations = Evaluation.query.all()
    return evaluations

def get_evaluations_by_topic(evaluation_type_id):
    evaluations = Evaluation.query.filter_by(
        evaluation_type_id=evaluation_type_id
    ).all()
    return evaluations

def get_evaluation(evaluation_id):
    evaluation = Evaluation.query.get(evaluation_id)
    return evaluation

def create_evaluation(data):
    evaluation_type_id = data.get('evaluation_type_id')
    evaluation_type = EvaluationType.query.get(evaluation_type_id)
    
    evaluation_ponderation = float(data.get('ponderation') or 0)

    if not evaluation_type:
        return None

    if evaluation_type.ponderation_type == 'Porcentaje':
        total = db.session.query(
            func.coalesce(func.sum(Evaluation.ponderation), 0)
        ).filter_by(evaluation_type_id=evaluation_type_id).scalar()
        if total + evaluation_ponderation > 100:
            return None, total

    new_evaluation = Evaluation(
        name = data.get('name'),
        ponderation = evaluation_ponderation,
        optional = data.get('optional', False),
        evaluation_type_id = evaluation_type_id
    )

    db.session.add(new_evaluation)
    db.session.commit()

    return new_evaluation, None

def update_evaluation(evaluation, data):
    if not evaluation:
        return None
    
    new_evaluation_ponderation = float(data.get('ponderation', evaluation.ponderation))
    evaluation_type = evaluation.evaluation_type

    if evaluation_type.ponderation_type == 'Porcentaje':
        total = db.session.query(
            func.coalesce(func.sum(Evaluation.ponderation), 0)
        ).filter(
            Evaluation.evaluation_type_id == evaluation_type.id,
            Evaluation.id != evaluation.id
        ).scalar()
        if total + new_evaluation_ponderation > 100:
            return None, total
    
    evaluation.name = data.get('name', evaluation.name)
    evaluation.ponderation = new_evaluation_ponderation
    evaluation.optional = data.get('optional', evaluation.optional)

    db.session.commit()
    return evaluation, None

def delete_evaluation(evaluation):
    if not evaluation:
        return False

    db.session.delete(evaluation)
    db.session.commit()
    return True
