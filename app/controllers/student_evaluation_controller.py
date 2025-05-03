from app import db
from app.models.student_evaluation import StudentEvaluations

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
