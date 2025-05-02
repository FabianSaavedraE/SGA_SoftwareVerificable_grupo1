from flask import Blueprint, request, render_template, redirect, url_for
from app.models.evaluation import Evaluation
from app.controllers.evaluation_controller import get_all_evaluations, get_evaluation, create_evaluation, update_evaluation, delete_evaluation
from app.controllers.evaluation_type_controller import get_evaluation_type
from app.controllers.course_section_controller import get_section
from app import db

evaluation_bp = Blueprint('evaluations', __name__, url_prefix='/evaluations')

@evaluation_bp.route('/create/<int:evaluation_type_id>', methods=['GET', 'POST'])
def create_evaluation_view(evaluation_type_id):
    evaluation_type = get_evaluation_type(evaluation_type_id)
    if not evaluation_type:
        return redirect(url_for('course_sections.show_section_view', course_section_id=evaluation_type.course_section_id))
    
    if request.method == 'POST':
        data = request.form.to_dict()
        data['evaluation_type_id'] = evaluation_type_id
        data['optional'] = request.form.get('optional') == 'on'
        create_evaluation(data)
        return redirect(url_for('course_sections.show_section_view', course_section_id=evaluation_type.course_section_id))
    
    return render_template('evaluations/create.html', evaluation_type=evaluation_type)
    
@evaluation_bp.route('/<int:evaluation_id>', methods=['GET', 'POST'])
def update_evaluation_view(evaluation_id):
    evaluation = get_evaluation(evaluation_id)
    if not evaluation:
        return redirect(url_for('course_sections.show_section_view', course_section_id=evaluation.evaluation_type.course_section_id))
    
    if request.method == 'POST':
        data = request.form.to_dict()
        data['optional'] = request.form.get('optional') == 'on'
        update_evaluation(evaluation, data)

        return redirect(url_for('course_sections.show_section_view', course_section_id=evaluation.evaluation_type.course_section_id))
    
    return render_template('evaluations/edit.html', evaluation=evaluation)

@evaluation_bp.route('/<int:evaluation_id>/show', methods=['GET'])
def show_evaluation_view(evaluation_id):
    evaluation = get_evaluation(evaluation_id)
    if not evaluation:
        return redirect(url_for('home'))

    evaluation_type = get_evaluation_type(evaluation.evaluation_type_id)
    course_section = get_section(evaluation_type.course_section_id)
    students = course_section.student_courses

    grades = {
        (student_evaluation.student_id): student_evaluation.grade
        for student_evaluation in evaluation.student_evaluations
    }

    return render_template(
        'evaluations/show.html',
        evaluation=evaluation,
        evaluation_type=evaluation_type,
        course_section=course_section,
        students=students,
        grades=grades
    )

@evaluation_bp.route('/delete/<int:evaluation_id>/<int:course_section_id>', methods=['POST'])
def delete_evaluation_view(evaluation_id, course_section_id):
    evaluation = get_evaluation(evaluation_id)
    if evaluation:
        delete_evaluation(evaluation)
        return redirect(url_for('course_sections.show_section_view', course_section_id=course_section_id))
    
    return redirect(url_for('course_sections.show_section_view', course_section_id=course_section_id))