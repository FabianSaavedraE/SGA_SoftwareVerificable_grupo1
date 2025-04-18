from app.models.evaluation import Evaluation
from app import db

def getAllEvaluations():
    evaluations = Evaluation.query.all()
    return evaluations

def getEvaluationsByTopic(evaluation_type_id):
    evaluations = Evaluation.query.find_by(evaluation_type_id=evaluation_type_id).all()
    return evaluations

def getEvaluation(evaluation_id):
    evaluation = Evaluation.query.get(evaluation_id)
    return evaluation

def createEvaluation(data):
    from app.models.evaluation_type import EvaluationType

    evaluation_type_id = data.get('evaluation_type_id')
    evaluation_type = EvaluationType.query.get(evaluation_type_id)

    if not evaluation_type:
        return None  # Fallback defensivo

    existing_evaluations = Evaluation.query.filter_by(evaluation_type_id=evaluation_type_id).all()
    ponderation = data.get('ponderation')

    if ponderation is '':
        if evaluation_type.ponderation_type == 'Peso':
            ponderation = 1
        elif evaluation_type.ponderation_type == 'Porcentaje':
            total_evaluations_after_creation = len(existing_evaluations) + 1
            ponderation = round(100 / total_evaluations_after_creation, 2)

    new_evaluation = Evaluation(
        name = data.get('name'),
        ponderation = ponderation,
        optional = data.get('optional', False),
        evaluation_type_id = evaluation_type_id
    )

    db.session.add(new_evaluation)
    db.session.commit()

    return new_evaluation
def updateEvaluation(evaluation, data):
    if not evaluation:
        return None
    
    evaluation.name = data.get('name', evaluation.name)
    evaluation.ponderation = data.get('ponderation', evaluation.ponderation)
    evaluation.optional = data.get('optional', evaluation.optional)

    db.session.commit()
    return evaluation

def deleteEvaluation(evaluation):
    if not evaluation:
        return False

    db.session.delete(evaluation)
    db.session.commit()
    return True
