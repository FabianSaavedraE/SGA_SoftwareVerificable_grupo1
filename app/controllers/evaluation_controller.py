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
    new_evaluation = Evaluation(
        name = data.get('name'),
        ponderation_type = data.get('ponderation_type'),
        ponderation = data.get('ponderation'),
        optional = data.get('optional'),
        evaluation_type_id = data.get('evaluation_type_id')
    )
    db.session.add(new_evaluation)
    db.session.commit()

    return new_evaluation

def updateEvaluation(evaluation, data):
    if not evaluation:
        return None
    
    evaluation.name = data.get('name', evaluation.name)
    evaluation.ponderation_type = data.get('ponderation_type', evaluation.ponderation_type)
    evaluation.ponderation = data.get('ponderation', evaluation.ponderation)
    evaluation.optional = data.get('optional', evaluation.optional)

    db.session.commit()
    return evaluation
