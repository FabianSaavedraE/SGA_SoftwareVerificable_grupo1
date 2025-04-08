from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.models.student_evaluation import StudentEvaluations
from app.controllers.student_evaluation_controller import createStudentEvaluation, getStudentEvaluation, updateStudentEvaluation
from app.controllers.evaluation_controller import getEvaluation
from app.controllers.student_controller import getStudent

from app import db

student_evaluation_bp = Blueprint('student_evaluations', __name__, url_prefix='/student_evaluations')

@student_evaluation_bp.route('/create/<int:evaluation_id>/<int:student_id>', methods=['GET', 'POST'])
def createStudentEvaluationView(student_id, evaluation_id):
    evaluation = getEvaluation(evaluation_id)
    student = getStudent(student_id)
    student_evaluation = getStudentEvaluation(student_id, evaluation_id)
    
    if not evaluation or not student:
        return redirect(url_for('evaluations.indexView'))
    
    if request.method == 'POST':
        data = request.form.to_dict()
        data['evaluation_id'] = evaluation_id
        data['student_id'] = student_id
        createStudentEvaluation(data)
        return redirect(url_for('evaluations.showEvaluationView', evaluation_id=evaluation_id))
    
    return render_template('student_evaluations/create.html', evaluation=evaluation, student=student, student_evaluation=student_evaluation)

@student_evaluation_bp.route('/update/<int:student_id>/<int:evaluation_id>', methods=['GET', 'POST'])
def updateStudentEvaluationView(student_id, evaluation_id):
    student_evaluation = getStudentEvaluation(student_id, evaluation_id)
    evaluation = getEvaluation(evaluation_id)
    student = getStudent(student_id)
    
    if not student_evaluation:
        return redirect(url_for('evaluations.showEvaluationView', evaluation_id=evaluation_id))

    if request.method == 'POST':
        data = request.form
        updateStudentEvaluation(student_evaluation, data)

        return redirect(url_for('evaluations.showEvaluationView', evaluation_id=evaluation_id))

    return render_template('student_evaluations/edit.html', student_evaluation=student_evaluation, student=student, evaluation=evaluation)