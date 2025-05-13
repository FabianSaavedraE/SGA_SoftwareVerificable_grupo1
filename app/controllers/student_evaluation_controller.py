from app import db
from app.models import StudentEvaluations, Evaluation

def get_student_evaluation(student_id, evaluation_id):
    student_evaluation = StudentEvaluations.query.get(
        (student_id, evaluation_id)
    )
    return student_evaluation

def create_student_evaluation(data):
    new_student_evaluation = StudentEvaluations(
        student_id = data.get('student_id'),
        evaluation_id = data.get('evaluation_id'),
        grade = data.get('grade')
    )
    db.session.add(new_student_evaluation)
    db.session.commit()

    return new_student_evaluation

def update_student_evaluation(student_evaluation, data):
    if not student_evaluation:
        return None

    student_evaluation.grade = data.get('grade', student_evaluation.grade)

    db.session.commit()
    return student_evaluation

def create_student_evaluation_json(data):
    student_evaluations = data.get('notas', [])
    for student_evaluation in student_evaluations:
        student_id = student_evaluation.get('alumno_id')
        evaluation_type_id = student_evaluation.get('topico_id')
        instance = student_evaluation.get('instancia')
        grade = student_evaluation.get('nota')
        evaluation_id = get_evaluation_id_by_topic_and_instance(
            evaluation_type_id, instance
        )
        
        new_student_evaluation = StudentEvaluations(
          student_id = student_id,
          evaluation_id = evaluation_id,
          grade = grade
        )
        db.session.add(new_student_evaluation)
    db.session.commit()

def get_evaluation_id_by_topic_and_instance(evaluation_type_id, instance):
    evaluations = Evaluation.query.filter_by(
        evaluation_type_id=evaluation_type_id
    ).order_by(Evaluation.id).all()
    selected_evaluation_id = evaluations[instance - 1].id
    return selected_evaluation_id
