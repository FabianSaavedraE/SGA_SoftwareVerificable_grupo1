from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models.student_evaluation import StudentEvaluations
from app.controllers.student_evaluation_controller import createStudentEvaluation, getStudentEvaluation, updateStudentEvaluation
from app.controllers.evaluation_controller import getEvaluation
from app.controllers.student_controller import getAllStudents

from app import db

student_evaluation_bp = Blueprint('student_evaluations', __name__, url_prefix='/student_evaluations')

@student_evaluation_bp.route('/create/<int:evaluation_id', methods=['GET', 'POST'])
def createStudentEvaluationView(evaluation_id):
    evaluation = getEvaluation(evaluation_id)
    students = getAllStudents()
    
    if not evaluation:
        return redirect(url_for('evaluations.showEvaluationView', evaluation_id=evaluation_id))
    
    if request.method == 'POST':
        data = request.form.to_dict()
        data['evaluation_id'] = evaluation_id
        createStudentEvaluation(data)
        return redirect(url_for('student_evaluations.createStudentEvaluationView', evaluation_id=evaluation_id))
    
    return render_template('student_evaluations/create.html', evaluation=evaluation, students=students)

def updateStudentEvaluationView(student_id, evaluation_id):
    student_evaluation = getStudentEvaluation(student_id, evaluation_id)
    if not student_evaluation:
        return redirect(url_for('evaluations.showEvaluationView', evaluation_id=evaluation_id))

    if request.method == 'POST':
        data = request.form
        updateStudentEvaluation(student_evaluation, data)

        return redirect(url_for('evaluations.showEvaluationView', evaluation_id=evaluation_id))

    return render_template('student_evaluations/edit.html', student_evaluation=student_evaluation)