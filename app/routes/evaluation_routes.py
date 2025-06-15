from flask import (
    Blueprint, request, render_template, redirect, url_for, send_file, flash
)

from app.controllers.evaluation_controller import (
    get_evaluation, create_evaluation, update_evaluation,
    delete_evaluation, export_evaluation_report_to_excel
)
from app.controllers.evaluation_type_controller import get_evaluation_type
from app.controllers.course_section_controller import get_section
from app.validators.evaluation_validator import assign_default_ponderations

evaluation_bp = Blueprint('evaluations', __name__, url_prefix='/evaluations')

@evaluation_bp.route(
    '/create/<int:evaluation_type_id>',
    methods=['GET', 'POST']
)
def create_evaluation_view(evaluation_type_id):
    evaluation_type = get_evaluation_type(evaluation_type_id)
    if not evaluation_type:
        return redirect(url_for(
            'course_sections.show_section_view',
            course_section_id=evaluation_type.course_section_id
        ))
    
    error = None
    if request.method == 'POST':
        evaluations = build_evaluation_data(request.form, evaluation_type_id)
        
        error = assign_default_ponderations(evaluation_type, evaluations)

        if not error:
            for data in evaluations:
                evaluation, current_sum = create_evaluation(data)
                if evaluation is None:
                    error = (
                        f'Suma actual de ponderaciones: {current_sum}%. '
                        f'No puede exceder 100% al agregar esta evaluación.'
                    )
                    break
            
        if error:
            return render_template(
                'evaluations/create.html',
                evaluation_type=evaluation_type,
                error=error,
            )

        return redirect(url_for(
            'course_sections.show_section_view',
            course_section_id=evaluation_type.course_section_id
        ))

    return render_template(
        'evaluations/create.html',
        evaluation_type=evaluation_type,
        error=error
    )

@evaluation_bp.route('/<int:evaluation_id>', methods=['GET', 'POST'])
def update_evaluation_view(evaluation_id):
    error = None
    evaluation = get_evaluation(evaluation_id)
    if not evaluation:
        return redirect(url_for(
            'course_sections.show_section_view',
            course_section_id=evaluation.evaluation_type.course_section_id
        ))

    if request.method == 'POST':
        data = request.form.to_dict()
        data['optional'] = 'optional' in request.form

        updated_evaluation, current_sum = update_evaluation(evaluation, data)
        
        if updated_evaluation is None:
            error = (
                f'Suma actual sin esta evaluación: {current_sum}%. '
                f'No puede exceder 100% al actualizar.'
            )
        else:
            return redirect(url_for(
                'course_sections.show_section_view',
                course_section_id=evaluation.evaluation_type.course_section_id
            ))

    return render_template(
        'evaluations/edit.html', evaluation=evaluation, error=error
    )

@evaluation_bp.route('/<int:evaluation_id>/show', methods=['GET'])
def show_evaluation_view(evaluation_id):
    evaluation = get_evaluation(evaluation_id)
    if not evaluation:
        return redirect(url_for('home'))

    evaluation_type = get_evaluation_type(evaluation.evaluation_type_id)
    course_section = get_section(evaluation_type.course_section_id)
    students = course_section.student_courses

    grades = build_grades_dict(evaluation)

    return render_template(
        'evaluations/show.html',
        evaluation=evaluation,
        evaluation_type=evaluation_type,
        course_section=course_section,
        students=students,
        grades=grades
    )

@evaluation_bp.route(
    '/delete/<int:evaluation_id>/<int:course_section_id>',
    methods=['POST']
)
def delete_evaluation_view(evaluation_id, course_section_id):
    evaluation = get_evaluation(evaluation_id)
    if evaluation:
        delete_evaluation(evaluation)
        return redirect(url_for(
            'course_sections.show_section_view',
            course_section_id=course_section_id
        ))

    return redirect(url_for(
        'course_sections.show_section_view',
        course_section_id=course_section_id
    ))

def build_grades_dict(evaluation):
    return {
        student_evaluation.student_id: student_evaluation.grade
        for student_evaluation in evaluation.student_evaluations
    }

def build_evaluation_data(form_data, evaluation_type_id):
    evaluations = []

    for key in form_data:
        if key.startswith('name_'):
            index = key.split('_')[1]
            name = form_data.get(f'name_{index}')
            ponderation = form_data.get(f'ponderation_{index}')
            optional = form_data.get(f'optional_{index}') == 'on'

            data = {
                'name': name,
                'ponderation': ponderation if ponderation else None,
                'optional': optional,
                'evaluation_type_id': evaluation_type_id
            }

            evaluations.append(data)

    return evaluations

@evaluation_bp.route('/<int:evaluation_id>/report', methods=['GET'])
def download_evaluation_report(evaluation_id):
    evaluation = get_evaluation(evaluation_id)
    result = export_evaluation_report_to_excel(evaluation)

    if result is None:
        flash(
            'No se puede generar reporte para esta evaluación',
            'error'
        )
        print("SECTION ID:", evaluation.evaluation_type.course_section_id)
        return redirect(
            url_for(
                'course_sections.show_section_view',
                course_section_id=evaluation.evaluation_type.course_section_id
        ))

    file_buffer, filename = result
    return send_file(file_buffer, as_attachment=True, download_name=filename)
