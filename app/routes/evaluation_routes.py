from flask import Blueprint, request, render_template, redirect, url_for
from app.models.evaluation import Evaluation
from app.controllers.evaluation_controller import getAllEvaluations, getEvaluation, createEvaluation, updateEvaluation
from app.controllers.evaluation_type_controller import getEvaluationType
from app import db

evaluation_bp = Blueprint('evaluations', __name__, url_prefix='/evaluations')

@evaluation_bp.route('/create/<int:evaluation_type_id>', methods=['GET', 'POST'])
def createEvaluationView(evaluation_type_id):
    evaluation_type = getEvaluationType(evaluation_type_id)
    if not evaluation_type:
        return redirect(url_for('course_sections.showSectionView', course_section_id=evaluation_type.course_section_id))
    
    if request.method == 'POST':
        data = request.form.to_dict()
        data['evaluation_type_id'] = evaluation_type_id
        createEvaluation(data)
        return redirect(url_for('course_sections.showSectionView', course_section_id=evaluation_type.course_section_id))
    
    return render_template('evaluations/create.html', evaluation_type=evaluation_type)
    
@evaluation_bp.route('/<int:evaluation_id>', methods=['GET', 'POST'])
def updateEvaluationView(evaluation_id):
    evaluation = getEvaluation(evaluation_id)
    if not evaluation:
        return redirect(url_for('course_sections.showSectionView', course_section_id=evaluation.evaluation_type.course_section_id))
    
    if request.method == 'POST':
        data = request.form
        updateEvaluation(evaluation, data)

        return redirect(url_for('course_sections.showSectionView', course_section_id=evaluation.evaluation_type.course_section_id))
    
    return render_template('evaluations/edit.html', evaluation=evaluation)
